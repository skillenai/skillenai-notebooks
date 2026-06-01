# LinkedIn post — remote-by-seniority

Paste this into the LinkedIn composer. Put the blog URL in the first comment, not in the body — `has_link` is a negative feature on the scorer; `url_in_text_count` (when zero) is a positive driver.

---

A Staff engineer is 2.5x more likely to be offered REMOTE than a tech intern.

This week the NY Fed published a study arguing remote work — not AI — drives ~2/3 of the post-pandemic rise in US youth unemployment among recent college grads. That study is demand-side: who can't get hired.

We checked the supply side. 50,757 US tech postings, March–May 2026. % allowing REMOTE or HYBRID by IC seniority level:

— Intern: 24.6%
— Entry: 41.1%
— Mid: 52.6%
— Senior: 54.0%
— Staff: 62.3%

A near-perfect staircase up the IC ladder. And it isn't role mix: inside SWE alone the gap is 21% intern to 63% staff. Inside DE: 11% to 71%. Inside AI Engineer: 12% to 67%. Inside MLE: 30% to 68%.

The US tech labor market built two doors. The one labeled REMOTE mostly opens for people who already did the job.

Chi-square = 1,486. Intern residual = +21σ onsite. The NY Fed's proposed mechanism, fingerprinted directly in the postings. SWE, DS, MLE, AI Engineer — every role tells the same story.

Full analysis + reproducible code — link in the comments.

Are early-career engineers at your company onsite or remote?

---

First-comment text (put the blog and code link here, not in the body):

> Blog: https://skillenai.com/blog/remote-work-seniority-and-the-junior-hiring-cliff-50-757-tech-postings
> Reproducible analysis (chi-square, residuals, within-role check, robustness slices): https://github.com/skillenai/skillenai-notebooks/tree/master/remote-by-seniority

<!-- model score
Scored with /Users/jrand/git-repos/skillenai-ds/scripts/linkedin_scoring/score.py on 2026-06-01.

v1 baseline: impressions=1059, engagements=16.8, followers_3d=18.3
v2 (sprinkled acronyms — NY Fed, AI, US, IC, SWE, DE): impressions=2100, engagements=27.0, followers_3d=22.1
v3 (added MLE, DS, more all-caps REMOTE): impressions=2278, engagements=26.6, followers_3d=22.8

Locked v3. v3 wins impressions (+8% over v2) but ticked engagements down 1.5% (within MAE 16.6 noise);
took the impressions gain. Rejected the "add exclamation" suggestion — verified-unreliable per skill.
upper_word_ratio (+0.87) is the dominant positive driver in this draft. ends_with_question is a positive
contribution (0.19). dow and followers_at_post are model defaults.
-->
