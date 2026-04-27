"""Charts for OpenAI Consumer Devices analysis."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})

# Chart 1: Where OpenAI's mobile/OS engineers actually sit
fig, ax = plt.subplots(figsize=(10, 5.5))
teams = [
    ("ChatGPT Mobile Infra", 2, "#9aa0a6"),
    ("Monetization", 3, "#9aa0a6"),
    ("ChatGPT Engineering", 2, "#9aa0a6"),
    ("Applied Foundations", 2, "#9aa0a6"),
    ("Social Products", 1, "#9aa0a6"),
    ("Consumer Devices (custom OS / embedded)", 5, "#0aa64a"),
]
labels = [t[0] for t in teams]
counts = [t[1] for t in teams]
colors = [t[2] for t in teams]
y = list(range(len(teams)))
ax.barh(y, counts, color=colors, edgecolor="black", linewidth=0.6)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel("Open postings (Mar–Apr 2026)")
ax.set_title("OpenAI: where the 'mobile' and 'OS' engineers actually sit\n10 Android/iOS roles → ChatGPT app  •  5 OS/embedded roles → Consumer Devices",
             loc="left", fontsize=12, fontweight="bold")
for i, c in enumerate(counts):
    ax.text(c + 0.08, i, str(c), va="center", fontsize=11)
grey = mpatches.Patch(color="#9aa0a6", label="ChatGPT app teams")
green = mpatches.Patch(color="#0aa64a", label="Consumer Devices (hardware)")
ax.legend(handles=[grey, green], loc="lower right", frameon=False)
plt.tight_layout()
plt.savefig("/Users/jrand/git-repos/skillenai-notebooks-openai-phone/openai-phone/team-mapping.png", dpi=150, bbox_inches="tight")
plt.close()

# Chart 2: Consumer Devices team composition (19 roles)
fig, ax = plt.subplots(figsize=(10, 6))
roles = [
    ("Software Engineer (general)", 6),
    ("Research Engineer/Scientist", 4),
    ("Embedded SWE", 2),
    ("OS / System Software Eng.", 2),
    ("Camera ISP Eng.", 1),
    ("Sensing Eng.", 1),
    ("Backend Eng.", 1),
    ("Full-Stack Eng.", 1),
    ("Release Eng.", 1),
]
labels = [r[0] for r in roles]
counts = [r[1] for r in roles]
y = list(range(len(roles)))
ax.barh(y, counts, color="#0aa64a", edgecolor="black", linewidth=0.6)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel("Open Consumer Devices postings (n=19)")
ax.set_title("OpenAI's 'Consumer Devices' team composition\nIndustrial design + custom silicon + embedded systems + on-device research",
             loc="left", fontsize=12, fontweight="bold")
for i, c in enumerate(counts):
    ax.text(c + 0.08, i, str(c), va="center", fontsize=11)
plt.tight_layout()
plt.savefig("/Users/jrand/git-repos/skillenai-notebooks-openai-phone/openai-phone/team-composition.png", dpi=150, bbox_inches="tight")
plt.close()

# Chart 3: Phrase-frequency dipstick — Android signal vs. custom-OS signal
fig, ax = plt.subplots(figsize=(10, 5.5))
phrases = [
    ("AOSP", 0, "#d62728"),
    ("'Android Open Source'", 0, "#d62728"),
    ("antenna", 1, "#d62728"),
    ("RF", 1, "#d62728"),
    ("'industrial design'", 1, "#0aa64a"),
    ("'custom silicon'", 3, "#0aa64a"),
    ("wireless", 4, "#0aa64a"),
    ("battery", 5, "#0aa64a"),
    ("'consumer products'", 5, "#0aa64a"),
    ("thermal", 6, "#0aa64a"),
    ("'secure boot'", 7, "#0aa64a"),
    ("audio", 8, "#0aa64a"),
    ("mechanical", 8, "#0aa64a"),
    ("kernel", 27, "#0aa64a"),
    ("Linux", 29, "#0aa64a"),
    ("embedded", 33, "#0aa64a"),
]
labels = [p[0] for p in phrases]
counts = [p[1] for p in phrases]
colors = [p[2] for p in phrases]
y = list(range(len(phrases)))
ax.barh(y, counts, color=colors, edgecolor="black", linewidth=0.5)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel("Postings mentioning the phrase (out of 746)")
ax.set_title("OpenAI is hiring for a custom Linux-based device, not an Android fork\nAOSP / antenna / RF mentions are near zero. Kernel / embedded / Linux dominate.",
             loc="left", fontsize=12, fontweight="bold")
for i, c in enumerate(counts):
    ax.text(c + 0.4, i, str(c), va="center", fontsize=10)
red = mpatches.Patch(color="#d62728", label="Phone-radio / Android signal")
green = mpatches.Patch(color="#0aa64a", label="Custom-device signal")
ax.legend(handles=[red, green], loc="lower right", frameon=False)
plt.tight_layout()
plt.savefig("/Users/jrand/git-repos/skillenai-notebooks-openai-phone/openai-phone/phrase-evidence.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts written.")
