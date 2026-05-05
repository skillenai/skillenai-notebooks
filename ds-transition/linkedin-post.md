# LinkedIn post — DS Transition

## Final draft (v3 — accept)

```
A Senior Data Scientist deciding what to do next is told the answer is AI Engineer. Measured by skill-stack overlap across thousands of job postings, AI Engineer is the longest jump on the board.

We pulled DS, MLE, AIE, Applied Scientist, Research Scientist, and Research Engineer postings, then measured top-30 skill overlap with Data Scientist (Jaccard):

→ Applied Scientist (no Amazon): 0.333
→ ML Engineer: 0.277
→ ML Engineer, Applied/Research wing: 0.224
→ ML Engineer, Platform/Infra wing: 0.176
→ AI Engineer: 0.154

Roles built around training models share the most stack with DS. Roles built around orchestrating LLMs share the least.

ML Engineer turned out to be two jobs hiding under one title:

→ Applied/Research/Training/Foundation (218 postings): PyTorch 46%, distributed training 18%, fine-tuning 16%, JAX 14%, RL 13%.
→ Platform/Infrastructure/Inference (147 postings): Kubernetes 18%, Docker 15%, Terraform 10%, observability 14%, Go 7%.

The Applied wing trains models. The Platform wing operates them. Only the first is a natural DS destination.

The DS to AI Engineer narrative is real, but the geometry is backwards. The closest training-flavored destinations already have names: Applied Scientist, ML Engineer (Applied), Research Engineer.

Full analysis in the first comment.

Which side of the stack are you closest to?
```

**First comment to add manually:**

```
Methodology + reproduction code: https://github.com/skillenai/skillenai-notebooks/tree/ds-transition/ds-transition

Skillenai blog version: https://skillenai.com/blog/ai-engineer-is-the-longest-jump-from-data-scientist-skill-stack-map (after publish)
```

<!-- model score
v1 (longer setup, "We pulled the skill profiles for..."):  imp=7,454  eng=43.3  fol=27.0
v2 (tighter, dropped the "Most-discussed career move" framing):  imp=7,144  eng=44.5  fol=26.3
v3 (FINAL — anchored hook on Senior DS protagonist, "told the answer is AI Engineer"):  imp=7,557  eng=46.4  fol=25.9

v3 over v1: +1.4% impressions, +7% engagements. Small follower-3d cost (-4%) is acceptable.
Skipped suggestion: "Add an exclamation in the hook" — model also flags exclamation_count as a small NEGATIVE numeric driver in this draft, and the SKILL.md guidance from 2026-05-03 verifies the suggestion is unreliable.

Strongest n-gram driver: 'scientist' (+0.998). 'data' positive but weak. The post leans heavily on the AI/DS/MLE/AIE/RAG/RL/JAX acronym density which lifts upper_word_ratio (the single strongest positive feature in the model).

Model performance: log-target CV R² ≈ 0.27 / 0.40 / -0.25 for impressions / engagements / followers_3d. Use for relative ranking; absolute predictions are noisy (the python-rules post predicted 4,235 impressions and got 313).
-->
