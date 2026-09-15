Remote job postings advertise 6% more than onsite ones.

That premium is fake.

Control for role and seniority and it drops to 0.5%. Remote hiring just skews senior: 19% of remote postings sit at staff level or above, against 13% onsite. The ladder pays. The work model doesn't.

But here's what didn't collapse.

We stripped out role, rung and platform, leaving only location. If remote work had unbundled pay from geography, the state named on a remote posting would stop predicting what it pays.

It predicts it just as well as onsite does.

Pass-through of a state's onsite pay premium into its remote premium: 1.44. We reject the idea that remote pay is location blind at p below 0.0001. We cannot reject that location matters exactly as much as it does onsite.

CA remote postings carry a +10.9% premium. CA onsite postings: +4.5%. Same story in WA and NY.

And the location that matters is your employer's, not yours. 64% of remote postings carry the same state as their employer's HQ, against a 33% chance baseline. Company fixed effects absorb 62% of the entire geographic gradient.

Remote work didn't detach pay from a map. It swapped one address for another.

One caveat I won't bury: our three posting sources disagree on the leftover gap. One says -2.3%, one says +0.1%, one says +5.0%, and the intervals don't overlap. So we report the bound, not a point estimate. Whatever it is, it's small.

46,873 US tech postings across AI, ML, data and software roles, March to September 2026.

If you moved somewhere cheaper to work remotely, did your pay follow your new ZIP code or your employer's?

---

First comment (keeps the link out of the body — has_link is a negative driver):

Full analysis, code and data: https://github.com/skillenai/skillenai-notebooks/tree/master/remote-pay-geography

<!-- model score
Scorer: scripts/linkedin_scoring/score.py (trained on 48 prior posts; CV R2 0.27 impressions / 0.40 engagements)

v1 baseline          : impressions 868.6  engagements 8.0
v2 +acronyms         : impressions 1018.6 engagements 9.9   (+17.3% / +23.8%)  ACCEPTED
v3 v2+exclamation    : impressions 1018.4 engagements 10.1  (-0.0% / +2.0%)    REJECTED
  -> exclamation gain sits inside model noise (MAE ~1204 impressions) and reads
     hype-y on an analytical post. Consistent with the skill's note that this
     suggestion is draft-dependent; tested rather than assumed.

Final v2 driver profile:
 predictions: {
  "impressions": {
    "predicted": 1018.6,
    "log_predicted": 6.927,
    "cv_r2": 0.268,
    "cv_mae_orig": 1204.1
  },
  "engagements": {
    "predicted": 9.9,
    "log_predicted": 2.393,
    "cv_r2": 0.402,
    "cv_mae_orig": 16.6
  },
  "followers_3d": {
    "predicted": 19.4,
    "log_predicted": 3.014,
    "cv_r2": -0.254,
    "cv_mae_orig": 9.7
  }
}
 positive   : [
  {
    "feature": "dow",
    "contrib": 0.244
  },
  {
    "feature": "followers_at_post",
    "contrib": 0.223
  },
  {
    "feature": "ends_with_question",
    "contrib": 0.191
  },
  {
    "feature": "url_in_text_count",
    "contrib": 0.175
  },
  {
    "feature": "word_count",
    "contrib": 0.17
  }
]
 negative   : [
  {
    "feature": "has_link",
    "contrib": -0.129
  },
  {
    "feature": "hour",
    "contrib": -0.085
  },
  {
    "feature": "line_count",
    "contrib": -0.083
  },
  {
    "feature": "exclamation_count",
    "contrib": -0.063
  },
  {
    "feature": "emoji_count",
    "contrib": -0.033
  }
]
-->
