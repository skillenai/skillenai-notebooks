"""Build a skill merge map that collapses duplicate surface forms.

Strategy:
  1. Normalize case + whitespace + hyphens/underscores, PRESERVE +/# (so C++ vs C# vs C stay distinct).
  2. Strip trailing parenthetical suffixes (e.g. "Retrieval-Augmented Generation (RAG)" -> base form).
  3. Group by normalized form; canonical = most-frequent surface form in the group.
  4. Cross-reference acronym parens with standalone acronyms (LLMs, RAG, NLP, etc.).
  5. Strip "meta-tag" descriptive parens like "(evals)", "(descriptive)", "(OOP)".
  6. Manual safety list: never merge across distinct tokens (C, C++, C#, R, Rust, Go, etc.).

Output:
  - skill_merge_map.json: surface_form -> canonical_form
  - skill_merge_candidates.csv: review table
"""
import csv
import json
import re
from collections import Counter, defaultdict

CSV_IN = "jobs.csv"

# Never merge these — they're distinct entities even if they normalize to something short
PROTECTED = {"C", "C++", "C#", "R", "Go", "Rust", "Java", "JavaScript", "TypeScript", "Swift", "Ruby", "Scala", "Python", "PHP", "Perl", "Lua", "Kotlin", "Dart", "Julia", "Haskell", "F#", ".NET"}

# Acronym pairs we explicitly do NOT want merged (false positives from acronym collision)
# Format: frozenset({canonical_form_a, canonical_form_b})
ACRONYM_BLOCKLIST = {
    frozenset({"React", "Reasoning and Acting (ReAct)"}),  # frontend framework vs agent pattern
    frozenset({"React", "ReAct"}),
}


def normalize(s):
    s = s.strip()
    # Strip trailing parenthetical suffix: "Foo (BAR)" -> "Foo"
    # Do this BEFORE lowercasing so we can still match acronyms
    s_no_paren = re.sub(r"\s*\([^)]*\)\s*$", "", s).strip()
    # Use the no-paren form if it's non-trivial, else the original
    base = s_no_paren if len(s_no_paren) >= 2 else s
    # Lowercase + normalize hyphens/underscores/slashes to single spaces
    t = base.lower()
    t = re.sub(r"[-_/]+", " ", t)
    # Collapse whitespace
    t = re.sub(r"\s+", " ", t).strip()
    # Strip trailing punctuation but keep + and #
    t = re.sub(r"[^\w\s+#]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def extract_parens_acronym(s):
    m = re.search(r"\(([A-Za-z][A-Za-z0-9]{1,})\)\s*$", s)
    if m:
        return m.group(1)
    return None


def main():
    counts = Counter()
    with open(CSV_IN) as f:
        for row in csv.DictReader(f):
            for sk in (row["skills"] or "").split("|"):
                if sk:
                    counts[sk] += 1

    # Build normalized groups, respecting protected list
    groups = defaultdict(list)  # norm_key -> [(surface, count)]
    for sk, c in counts.items():
        if sk in PROTECTED:
            # Each protected skill becomes its own singleton group (keyed by raw form)
            groups[f"__PROTECTED__{sk}"].append((sk, c))
            continue
        n = normalize(sk)
        if not n:
            continue
        groups[n].append((sk, c))

    # Pick canonical per group (most frequent surface form)
    merge_map = {}  # surface -> canonical
    groups_rich = []  # for CSV
    for norm, members in groups.items():
        if len(members) == 1:
            continue  # nothing to merge
        members_sorted = sorted(members, key=lambda x: (-x[1], x[0]))
        canonical = members_sorted[0][0]
        total_n = sum(c for _, c in members)
        for surface, _ in members_sorted[1:]:
            merge_map[surface] = canonical
        groups_rich.append({
            "canonical": canonical,
            "norm": norm,
            "members": " / ".join(f"{m}({c})" for m, c in members_sorted),
            "total": total_n,
            "method": "normalize",
        })

    # Acronym-expansion pass: look at every canonical skill; if it ends with "(ACRONYM)"
    # AND the acronym exists as another canonical, merge the expanded form into the shorter acronym
    # (or vice versa, pick the more-frequent one)
    canonical_forms = set(counts) - set(merge_map)  # surface forms that still map to themselves
    # Dict of canonical -> count, accounting for absorbed merges
    canonical_counts = Counter()
    for sk, c in counts.items():
        target = merge_map.get(sk, sk)
        canonical_counts[target] += c

    # Find acronym pairs among current canonicals
    canon_lc = {c.lower(): c for c in canonical_counts}
    for canon in list(canonical_counts.keys()):
        acro = extract_parens_acronym(canon)
        if not acro:
            continue
        # Look for standalone acronym form
        standalone = canon_lc.get(acro.lower())
        if standalone and standalone != canon and standalone not in PROTECTED \
           and frozenset({standalone, canon}) not in ACRONYM_BLOCKLIST:
            # Prefer the shorter form (the standalone acronym) as canonical — cleaner in tables
            winner, loser = standalone, canon
            # Apply: update merge_map so everything pointing to loser now points to winner
            merge_map[loser] = winner
            for s, t in list(merge_map.items()):
                if t == loser:
                    merge_map[s] = winner
            canonical_counts[winner] += canonical_counts[loser]
            del canonical_counts[loser]
            groups_rich.append({
                "canonical": winner,
                "norm": "",
                "members": f"{winner}({counts.get(winner,0)}) <- {loser}({counts.get(loser,0)})",
                "total": canonical_counts[winner],
                "method": "acronym",
            })

    # Meta-tag stripping: "evaluation (evals)" -> "evaluation" if bare form exists
    for surface in list(counts):
        if surface in merge_map or surface in PROTECTED:
            continue
        stripped = re.sub(r"\s*\([^)]*\)\s*$", "", surface).strip()
        if stripped and stripped != surface and stripped in canonical_counts and stripped != surface:
            # merge this surface into the stripped form
            target = merge_map.get(stripped, stripped)
            merge_map[surface] = target
            groups_rich.append({
                "canonical": target,
                "norm": "",
                "members": f"{surface} -> {target}",
                "total": counts[surface],
                "method": "meta_strip",
            })

    # Write outputs
    with open("skill_merge_map.json", "w") as f:
        json.dump(merge_map, f, indent=2, sort_keys=True)
    print(f"Wrote skill_merge_map.json with {len(merge_map)} surface->canonical mappings")

    groups_rich.sort(key=lambda r: -r["total"])
    with open("skill_merge_candidates.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["canonical", "norm", "members", "total", "method"])
        w.writeheader()
        w.writerows(groups_rich)
    print(f"Wrote skill_merge_candidates.csv with {len(groups_rich)} groups")

    print("\nTop 30 merges by combined count:")
    print(f"{'canonical':35} {'method':12} {'N':>6}  members")
    for r in groups_rich[:30]:
        print(f"{r['canonical'][:35]:35} {r['method']:12} {r['total']:>6}  {r['members'][:80]}")


if __name__ == "__main__":
    main()
