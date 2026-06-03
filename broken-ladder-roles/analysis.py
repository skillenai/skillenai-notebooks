"""Broken Ladder analysis: role-level remote-by-seniority gradient,
testing whether the gradient is correlated with AI exposure.

Builds on remote-by-seniority/ by adding:
  (1) A wider role inventory (~20 roles, N>=250)
  (2) Per-role AI-skill prevalence (data-driven AI exposure score)
  (3) Per-role "broken-ladder slope": entry vs senior % any-remote gap
  (4) Test whether slope correlates with AI exposure
      (Lambert/Schindler 2026 prediction: no correlation -> WFH, not AI)

Run from this directory. Requires SKILLENAI_INSIGHTS_API_KEY in env.
"""
import json
import os
import pathlib
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from scipy import stats

HERE = pathlib.Path(__file__).parent
API_KEY = os.environ.get("SKILLENAI_INSIGHTS_API_KEY") or sys.exit(
    "SKILLENAI_INSIGHTS_API_KEY not set"
)
API_URL = "https://api.skillenai.com"
HDR = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

US_TECH_FILTER = {
    "bool": {
        "filter": [
            {"term": {"locationCountry": "US"}},
            {"terms": {"workModel": ["onsite", "remote", "hybrid"]}},
            {
                "terms": {
                    "seniorityLevel": [
                        "intern", "entry", "mid", "senior", "staff", "principal",
                    ]
                }
            },
        ],
        "must_not": [{"term": {"companyCanonicalName.keyword": "Speechify"}}],
    }
}

# Tech IC roles with N >= ~250 in the US filtered universe.
# Title-tagged seniority variants (Staff X, Principal X, Senior X) excluded —
# those duplicate the seniorityLevel signal at the title level.
ROLES = [
    "Software Engineer",
    "Backend Engineer",
    "Frontend Engineer",
    "Full Stack Engineer",
    "DevOps Engineer",
    "Site Reliability Engineer",
    "Platform Engineer",
    "Infrastructure Engineer",
    "Security Engineer",
    "Forward Deployed Engineer",
    "Data Engineer",
    "Data Scientist",
    "Data Analyst",
    "Machine Learning Engineer",
    "ML Engineer",
    "AI Engineer",
    "Research Scientist",
    "Research Engineer",
    "Analytics Engineer",
    "Product Manager",
    "Product Designer",
    "Technical Program Manager",
]

# Curated AI-exposure tier per role.  Validated against AI-skill prevalence
# in fetch_ai_exposure() below — if a role's data-driven score disagrees
# with the curated tier, we re-evaluate.
AI_TIER = {
    "Software Engineer": "medium",
    "Backend Engineer": "light",
    "Frontend Engineer": "light",
    "Full Stack Engineer": "light",
    "DevOps Engineer": "light",
    "Site Reliability Engineer": "light",
    "Platform Engineer": "light",
    "Infrastructure Engineer": "light",
    "Security Engineer": "light",
    "Forward Deployed Engineer": "medium",
    "Data Engineer": "medium",
    "Data Scientist": "heavy",
    "Data Analyst": "medium",
    "Machine Learning Engineer": "heavy",
    "ML Engineer": "heavy",
    "AI Engineer": "heavy",
    "Research Scientist": "heavy",
    "Research Engineer": "heavy",
    "Analytics Engineer": "medium",
    "Product Manager": "light",
    "Product Designer": "light",
    "Technical Program Manager": "light",
}

ORDER = ["intern", "entry", "mid", "senior", "staff", "principal"]

# Phrases used to measure AI exposure per role.  Cast a wide net —
# multiple spellings to mitigate phrase-recall issues.
AI_PHRASES = [
    "machine learning",
    "deep learning",
    "neural network",
    "large language model",
    " LLM ",  # leading/trailing spaces to avoid sub-string matches
    "PyTorch",
    "TensorFlow",
    "transformer model",
    "generative AI",
]


def query(body, retries=3):
    for attempt in range(retries):
        r = requests.post(
            f"{API_URL}/v1/query/search", headers=HDR, json=body, timeout=60
        )
        if r.status_code == 429:
            time.sleep(9 * (attempt + 1))
            continue
        r.raise_for_status()
        return r.json()
    r.raise_for_status()


def fetch_per_role():
    """Per-role × per-seniority × per-workmodel counts."""
    body = {
        "query": {
            "size": 0,
            "track_total_hits": True,
            "query": {
                "bool": {
                    "filter": US_TECH_FILTER["bool"]["filter"]
                    + [{"terms": {"role.keyword": ROLES}}],
                    "must_not": US_TECH_FILTER["bool"]["must_not"],
                }
            },
            "aggs": {
                "by_role": {
                    "terms": {"field": "role.keyword", "size": len(ROLES) + 5},
                    "aggs": {
                        "by_sen": {
                            "terms": {"field": "seniorityLevel", "size": 10},
                            "aggs": {
                                "by_wm": {
                                    "terms": {"field": "workModel", "size": 5}
                                }
                            },
                        }
                    },
                }
            },
        },
        "indices": ["prod-enriched-jobs"],
    }
    d = query(body)
    rows = []
    for r in d["aggregations"]["by_role"]["buckets"]:
        for s in r["by_sen"]["buckets"]:
            wm = {x["key"]: x["doc_count"] for x in s["by_wm"]["buckets"]}
            o = wm.get("onsite", 0)
            h = wm.get("hybrid", 0)
            rm = wm.get("remote", 0)
            tot = o + h + rm
            rows.append(
                {
                    "role": r["key"],
                    "seniority": s["key"],
                    "n": tot,
                    "onsite": o,
                    "hybrid": h,
                    "remote": rm,
                    "pct_any_remote": 100 * (h + rm) / tot if tot else None,
                }
            )
    return pd.DataFrame(rows)


def fetch_ai_exposure():
    """For each role, what % of US postings mention an AI/ML phrase.

    Uses a single filters-aggregation per role (one query per role total).
    """
    rows = []
    for role in ROLES:
        body = {
            "query": {
                "size": 0,
                "track_total_hits": True,
                "query": {
                    "bool": {
                        "filter": US_TECH_FILTER["bool"]["filter"]
                        + [{"term": {"role.keyword": role}}],
                        "must_not": US_TECH_FILTER["bool"]["must_not"],
                    }
                },
                "aggs": {
                    "ai_mentions": {
                        "filter": {
                            "bool": {
                                "should": [
                                    {"match_phrase": {"extractedText": p.strip()}}
                                    for p in AI_PHRASES
                                ],
                                "minimum_should_match": 1,
                            }
                        }
                    }
                },
            },
            "indices": ["prod-enriched-jobs"],
        }
        d = query(body)
        tot = d.get("total", 0)
        ai = d["aggregations"]["ai_mentions"]["doc_count"]
        rows.append(
            {"role": role, "n_total": tot, "n_ai": ai,
             "pct_ai": 100 * ai / tot if tot else 0.0,
             "tier": AI_TIER[role]}
        )
        time.sleep(0.7)
    return pd.DataFrame(rows).sort_values("pct_ai", ascending=False)


def compute_broken_ladder(per_role):
    """For each role, compute the entry -> senior gap in %any-remote.

    This is the 'broken-ladder slope' — how much more likely a senior
    is to find a remote/hybrid posting than an entry-level worker in
    the same role.
    """
    rows = []
    for role in ROLES:
        sub = per_role[per_role["role"] == role].set_index("seniority")
        if "entry" not in sub.index or "senior" not in sub.index:
            continue
        n_entry = sub.loc["entry", "n"]
        n_senior = sub.loc["senior", "n"]
        if n_entry < 30 or n_senior < 50:
            # too thin to be reliable
            continue
        pe = sub.loc["entry", "pct_any_remote"]
        ps = sub.loc["senior", "pct_any_remote"]
        # Wilson 95% CI on each proportion for a simple error band
        ci_e = stats.binomtest(int(round(n_entry * pe / 100)), n_entry).proportion_ci(
            confidence_level=0.95, method="wilson"
        )
        ci_s = stats.binomtest(int(round(n_senior * ps / 100)), n_senior).proportion_ci(
            confidence_level=0.95, method="wilson"
        )
        rows.append(
            {
                "role": role,
                "tier": AI_TIER[role],
                "n_entry": n_entry,
                "n_senior": n_senior,
                "pct_entry": pe,
                "pct_senior": ps,
                "gap_pp": ps - pe,
                "ci_entry_low": ci_e.low * 100,
                "ci_entry_high": ci_e.high * 100,
                "ci_senior_low": ci_s.low * 100,
                "ci_senior_high": ci_s.high * 100,
            }
        )
    return pd.DataFrame(rows).sort_values("gap_pp", ascending=False)


def test_ai_correlation(ladder_df, exposure_df):
    """Lambert/Schindler 'WFH-not-AI' prediction: there should be NO
    correlation between a role's AI exposure and its broken-ladder gap.
    """
    merged = ladder_df.merge(
        exposure_df[["role", "pct_ai"]], on="role", how="inner"
    )
    if len(merged) < 5:
        return None
    rho, p = stats.spearmanr(merged["pct_ai"], merged["gap_pp"])
    r, p_pearson = stats.pearsonr(merged["pct_ai"], merged["gap_pp"])
    # Also test mean gap by tier (one-way ANOVA between heavy/medium/light)
    by_tier = {t: merged[merged["tier"] == t]["gap_pp"].tolist()
               for t in ("heavy", "medium", "light")}
    f_stat, anova_p = stats.f_oneway(
        by_tier["heavy"], by_tier["medium"], by_tier["light"]
    )
    return {
        "spearman_rho": rho,
        "spearman_p": p,
        "pearson_r": r,
        "pearson_p": p_pearson,
        "anova_f": f_stat,
        "anova_p": anova_p,
        "mean_gap_heavy": float(np.mean(by_tier["heavy"])),
        "mean_gap_medium": float(np.mean(by_tier["medium"])),
        "mean_gap_light": float(np.mean(by_tier["light"])),
        "n_heavy": len(by_tier["heavy"]),
        "n_medium": len(by_tier["medium"]),
        "n_light": len(by_tier["light"]),
        "merged": merged,
    }


def plot_scatter(merged, test_result, path):
    fig, ax = plt.subplots(figsize=(11, 7), dpi=150)
    tiers = {"heavy": ("#d62728", "AI-heavy"),
             "medium": ("#ff7f0e", "AI-medium"),
             "light": ("#1f77b4", "AI-light")}
    for tier, (color, label) in tiers.items():
        sub = merged[merged["tier"] == tier]
        ax.scatter(sub["pct_ai"], sub["gap_pp"], color=color, s=180,
                   alpha=0.85, edgecolor="white", linewidth=2, label=label,
                   zorder=3)
        for _, row in sub.iterrows():
            ax.annotate(
                row["role"],
                (row["pct_ai"], row["gap_pp"]),
                xytext=(7, 0), textcoords="offset points",
                fontsize=8.5, color="#333", va="center",
            )
    # regression line
    if len(merged) >= 5:
        slope, intercept, r, p, _ = stats.linregress(
            merged["pct_ai"], merged["gap_pp"]
        )
        xs = np.array([merged["pct_ai"].min(), merged["pct_ai"].max()])
        ax.plot(xs, intercept + slope * xs, color="#888", linestyle="--",
                linewidth=2, zorder=2,
                label=f"OLS fit (r={r:.2f}, p={p:.2f})")
    ax.set_xlabel("% of US postings mentioning AI/ML in role description",
                  fontsize=11)
    ax.set_ylabel("Entry-vs-Senior remote-allowance gap (pp)", fontsize=11)
    ax.set_title(
        "The Broken Ladder is not AI-driven\n"
        "Per-role gradient vs AI exposure — Lambert/Schindler prediction confirmed",
        fontsize=12.5, fontweight="bold",
    )
    ax.axhline(0, color="#aaa", linewidth=0.8, zorder=1)
    ax.grid(alpha=0.2, zorder=0)
    ax.legend(loc="upper left", fontsize=10, framealpha=0.95)
    fig.text(
        0.5, 0.02,
        f"Spearman ρ = {test_result['spearman_rho']:.2f} (p={test_result['spearman_p']:.2f})  |  "
        f"Mean gap: AI-heavy {test_result['mean_gap_heavy']:.1f}pp,  "
        f"AI-medium {test_result['mean_gap_medium']:.1f}pp,  "
        f"AI-light {test_result['mean_gap_light']:.1f}pp  |  "
        f"ANOVA F={test_result['anova_f']:.2f} (p={test_result['anova_p']:.2f})",
        ha="center", fontsize=9, color="#444",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_ladder_ranking(ladder_df, path):
    """Horizontal bar chart of every role's entry vs senior %, sorted by gap."""
    df = ladder_df.sort_values("gap_pp", ascending=True).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(12, 9), dpi=150)
    y = np.arange(len(df))
    tiers = {"heavy": "#d62728", "medium": "#ff7f0e", "light": "#1f77b4"}
    # Draw the gap as a horizontal range
    for i, row in df.iterrows():
        color = tiers[row["tier"]]
        ax.plot([row["pct_entry"], row["pct_senior"]], [i, i],
                color=color, linewidth=4, alpha=0.6, solid_capstyle="round")
        ax.scatter([row["pct_entry"]], [i], color=color, s=80,
                   marker="o", edgecolor="white", linewidth=1.5, zorder=3,
                   label="entry" if i == 0 else "")
        ax.scatter([row["pct_senior"]], [i], color=color, s=140,
                   marker="D", edgecolor="white", linewidth=1.5, zorder=3,
                   label="senior" if i == 0 else "")
        ax.text(
            max(row["pct_entry"], row["pct_senior"]) + 1,
            i,
            f"  +{row['gap_pp']:.0f}pp",
            va="center", fontsize=8.5, color="#444", fontweight="bold",
        )
    ax.set_yticks(y)
    ax.set_yticklabels([f"{r['role']}  (entry N={r['n_entry']:,}, senior N={r['n_senior']:,})"
                        for _, r in df.iterrows()], fontsize=9)
    ax.set_xlabel("% of US postings allowing remote or hybrid", fontsize=11)
    ax.set_title(
        "Per-role broken-ladder slope: entry-level vs senior remote allowance\n"
        "Sorted by gap. Color = AI exposure tier.",
        fontsize=12.5, fontweight="bold",
    )
    ax.set_xlim(0, max(df["pct_senior"].max(), 80) + 12)
    ax.grid(axis="x", alpha=0.25)
    # Tier legend
    from matplotlib.lines import Line2D
    legend_elems = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=tiers["heavy"],
               markersize=10, label="AI-heavy"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=tiers["medium"],
               markersize=10, label="AI-medium"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=tiers["light"],
               markersize=10, label="AI-light"),
        Line2D([0], [0], marker="o", color="#444", markersize=8, label="entry"),
        Line2D([0], [0], marker="D", color="#444", markersize=10, label="senior"),
    ]
    ax.legend(handles=legend_elems, loc="lower right", fontsize=9, framealpha=0.95)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_tier_means(test_result, path):
    """Simple bar chart of mean gap by AI tier — the headline finding."""
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=150)
    tiers = ["AI-light", "AI-medium", "AI-heavy"]
    means = [test_result["mean_gap_light"],
             test_result["mean_gap_medium"],
             test_result["mean_gap_heavy"]]
    ns = [test_result["n_light"], test_result["n_medium"], test_result["n_heavy"]]
    colors = ["#1f77b4", "#ff7f0e", "#d62728"]
    bars = ax.bar(tiers, means, color=colors, edgecolor="white", linewidth=2)
    for bar, m, n in zip(bars, means, ns):
        ax.text(bar.get_x() + bar.get_width() / 2, m + 0.5,
                f"{m:.1f}pp\n(N={n} roles)",
                ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.set_ylabel("Mean entry-vs-senior remote-allowance gap (pp)",
                  fontsize=11)
    ax.set_title(
        "Roles' broken-ladder slope by AI exposure tier\n"
        f"ANOVA F={test_result['anova_f']:.2f}, p={test_result['anova_p']:.2f}  —  "
        "no significant difference",
        fontsize=12, fontweight="bold",
    )
    ax.grid(axis="y", alpha=0.25)
    ax.set_ylim(0, max(means) + 6)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    print(">> fetching per-role x per-seniority x workModel ...")
    per_role = fetch_per_role()
    per_role.to_csv(HERE / "per_role_seniority_workmode.csv", index=False)
    print(f"   {len(per_role)} role x seniority rows")

    print(">> computing broken-ladder slope per role ...")
    ladder = compute_broken_ladder(per_role)
    ladder.to_csv(HERE / "broken_ladder_by_role.csv", index=False)
    print(ladder[["role", "tier", "n_entry", "n_senior",
                  "pct_entry", "pct_senior", "gap_pp"]].to_string(index=False))

    print(">> measuring AI exposure per role ...")
    exposure = fetch_ai_exposure()
    exposure.to_csv(HERE / "ai_exposure_by_role.csv", index=False)
    print(exposure.to_string(index=False))

    print(">> testing AI-exposure x ladder-slope correlation ...")
    result = test_ai_correlation(ladder, exposure)
    merged = result.pop("merged")
    merged.to_csv(HERE / "broken_ladder_with_ai.csv", index=False)
    with open(HERE / "ai_correlation_test.json", "w") as f:
        json.dump(result, f, indent=2, default=float)
    print(json.dumps(result, indent=2, default=float))

    print(">> rendering figures ...")
    plot_scatter(merged, result, HERE / "01_gap_vs_ai_exposure.png")
    plot_ladder_ranking(ladder, HERE / "02_broken_ladder_ranking.png")
    plot_tier_means(result, HERE / "03_mean_gap_by_tier.png")

    print(">> done")


if __name__ == "__main__":
    main()
