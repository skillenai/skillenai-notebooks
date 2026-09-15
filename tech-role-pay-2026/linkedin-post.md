Which tech role pays the best in 2026?

We measured 62,805 US job postings that disclose a salary range. The answer is ML and AI research roles: Research Scientist at $215K and ML Engineer at $209K at the senior rung, with AI Engineer fourth at $198K.

Now the part that should actually change what you do. The gap between an ML Engineer and a plain Software Engineer is $16K. The gap between a mid-level and a staff-level engineer doing the same job is $65K. One rung is worth three role switches.

The ML premium is real, to be clear. Across the 37 employers that post both roles at the senior rung, ML Engineer pays more at 25 of them — same companies, same level. It's just small.

Three things surprised us. The top of the board is compressed: ranks 1 through 13 span $215K to $180K, so most of the engineering market sits inside a $35K band, and the top two roles aren't statistically separable from each other at all. The real cliffs are below the engineering tier, and there are two of them — QA and SDET engineers sit $46K below Software Engineer at the same rung, Data Analysts $63K below, and no engineer-versus-engineer gap comes close (DS vs SWE is $18K, a quarter of the QA gap). And the advice inverts by tier: if you're a mid-level engineer the promotion is the whole game, but if you're in QA or an analyst role the tier boundary is worth $46K to $86K, far more than any promotion inside it.

Of four factors setting your pay, the job title explains the least: seniority rung 0.263, employer 0.224, US state 0.186, role label 0.149. A posting in Florida advertises 33% less than the same role and rung in California.

We also threw out eight job titles. Our first leaderboard was topped by Research Engineer at $260K, until we noticed 27% of those postings came from one employer — drop them and it's $220K. When 85% of "Mission Software Engineer" postings trace to a single defense manufacturer, that title is one company's internal ladder, not a market rate. We dropped "Test Engineer" too: its top skill term is manufacturing at 26% against Selenium at 7%, so it reads like software QA and isn't.

Full breakdown, all 26 roles, methodology in the comments.

What would move your pay more this year: the title, or the rung?

<!-- model score
Scorer: scripts/linkedin_scoring/score.py (trained on 48 of the author's own posts)
CV R2: impressions 0.268 (MAE ~1,204), engagements 0.402, followers_3d -0.254 (unreliable, not cited)

v1  baseline, 14 blocks                    7,808 / 35.9
v2  consolidated to 10 blocks              7,800 / 37.6   best scorer, but now FACTUALLY STALE
v3  + "The answer surprised us!" hook      7,195 / 37.6   reverted (-7.8% imp)
v4  + exclamation only, no new words       7,491 / 37.7   reverted (-4.0% imp); isolates that the
                                                          punctuation itself costs ~4%, independent
                                                          of v3's wording change
--- QA/SDET correction required a rewrite ---
v5  full rewrite w/ QA cliff + method note 6,324 / 37.7
v6  v5 with the method note trimmed        6,357 / 38.0   trim did not recover it, so length is not
                                                          the driver
v7  MINIMAL edit to v2: QA folded into     6,945 / 37.7   ACCEPTED
    the existing consolidated paragraph

Accepted v7 over the higher-scoring v2 because v2 is wrong: it claims one cliff (analyst) when there
are two (QA -$46K, analyst -$63K) and carries the pre-correction R2 values. The 855-impression gap
is inside the model's own MAE, so the trade is accuracy for noise.

Top positive drivers in v7: upper_word_ratio (ML, AI, DS, SWE, QA, SDET acronyms), word_count,
ends_with_question, ngram "scientist".
Link stays out of the body; goes in the first comment.
-->
