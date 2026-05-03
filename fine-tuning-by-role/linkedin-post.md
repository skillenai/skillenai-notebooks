# LinkedIn Post — Fine-Tuning by Role

## Final draft (v3 — accept)

```
AI Engineers mention fine-tuning in 26% of job postings. ML Engineers mention it in 18%. But which group is actually doing the deep technical work?

We pulled 6,802 postings — DS, MLE, AIE — from March-May 2026 and looked at what "fine-tuning" actually means inside each role.

The split is sharp.

When an AI Engineer posting mentions fine-tuning, it co-mentions:
• RAG: 61%
• Prompt engineering: 41%
• LangChain: 34%
• LoRA / distillation / post-training: 7% / 5% / 5%

When an ML Engineer posting mentions fine-tuning, it co-mentions:
• Distillation: 12%
• LoRA: 9%
• RLHF: 8%
• Post-training: 7%
• RAG: 28% (less than half the AIE rate)

AI Engineers pair "fine-tuning" with the LLM-orchestration stack — RAG, LangChain, vector DBs, prompt engineering. ML Engineers pair it with the deep training toolkit — distillation, RLHF, LoRA, post-training.

Cleanest summary: AI Engineers fine-tune the API. ML Engineers fine-tune the model.

The "fine-tuning is making a comeback" narrative is real, but it's a comeback for ML Engineers, not AI Engineers. The role that captured the word is not the role that captured the substance.

If you're an AI Engineer who wants to deepen — the postings that pair fine-tuning with LoRA, RLHF, distillation, and post-training are mostly titled ML Engineer, not AI Engineer.

Where does that put you?

Full analysis with chi-square tests + 95% CIs in the first comment.
```

**First comment to add manually:**

```
Methodology + reproduction code: https://github.com/skillenai/skillenai-notebooks/tree/master/fine-tuning-by-role
```

<!-- model score
v1 (URL inline, longer): impressions 4,752 / engagements 40 / followers_3d 22
v2 (URL moved to first comment): impressions 5,023 / engagements 37 / followers_3d 23
v3 (tighter, fewer lines): impressions 5,100 / engagements 37 / followers_3d 23

Stopped at v3 — gain over v2 was <2% (1.5% impressions, no change on engagement/followers).

Strongest positive driver in this draft: upper_word_ratio (the abundance of acronyms — AI, ML, DS, MLE, AIE, RAG, LoRA, RLHF, PEFT — is the single largest predictor at +0.74 for log-impressions).
Strongest negative driver remaining: line_count.
Skipped suggestion: "Add an exclamation in the hook" — model also flags exclamation_count as a small NEGATIVE numeric driver (-0.063), so the suggestion contradicts the trained coefficients on this draft.

Model performance for context: log-target CV R² ≈ 0.27 / 0.40 / -0.25 for impressions / engagements / followers_3d. Use for relative ranking between drafts, not absolute predictions.
-->
