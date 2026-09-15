# LinkedIn post — who-feeds-ai-roles

Attach `07_role_race.mp4` (the 74s leaderboard race). Put the blog link in the
first comment, not the body — `has_link` is a negative driver.

---

Software Engineering was 69% of all tech hiring in 1998. Today it's 41%.

We traced 568,663 career histories back to the 1990s to find where that share went. Data roles took more of it than AI did: 5% to 23%, while AI went 1% to 10%. Together they account for almost exactly what software gave up.

But the part that surprised me is what "AI and data" actually contains. Six roles, one label, and a 54x spread in how many of their people hold a PhD:

AI Researcher 32.7%. Data Scientist (DS) 16.7%. ML Engineer (MLE) 12.4%. AI Engineer (AIE) 4.9%. Data Analyst 2.2%. Data Engineer (DE) 0.6%. The tech-wide baseline is 2.7%.

The two biggest roles in that list sit at or below the baseline. Data Analyst alone is 11% of all tech hiring.

Career histories say the same thing a second way. Arrivals from academic posts range from 20.9% for AI Researcher down to 3.3% for Data Engineer, which takes 29% of its people straight from Software Engineer.

So the story that the AI boom drained the universities is half right. Academia fed Data Science and AI Research. What fed AI Engineering and Data Engineering was software.

One more: the cloud era never grew. Infrastructure held a 9-12% band for thirty years while sysadmins and network engineers were swapped for DevOps, cloud and security. AI and data expanded the pie. Cloud just redistributed it.

If you're advising someone entering this field, which of those six roles would you point them at?

---

**First comment:** Full analysis, all six roles, and the methodology:
https://skillenai.com/YYYY/MM/DD/software-was-69-of-tech-hiring-data-and-ai-took-the-rest

<!-- model score
Scorer: scripts/linkedin_scoring/score.py (trained on 48 prior posts;
CV R2 0.27 impressions / 0.40 engagements). Absolute values are noisy —
used here for relative ranking between drafts only.

  v1  baseline                        impressions 2739 | engagements 38.4
  v2  + exclamation in hook           impressions 2716 | engagements 39.1   (impressions WORSE)
  v3  + acronyms + "DATA" in caps     impressions 4680 | engagements 39.9
  v4  v3 + exclamation                impressions 4428 | engagements 38.3   (worse on both)
  v5  v3 + more acronyms              impressions 4377 | engagements 39.2   (over-tuned)
  v6  acronyms only, natural prose    impressions 4734 | engagements 44.8   <-- SHIPPED

Notes for next time:
  - The acronym parentheticals (DS/MLE/AIE/DE) drove a +73% impressions lift.
    upper_word_ratio remains the strongest single format lever.
  - Shouty ALL-CAPS ("DATA") scored WORSE than the same text with natural
    capitalisation: v3 4680/39.9 vs v6 4734/44.8. Raising upper_word_ratio by
    yelling is not the same as raising it with real acronyms.
  - The "add an exclamation" suggestion HURT this draft (-5% impressions on v4).
    Confirms it is draft-dependent; always test rather than apply.
  - Top positive n-gram was "scientist" (+0.573), consistent with the
    data-science career cluster being the author's strongest historical topic.
-->
