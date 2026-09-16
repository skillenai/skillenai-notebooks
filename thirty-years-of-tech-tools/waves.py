"""What churns, and when.

Quarterly trailing-twelve-month shares -- the same construction as the companion
role race, for the same two reasons: a 12-month window cancels the January
imputation spike (a bare "2019" start date is imputed to January, putting 17.7%
of starts there), and it cancels calendar seasonality, so a partial final year
does not read as a collapse. Windows ending after the last solid quarter are
kept and marked provisional rather than dropped.

For each named technology the lifecycle is measured, not assumed:

  rise  = quarters from the first window at >=25% of its own peak, to the peak
  fall  = quarters from the peak to the first window back below 50% of it

`fall` is RIGHT-CENSORED for anything still near its peak, so it is reported as
a survival quantity: censored items are counted as "has not fallen yet" rather
than dropped, because dropping them keeps only the things that died and makes
every era look equally fatal.
"""
from __future__ import annotations
import collections, csv, gzip, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from named import audit, kind  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
DATA, OUT = HERE / "_data", HERE / "_out"
MERGE = json.load(open(OUT / "merge_map.json"))

Y0, Y1 = 1994, 2025
LAST_SOLID = (2025, 6)      # employment records run to ~Oct 2025 (SKI-531)
LAST_Q = (2025, 9)


def qs():
    out = [(y, m) for y in range(1996, Y1 + 1) for m in (3, 6, 9, 12)]
    return [q for q in out if q <= LAST_Q]


def main() -> int:
    pos = collections.Counter()
    hit: dict[tuple, collections.Counter] = collections.defaultdict(collections.Counter)
    seen: set[str] = set()
    with gzip.open(DATA / "positions.csv.gz", "rt", encoding="utf-8",
                   errors="replace") as fh:
        for r in csv.DictReader(fh):
            yr = int(r["yr"])
            if not (Y0 <= yr <= Y1):
                continue
            mon = int(r["mon"] or 1)
            if r["pos"] not in seen:
                seen.add(r["pos"])
                pos[(yr, mon)] += 1
            if (lab := MERGE.get(r["dst_id"])):
                hit[(yr, mon)][lab] += 1
    print(f"positions {len(seen):,}")

    QS = qs()
    SHARE, TOT = {}, {}
    for (y, m) in QS:
        yy, mm, tot, c = y, m, 0, collections.Counter()
        for _ in range(12):
            tot += pos[(yy, mm)]
            c.update(hit.get((yy, mm), {}))
            mm -= 1
            if mm == 0:
                yy, mm = yy - 1, 12
        TOT[(y, m)] = tot
        SHARE[(y, m)] = {k: 100.0 * v / tot for k, v in c.items()} if tot else {}

    peak = collections.defaultdict(float)
    for q in QS:
        for k, v in SHARE[q].items():
            peak[k] = max(peak[k], v)

    POOL = sorted([k for k, v in peak.items() if v >= 0.5 and kind(k) == "named"],
                  key=lambda k: -peak[k])
    un = audit([k for k, v in peak.items() if v >= 0.5])
    print(f"named technologies ever >=0.5% of a window: {len(POOL)}")
    if un:
        print(f"!! UNASSIGNED (fix named.py before shipping): {un}")

    # ---------------------------------------------------------------- lifecycle
    qi = {q: i for i, q in enumerate(QS)}
    rows = []
    for k in POOL:
        s = [SHARE[q].get(k, 0.0) for q in QS]
        pk = max(s)
        pq = s.index(pk)
        rise_from = next((i for i, v in enumerate(s) if v >= 0.25 * pk), pq)
        # first window at or after the peak that drops below half of it
        fall_at = next((i for i in range(pq, len(s)) if s[i] < 0.50 * pk), None)
        rows.append({
            "skill": k, "peak": round(pk, 3),
            "peak_q": f"{QS[pq][0]}Q{QS[pq][1]//3}",
            "peak_year": QS[pq][0],
            "rise_q": pq - rise_from,
            "fall_q": (fall_at - pq) if fall_at is not None else None,
            "censored": fall_at is None,
            "now": round(s[-1], 3), "rel_now": round(s[-1] / pk, 3) if pk else 0,
        })

    print(f"\n{'technology':<18}{'peak':>7} {'peaked':>8} {'rise':>6} {'fall':>7} {'now/peak':>10}")
    for r in sorted(rows, key=lambda r: (r["peak_year"], -r["peak"])):
        f = "still up" if r["censored"] else f"{r['fall_q']}q"
        print(f"{r['skill'][:17]:<18}{r['peak']:>6.2f}% {r['peak_q']:>8} "
              f"{r['rise_q']:>5}q {f:>7} {100*r['rel_now']:>9.0f}%")

    # ------------------------------------------------- adoption speed by era
    print(f"\n{'='*70}\nIS ADOPTION GETTING FASTER?  (rise quarters, by peak era)\n{'='*70}")
    import statistics
    for lo, hi in ((1996, 2003), (2004, 2011), (2012, 2018), (2019, 2025)):
        g = [r["rise_q"] for r in rows if lo <= r["peak_year"] <= hi]
        if g:
            print(f"  peaked {lo}-{hi}: n={len(g):>3}  median rise "
                  f"{statistics.median(g):>5.1f}q  mean {statistics.mean(g):>5.1f}q")
    print("\nNOTE: items peaking in the first window have their rise truncated by")
    print("the corpus start, and items peaking in the last window cannot yet fall.")

    print(f"\n{'='*70}\nHOW MANY HAVE FALLEN BELOW HALF THEIR PEAK, by peak era\n{'='*70}")
    for lo, hi in ((1996, 2003), (2004, 2011), (2012, 2018), (2019, 2025)):
        g = [r for r in rows if lo <= r["peak_year"] <= hi]
        if g:
            fell = sum(1 for r in g if not r["censored"])
            print(f"  peaked {lo}-{hi}: {fell}/{len(g)} fell "
                  f"({100*fell/len(g):.0f}%)")

    json.dump({"quarters": [list(q) for q in QS],
               "last_solid": list(LAST_SOLID),
               "totals": {f"{y}Q{m//3}": TOT[(y, m)] for (y, m) in QS},
               "pool": POOL,
               "lifecycle": rows,
               "share": {f"{y}Q{m//3}": {k: round(SHARE[(y, m)].get(k, 0.0), 4)
                                         for k in POOL} for (y, m) in QS}},
              open(OUT / "waves.json", "w"))
    print(f"\nwrote {OUT/'waves.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
