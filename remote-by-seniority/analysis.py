"""Generate figures + CSVs for the remote-by-seniority analysis.

Run from this directory. Requires SKILLENAI_INSIGHTS_API_KEY in env (or sourced
from skillenai-ds/.env).
"""
import json
import os
import pathlib
import sys

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

ORDER = ["intern", "entry", "mid", "senior", "staff", "principal"]
PRETTY = {
    "intern": "Intern",
    "entry": "Entry",
    "mid": "Mid",
    "senior": "Senior",
    "staff": "Staff",
    "principal": "Principal",
}


def query(body):
    r = requests.post(f"{API_URL}/v1/query/search", headers=HDR, json=body, timeout=30)
    r.raise_for_status()
    return r.json()


def fetch_overview():
    body = {
        "query": {
            "size": 0,
            "track_total_hits": True,
            "query": US_TECH_FILTER,
            "aggs": {
                "by_sen": {
                    "terms": {"field": "seniorityLevel", "size": 10},
                    "aggs": {"by_wm": {"terms": {"field": "workModel", "size": 5}}},
                }
            },
        },
        "indices": ["prod-enriched-jobs"],
    }
    d = query(body)
    rows = []
    for b in d["aggregations"]["by_sen"]["buckets"]:
        wm = {x["key"]: x["doc_count"] for x in b["by_wm"]["buckets"]}
        o = wm.get("onsite", 0)
        h = wm.get("hybrid", 0)
        r_ = wm.get("remote", 0)
        rows.append(
            {
                "seniority": b["key"],
                "n": o + h + r_,
                "onsite": o,
                "hybrid": h,
                "remote": r_,
            }
        )
    df = pd.DataFrame(rows).set_index("seniority").reindex(ORDER)
    df["pct_onsite"] = 100 * df["onsite"] / df["n"]
    df["pct_hybrid"] = 100 * df["hybrid"] / df["n"]
    df["pct_remote"] = 100 * df["remote"] / df["n"]
    df["pct_any_remote"] = df["pct_hybrid"] + df["pct_remote"]
    return df


def fetch_within_role():
    roles = [
        "Software Engineer",
        "Data Engineer",
        "Backend Engineer",
        "Machine Learning Engineer",
        "AI Engineer",
        "Data Scientist",
        "Product Manager",
        "DevOps Engineer",
        "Security Engineer",
        "Frontend Engineer",
    ]
    body = {
        "query": {
            "size": 0,
            "query": {
                "bool": {
                    "filter": US_TECH_FILTER["bool"]["filter"]
                    + [{"terms": {"role.keyword": roles}}],
                    "must_not": US_TECH_FILTER["bool"]["must_not"],
                }
            },
            "aggs": {
                "by_role": {
                    "terms": {"field": "role.keyword", "size": 15},
                    "aggs": {
                        "by_sen": {
                            "terms": {"field": "seniorityLevel", "size": 10},
                            "aggs": {
                                "by_wm": {"terms": {"field": "workModel", "size": 5}}
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
                    "pct_any_remote": 100 * (h + rm) / tot if tot else None,
                }
            )
    return pd.DataFrame(rows)


def chi_square_table(df):
    ct = df[["onsite", "hybrid", "remote"]].to_numpy()
    chi2, p, dof, exp = stats.chi2_contingency(ct)
    n = ct.sum()
    cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
    resid = (ct - exp) / np.sqrt(exp)
    return {
        "chi2": chi2,
        "p": p,
        "dof": dof,
        "cramers_v": cramers_v,
        "n": int(n),
        "resid": pd.DataFrame(
            resid, index=df.index, columns=["onsite", "hybrid", "remote"]
        ),
    }


def plot_ladder(df, path):
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)
    levels = df.index.tolist()
    pct = df["pct_any_remote"].to_numpy()
    n = df["n"].to_numpy()
    colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(levels)))
    bars = ax.bar(
        [PRETTY[l] for l in levels],
        pct,
        color=colors,
        edgecolor="white",
        linewidth=1.5,
    )
    for bar, p, nn in zip(bars, pct, n):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            p + 1,
            f"{p:.1f}%\n(N={nn:,})",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )
    ax.set_ylim(0, 75)
    ax.set_ylabel("% of postings allowing remote or hybrid", fontsize=11)
    ax.set_xlabel("Seniority level (IC ladder)", fontsize=11)
    ax.set_title(
        "Remote-or-hybrid by seniority — US tech postings (March–May 2026)",
        fontsize=13,
        pad=12,
    )
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.text(
        0.5,
        -0.02,
        "Source: Skillenai jobs index. N=50,740 US tech postings (Speechify excluded).",
        ha="center",
        fontsize=9,
        style="italic",
        color="#666",
    )
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_stacked(df, path):
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)
    levels = [PRETTY[l] for l in df.index]
    onsite = df["pct_onsite"].to_numpy()
    hybrid = df["pct_hybrid"].to_numpy()
    remote = df["pct_remote"].to_numpy()
    ax.bar(levels, remote, label="Remote", color="#2a9d8f")
    ax.bar(levels, hybrid, bottom=remote, label="Hybrid", color="#e9c46a")
    ax.bar(
        levels, onsite, bottom=remote + hybrid, label="Onsite", color="#e76f51"
    )
    # annotate "% remote" inside each bar
    for i, lev in enumerate(levels):
        ax.text(
            i,
            remote[i] / 2,
            f"{remote[i]:.0f}%",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=10,
        )
        ax.text(
            i,
            remote[i] + hybrid[i] / 2,
            f"{hybrid[i]:.0f}%",
            ha="center",
            va="center",
            color="#333",
            fontweight="bold",
            fontsize=10,
        )
        ax.text(
            i,
            remote[i] + hybrid[i] + onsite[i] / 2,
            f"{onsite[i]:.0f}%",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=10,
        )
    ax.set_ylim(0, 100)
    ax.set_ylabel("Share of postings (%)", fontsize=11)
    ax.set_xlabel("Seniority level (IC ladder)", fontsize=11)
    ax.set_title(
        "Work-mode mix by seniority — onsite shrinks as the ladder climbs",
        fontsize=13,
        pad=12,
    )
    ax.legend(loc="lower right", framealpha=0.95)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_within_role(within_df, path):
    pivot = within_df.pivot(index="role", columns="seniority", values="pct_any_remote")
    pivot = pivot.reindex(columns=ORDER)
    # only keep cells with N>=30
    n_pivot = within_df.pivot(index="role", columns="seniority", values="n").reindex(
        columns=ORDER
    )
    mask = n_pivot.fillna(0) < 30
    pivot_masked = pivot.where(~mask)
    # sort roles by max remote rate
    role_order = pivot_masked.max(axis=1).sort_values(ascending=False).index.tolist()
    pivot_masked = pivot_masked.loc[role_order]
    n_pivot = n_pivot.loc[role_order]

    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    im = ax.imshow(pivot_masked.values, aspect="auto", cmap="RdYlGn", vmin=10, vmax=75)
    ax.set_xticks(range(len(ORDER)))
    ax.set_xticklabels([PRETTY[s] for s in ORDER], fontsize=10)
    ax.set_yticks(range(len(role_order)))
    ax.set_yticklabels(role_order, fontsize=10)
    for i in range(len(role_order)):
        for j in range(len(ORDER)):
            v = pivot_masked.values[i, j]
            n = n_pivot.values[i, j]
            if pd.isna(v):
                ax.text(j, i, "N<30", ha="center", va="center", color="#888", fontsize=8)
            else:
                ax.text(
                    j,
                    i,
                    f"{v:.0f}%\nN={int(n) if not pd.isna(n) else 0}",
                    ha="center",
                    va="center",
                    color="black",
                    fontsize=8,
                    fontweight="bold",
                )
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.set_label("% any-remote (remote + hybrid)", fontsize=10)
    ax.set_title(
        "Within-role: the seniority remote gap holds in every tech role",
        fontsize=13,
        pad=12,
    )
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def fetch_robustness():
    body = {
        "query": {
            "size": 0,
            "query": {
                "bool": {
                    "filter": US_TECH_FILTER["bool"]["filter"],
                    "must_not": US_TECH_FILTER["bool"]["must_not"]
                    + [
                        {
                            "terms": {
                                "companyCanonicalName.keyword": [
                                    "SpaceX",
                                    "Anduril",
                                    "andurilindustries",
                                    "Raytheon",
                                    "Lockheed Martin",
                                    "Northrop Grumman",
                                    "Boeing",
                                    "Internal Postings",
                                    "Confidential",
                                    "Johns Hopkins Applied Physics Laboratory",
                                    "agency",
                                ]
                            }
                        }
                    ],
                }
            },
            "aggs": {
                "by_sen": {
                    "terms": {"field": "seniorityLevel", "size": 10},
                    "aggs": {"by_wm": {"terms": {"field": "workModel", "size": 5}}},
                }
            },
        },
        "indices": ["prod-enriched-jobs"],
    }
    d = query(body)
    rows = []
    for b in d["aggregations"]["by_sen"]["buckets"]:
        wm = {x["key"]: x["doc_count"] for x in b["by_wm"]["buckets"]}
        o = wm.get("onsite", 0)
        h = wm.get("hybrid", 0)
        r_ = wm.get("remote", 0)
        rows.append(
            {
                "seniority": b["key"],
                "n": o + h + r_,
                "pct_any_remote": 100 * (h + r_) / (o + h + r_) if (o + h + r_) else 0,
            }
        )
    return pd.DataFrame(rows).set_index("seniority").reindex(ORDER)


def main():
    print("Fetching overview...")
    overview = fetch_overview()
    overview.to_csv(HERE / "overview_by_seniority.csv")
    print(overview)

    print("\nChi-square test...")
    stats_out = chi_square_table(overview)
    print(
        f"chi2={stats_out['chi2']:.1f} dof={stats_out['dof']} p={stats_out['p']:.3e} "
        f"V={stats_out['cramers_v']:.4f} N={stats_out['n']:,}"
    )
    print("\nStandardized residuals:")
    print(stats_out["resid"].round(1))
    stats_out["resid"].to_csv(HERE / "standardized_residuals.csv")
    with open(HERE / "chi_square_stats.json", "w") as f:
        json.dump(
            {
                "chi2": stats_out["chi2"],
                "p": stats_out["p"],
                "dof": stats_out["dof"],
                "cramers_v": stats_out["cramers_v"],
                "n": stats_out["n"],
            },
            f,
            indent=2,
        )

    print("\nFetching within-role...")
    within = fetch_within_role()
    within.to_csv(HERE / "within_role.csv", index=False)

    print("Fetching robustness slice (no defense/hardware)...")
    rob = fetch_robustness()
    rob.to_csv(HERE / "robustness_no_defense.csv")
    print(rob)

    print("\nRendering figures...")
    plot_ladder(overview, HERE / "01_ladder_any_remote.png")
    plot_stacked(overview, HERE / "02_workmode_mix.png")
    plot_within_role(within, HERE / "03_within_role_heatmap.png")
    print("Done.")


if __name__ == "__main__":
    main()
