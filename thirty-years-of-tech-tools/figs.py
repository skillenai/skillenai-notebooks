"""Static figures for the thirty-years-of-tech-tools analysis.

02  when a technology peaked vs how much of that peak it still holds
03  fall rate at a FIXED 20-quarter follow-up, by era (censoring-safe)
04  quarters from a quarter of peak to peak -- adoption speed, LLMs marked

Header spacing is set per-figure in INCHES rather than using brand.header's
figure-fraction default, which collapses onto the title on short figures.
"""
import json, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, "/Users/jrand/git-repos/skillenai-notebooks/tech-role-pay-2026")
import brand  # noqa: F401
from brand import BG, INK, GRID, MUTE, header, footer, stamp, save

W = json.load(open("/Users/jrand/git-repos/skillenai-ds/work/skill-race/_out/waves.json"))
QS = [tuple(q) for q in W["quarters"]]
QI = {f"{y}Q{m//3}": i for i, (y, m) in enumerate(QS)}
ROWS = W["lifecycle"]
LAST = len(QS) - 1

CY, GR, AM, VI = "#22C1DA", "#1BA36B", "#E9A23B", "#7A3FD1"
RED = "#D64545"


def qx(pq):
    y, q = pq.split("Q")
    return int(y) + (int(q) - 1) * 0.25


def hdr(fig, H, title, sub, y=0.995):
    """Title + subtitle with a gap sized in inches, not figure fraction."""
    header(fig, title, sub, y=y, dy=0.34 / H, ts=16.0, ss=9.7)


# ---------------------------------------------------------------- 02
def fig_peak_vs_survival():
    H = 6.9
    fig, ax = plt.subplots(figsize=(11.8, H))
    xs = [qx(r["peak_q"]) for r in ROWS]
    ys = [100 * r["rel_now"] for r in ROWS]
    cols = [RED if y < 15 else (AM if y < 50 else GR) for y in ys]
    mx = max(r["peak"] for r in ROWS)
    sz = [24 + 820 * r["peak"] / mx for r in ROWS]
    ax.scatter(xs, ys, s=sz, c=cols, alpha=.70, linewidths=0, zorder=3)
    ax.axhline(50, color=GRID, lw=1.1, ls="--", zorder=0)
    ax.text(2025.9, 51.5, "half of peak", fontsize=8.4, color=MUTE,
            va="bottom", ha="right")

    # Labels placed in DATA coordinates with leader lines. The pre-2002 cluster
    # is far too dense to label in place, so those labels are fanned out to the
    # left and below and joined to their dot by a thin line.
    LAB = {
        "Novell":       (1995.7, 24.0), "Windows NT": (1995.7, 18.0),
        "Delphi":       (1995.7, 12.5), "MS Access":  (1995.7, 7.0),
        "PowerBuilder": (1995.7, 1.5),
        "COBOL":        (2001.4, 24.5), "Visual Basic": (2003.0, 19.0),
        "Unix":         (2001.4, 30.0), "Perl":       (2004.4, 13.5),
        "ASP":          (2004.4, 7.5),  "Oracle":     (2002.6, 8.0),
        "Java":         (2001.6, 55.0), "HTML":       (2003.4, 43.0),
        "Linux":        (2003.4, 36.0),
        "C#":           (2009.6, 33.0), "PHP":        (2009.6, 19.0),
        "jQuery":       (2013.6, 9.0),
        "Python":       (2021.2, 99.0), "SQL":        (2021.2, 91.5),
        "React":        (2020.0, 84.0), "Excel":      (2025.3, 78.0),
        "AWS":          (2019.2, 74.0), "Docker":     (2025.3, 68.5),
        "LLMs":         (2022.6, 62.0),
    }
    for r in ROWS:
        if r["skill"] not in LAB:
            continue
        tx, ty = LAB[r["skill"]]
        px, py = qx(r["peak_q"]), 100 * r["rel_now"]
        ha = "right" if tx > px else "left"
        ax.annotate(r["skill"], xy=(px, py), xytext=(tx, ty),
                    fontsize=8.7, weight="semibold", color=INK,
                    ha=ha, va="center", zorder=5,
                    arrowprops=dict(arrowstyle="-", color=MUTE, lw=.6,
                                    shrinkA=2, shrinkB=3, alpha=.8))

    ax.set_xlim(1994.6, 2026.6)
    ax.set_ylim(-5, 108)
    ax.set_ylabel("Current share as % of its own peak", fontsize=9.8, color=INK)
    ax.set_xlabel("Quarter the technology peaked", fontsize=9.8, color=MUTE)
    ax.set_xticks([1996, 2000, 2005, 2010, 2015, 2020, 2025])
    ax.set_xticklabels(["1996", "2000", "2005", "2010", "2015", "2020", "2025"])
    ax.grid(axis="y", color=GRID, alpha=.7, lw=.7)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)
    top, bot = 1 - 1.18 / H, 0.80 / H
    fig.tight_layout(rect=[0, bot, 1, top])
    hdr(fig, H, "Everything that peaked before 2002 is effectively gone",
        "100 named technologies; dot size is peak share of jobs. Not one of the 28 that peaked before 2002 "
        "still holds half its peak - Java comes closest at 48%,\nand ASP, Novell, Windows NT and Delphi hold none of it. "
        "All 56 that peaked after 2019 still hold at least 46%.")
    footer(fig, "Skillenai talent graph - 633,386 dated job positions from 178,469 people, 1996-2025. "
                "Share = jobs started in a trailing 12-month window naming the technology. "
                "Current = the window ending 2025Q3.", y=bot - 0.075)
    stamp(fig, x=.905, y=.004, h=.034)
    save(fig, "02_peak_vs_survival.png")


# ---------------------------------------------------------------- 03
def fig_fall_rate():
    """Two bands, matching the Fisher test exactly.

    A finer split was tried and abandoned: 2002-2007 holds only 3 technologies,
    and a 0% bar off n=3 reads as a finding when it is an empty cell.
    """
    elig = [r for r in ROWS if QI[r["peak_q"]] + 20 <= LAST]
    bands = [("peaked 1996-2007", 1996, 2007), ("peaked 2008-2020", 2008, 2020)]
    labs, vals, ns = [], [], []
    for lab, lo, hi in bands:
        g = [r for r in elig if lo <= r["peak_year"] <= hi]
        fell = sum(1 for r in g if (not r["censored"]) and r["fall_q"] <= 20)
        labs.append(lab)
        vals.append(100 * fell / len(g))
        ns.append((fell, len(g)))
    H = 5.2
    fig, ax = plt.subplots(figsize=(8.0, H))
    ax.bar(labs, vals, color=[RED, GR], width=.52)
    for i, (v, (f, n)) in enumerate(zip(vals, ns)):
        ax.text(i, v + 1.6, f"{v:.0f}%", ha="center", fontsize=22,
                weight="bold", color=INK)
        ax.text(i, v / 2, f"{f} of {n}", ha="center", va="center",
                fontsize=10.5, color=BG, weight="semibold")
    ax.set_ylim(0, max(vals) * 1.34)
    ax.set_ylabel("Fell below half their peak\nwithin 5 years of it",
                  fontsize=9.6, color=INK, linespacing=1.5)
    ax.grid(axis="y", color=GRID, alpha=.7, lw=.7)
    ax.set_axisbelow(True)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)
    ax.set_xticklabels(labs, fontsize=10.5, color=INK)
    top, bot = 1 - 1.30 / H, 0.86 / H
    fig.tight_layout(rect=[0.02, bot, 1, top])
    hdr(fig, H, "The churn stopped",
        "Every technology is given exactly 20 quarters after its own peak, so a recent\n"
        "arrival is not scored as a survivor merely for being young. "
        "Fisher exact p=0.025,\nodds ratio 6.6.")
    footer(fig, "49 named technologies that peaked early enough to have five years of follow-up. "
                "Those peaking after 2020Q3 are excluded.", y=bot - 0.115)
    stamp(fig, x=.855, y=.004, h=.046)
    save(fig, "03_fall_rate.png")


# ---------------------------------------------------------------- 04
def fig_rise_speed():
    # Technologies already rising when the data begins are excluded: their rise
    # is cut off by the window, not by how fast anyone adopted them.
    ok = [r for r in ROWS if QI[r["peak_q"]] - r["rise_q"] >= 8]
    rises = sorted(r["rise_q"] for r in ok)
    med = float(np.median(rises))
    llm = next(r for r in ROWS if r["skill"] == "LLMs")
    H = 5.5
    fig, ax = plt.subplots(figsize=(10.4, H))
    ax.hist(rises, bins=range(0, max(rises) + 5, 4), color=CY, alpha=.85,
            edgecolor=BG, linewidth=1.2)
    ymax = ax.get_ylim()[1]
    ax.axvline(med, color=INK, lw=1.4, ls="--")
    ax.text(med + 1.4, ymax * .93, f"median\n{med:.0f} quarters", fontsize=9.2,
            color=INK, weight="semibold", va="top")
    ax.axvline(llm["rise_q"], color=RED, lw=2.4)
    ax.text(llm["rise_q"] + 1.4, ymax * .62, f"LLMs\n{llm['rise_q']} quarters",
            fontsize=10.4, color=RED, weight="bold", va="top")
    ax.set_xlabel("Quarters from a quarter of peak share to peak share",
                  fontsize=9.6, color=MUTE)
    ax.set_ylabel("Technologies", fontsize=9.6, color=INK)
    ax.grid(axis="y", color=GRID, alpha=.7, lw=.7)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)
    top, bot = 1 - 1.26 / H, 0.92 / H
    fig.tight_layout(rect=[0, bot, 1, top])
    hdr(fig, H, "LLMs climbed faster than anything else we can time",
        f"Adoption speed for the {len(ok)} named technologies whose entire rise happens inside "
        "the window. The median took 31 quarters,\nalmost eight years. LLMs took nine. "
        "The next fastest is XML at 11.")
    footer(fig, "36 technologies - Java, Linux, HTML, SQL and others - were already established "
                "in 1996 and are excluded, because their rise began before the data does. "
                "They are not known to be slower.", y=bot - 0.10)
    stamp(fig, x=.888, y=.004, h=.043)
    save(fig, "04_rise_speed.png")


if __name__ == "__main__":
    fig_peak_vs_survival()
    fig_fall_rate()
    fig_rise_speed()
