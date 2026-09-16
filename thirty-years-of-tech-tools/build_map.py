"""Build the skill merge map from the corpus, then report what it merged.

Strategy (same shape as skillenai-api-skill/scripts/canonicalize_skills.py, but
driven off resolved ENTITY IDS rather than free text, because the ids are what
the exact server-side recount will key on):

  1. group every resolved canonical_name by norm() -- lowercase, punctuation and
     separator collapsed, trailing parenthetical dropped, "+"/"#" preserved so
     C / C++ / C# stay apart;
  2. within a group the most-frequent surface form becomes the display label,
     EXCEPT where canon.ALIAS names one explicitly (so "js" and "javascript"
     land on "JavaScript" even though neither is the modal spelling);
  3. emit {entity_id: concept_label} -- the map the exact recount consumes.

Writes _out/merge_map.json and _out/merge_audit.txt.
"""
from __future__ import annotations
import collections, csv, gzip, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from canon import ALIAS, PROTECTED, display, norm  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "_out"
OUT.mkdir(exist_ok=True)

_PROT_LABEL = {"c": "C", "c++": "C++", "c#": "C#", "r": "R", "go": "Go",
               "f#": "F#", ".net": ".NET", "j2ee": "J2EE", "d": "D"}


def main() -> int:
    # entity_id -> name (an id has exactly one canonical_name), and name volume
    id_name: dict[str, str] = {}
    name_n: collections.Counter = collections.Counter()
    with gzip.open(HERE / "_data/skill_year.csv.gz", "rt",
                   encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            nm = (r["canonical_name"] or "").strip()
            if not nm:
                continue
            id_name[r["dst_id"]] = nm
            name_n[nm] += int(r["n_pos"])

    # group names by normalised key
    groups: dict[str, list[str]] = collections.defaultdict(list)
    for nm in name_n:
        k = norm(nm)
        if k:
            groups[k].append(nm)

    label: dict[str, str] = {}      # normalised key -> display label
    for k, names in groups.items():
        if k in PROTECTED:
            label[k] = _PROT_LABEL[k]
        elif k in ALIAS:
            label[k] = ALIAS[k]
        else:
            label[k] = display(max(names, key=lambda n: (name_n[n], -len(n))))

    merge = {eid: label[norm(nm)] for eid, nm in id_name.items() if norm(nm)}
    json.dump(merge, open(OUT / "merge_map.json", "w"))

    # audit: the biggest groups that actually merged something
    merged = [(sum(name_n[n] for n in v), label[k], sorted(v, key=lambda n: -name_n[n]))
              for k, v in groups.items() if len(v) > 1]
    merged.sort(reverse=True)
    with open(OUT / "merge_audit.txt", "w") as fh:
        for tot, lab, names in merged:
            fh.write(f"{tot:>8,}  {lab}\n          <- {', '.join(names[:8])}\n")

    print(f"entity ids        : {len(id_name):,}")
    print(f"distinct names    : {len(name_n):,}")
    print(f"distinct concepts : {len(set(merge.values())):,}")
    print(f"groups that merged: {len(merged):,}\n")
    print("largest merges:")
    for tot, lab, names in merged[:30]:
        print(f"  {tot:>8,}  {lab:<22} <- {', '.join(names[:5])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
