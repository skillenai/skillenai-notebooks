"""Artifact checks, run BEFORE any number from this corpus is interpreted.

Three things could manufacture the headline ("titles fragmented while skills
consolidated") without any of it being true, and each gets a test whose correct
answer is known in advance:

  A. THIN EARLY YEARS. 1996 has 3,549 skill-bearing positions against 45,884 in
     2022. A distribution estimated from fewer positions is noisier, and noise
     both depresses year-to-year similarity and INFLATES effective-N (spurious
     singletons look like diversity). Test: a split-half null -- two disjoint
     random halves of the SAME year, at a sample size held equal across all
     years. Its correct value is "no change", so whatever it reports is the
     measurement floor, and only excess over it counts.

  B. VERBOSITY DRIFT. Skills per position rises 4.5 -> 6.7 across the window.
     Longer skill lists reach further down the tail. Test: recompute
     concentration WITHIN strata of identical skill count. If the trend
     survives at fixed k, verbosity is not producing it.

  C. ROLE MIX. The corpus shifts toward data/AI roles, which may simply share a
     narrower toolkit. Test: recompute within single large roles.

Everything here is resampled at a FIXED NUMBER OF POSITIONS, never a fixed
fraction of a growing corpus, and effective-N is reported with its bootstrap CI.
"""
from __future__ import annotations
import collections, csv, gzip, json, pathlib, sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, "/Users/jrand/git-repos/skillenai-notebooks/who-feeds-ai-roles")

HERE = pathlib.Path(__file__).resolve().parent
DATA, OUT = HERE / "_data", HERE / "_out"
MERGE = json.load(open(OUT / "merge_map.json"))

Y0, Y1 = 1996, 2024
NBOOT = 300
RNG = np.random.default_rng(20260916)


def load_positions():
    """{year: [ (skill_label, ...), ... ]} -- one tuple per position.

    Also returns per-position role, so the role-mix check can reuse the load.
    """
    from allroles import role_of
    pos_skills: dict[str, list[str]] = collections.defaultdict(list)
    pos_meta: dict[str, tuple] = {}
    with gzip.open(DATA / "positions.csv.gz", "rt", encoding="utf-8",
                   errors="replace") as fh:
        for r in csv.DictReader(fh):
            yr = int(r["yr"])
            if not (Y0 <= yr <= Y1):
                continue
            lab = MERGE.get(r["dst_id"])
            if not lab:
                continue
            p = r["pos"]
            pos_skills[p].append(lab)
            if p not in pos_meta:
                pos_meta[p] = (yr, role_of(r["role"] or ""), r["mon"])
    by_year: dict[int, list] = collections.defaultdict(list)
    for p, sk in pos_skills.items():
        yr, role, mon = pos_meta[p]
        by_year[yr].append((tuple(sorted(set(sk))), role, mon))
    return by_year


# ------------------------------------------------------------------ measures
def eff_n(positions) -> float:
    """Inverse Herfindahl of the skill-MENTION distribution over a position set."""
    c = collections.Counter()
    for sk, _, _ in positions:
        c.update(sk)
    if not c:
        return float("nan")
    p = np.array(list(c.values()), dtype=float)
    p /= p.sum()
    return float(1.0 / (p ** 2).sum())


def vec(positions, keys_idx, n_keys):
    v = np.zeros(n_keys)
    for sk, _, _ in positions:
        for s in sk:
            i = keys_idx.get(s)
            if i is not None:
                v[i] += 1
    return v


def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(a @ b / (na * nb)) if na and nb else float("nan")


# ------------------------------------------------------------------ checks
def check_a_split_half(by_year, m):
    """Churn with a split-half null. m = positions per draw, equal every year."""
    keys = sorted({s for yr in by_year for sk, _, _ in by_year[yr] for s in sk})
    ki = {k: i for i, k in enumerate(keys)}
    nk = len(keys)
    print(f"\n{'='*74}\nCHECK A - churn against a split-half null "
          f"({m} positions/draw, {NBOOT} reps, {nk:,} skills)\n{'='*74}")
    print(f"{'pair':>12} {'observed':>9} {'null':>8} {'excess':>9} {'95% CI':>18}")
    res = {}
    for lag in (1, 5):
        print(f"\n-- lag {lag}y --")
        for yr in range(Y0 + lag, Y1 + 1):
            A, B = by_year[yr - lag], by_year[yr]
            if len(A) < 2 * m or len(B) < 2 * m:
                continue
            obs, nul = [], []
            for _ in range(NBOOT):
                ia = RNG.choice(len(A), 2 * m, replace=False)
                ib = RNG.choice(len(B), 2 * m, replace=False)
                a1 = vec([A[i] for i in ia[:m]], ki, nk)
                a2 = vec([A[i] for i in ia[m:]], ki, nk)
                b1 = vec([B[i] for i in ib[:m]], ki, nk)
                b2 = vec([B[i] for i in ib[m:]], ki, nk)
                obs.append(0.5 * (cos(a1, b1) + cos(a2, b2)))
                nul.append(0.5 * (cos(a1, a2) + cos(b1, b2)))
            obs, nul = np.array(obs), np.array(nul)
            exc = nul - obs
            lo, hi = np.percentile(exc, [2.5, 97.5])
            res[f"lag{lag}_{yr}"] = dict(obs=float(obs.mean()), null=float(nul.mean()),
                                         excess=float(exc.mean()), lo=float(lo), hi=float(hi))
            if yr % 3 == 0:
                print(f"{yr-lag}->{yr:<7} {obs.mean():>9.4f} {nul.mean():>8.4f} "
                      f"{exc.mean():>9.4f}   [{lo:.4f}, {hi:.4f}]")
    return res


def check_b_verbosity(by_year, m):
    """Effective-N per year within strata of identical skills-per-position."""
    print(f"\n{'='*74}\nCHECK B - concentration at FIXED skills-per-position\n{'='*74}")
    print(f"{'year':>6} {'all k':>16}" + "".join(f"{f'k={k}':>16}" for k in (3, 5, 7)))
    res = {}
    for yr in range(Y0, Y1 + 1, 2):
        row = {}
        cells = [("all", by_year[yr])]
        cells += [(k, [p for p in by_year[yr] if len(p[0]) == k]) for k in (3, 5, 7)]
        line = f"{yr:>6}"
        for name, pool in cells:
            if len(pool) < m:
                line += f"{'-':>16}"
                row[str(name)] = None
                continue
            vals = [eff_n([pool[i] for i in RNG.choice(len(pool), m, replace=False)])
                    for _ in range(60)]
            lo, hi = np.percentile(vals, [2.5, 97.5])
            row[str(name)] = dict(mean=float(np.mean(vals)), lo=float(lo), hi=float(hi))
            line += f"{np.mean(vals):>9.0f} ±{(hi-lo)/2:>5.0f}"
        print(line)
        res[yr] = row
    return res


def check_c_rolemix(by_year, m):
    """Effective-N within single large roles, so role composition cannot drive it."""
    print(f"\n{'='*74}\nCHECK C - concentration WITHIN a single role\n{'='*74}")
    roles = ["Software Engineer", "Data Analyst", "QA / SDET Engineer"]
    print(f"{'year':>6}" + "".join(f"{r[:20]:>22}" for r in roles))
    res = {}
    for yr in range(Y0, Y1 + 1, 2):
        line, row = f"{yr:>6}", {}
        for r in roles:
            pool = [p for p in by_year[yr] if p[1] == r]
            if len(pool) < m:
                line += f"{'-':>22}"
                row[r] = None
                continue
            vals = [eff_n([pool[i] for i in RNG.choice(len(pool), m, replace=False)])
                    for _ in range(60)]
            row[r] = float(np.mean(vals))
            line += f"{np.mean(vals):>16.0f} (n={len(pool)//1000}k)" if len(pool) > 1000 \
                else f"{np.mean(vals):>22.0f}"
        print(line)
        res[yr] = row
    return res


def main() -> int:
    by_year = load_positions()
    sizes = {y: len(by_year[y]) for y in range(Y0, Y1 + 1)}
    print("positions per year:", {y: sizes[y] for y in (1996, 2000, 2010, 2020, 2024)})
    m_small = min(sizes.values()) // 2          # split-half needs 2m per year
    print(f"smallest year {min(sizes.values()):,} -> m = {m_small:,} positions/draw")

    res = {
        "split_half": check_a_split_half(by_year, m_small),
        "verbosity": check_b_verbosity(by_year, 800),
        "rolemix": check_c_rolemix(by_year, 400),
    }
    json.dump(res, open(OUT / "robust.json", "w"), indent=0)
    print(f"\nwrote {OUT/'robust.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
