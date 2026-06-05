The customer-facing layer in AI is 5× thicker than it was in cloud.

I dropped this comment on Andrew Ng's recent Forward Deployed Engineer (FDE) post: "FDEs from frontier labs are to AI Engineers what Solutions Architects from cloud providers were to Software Engineers." Then I tested it against 44,000 job postings.

The FDE-to-AIE ratio is 29.2%. The SA-to-SWE ratio ran at 5.7%. For every 100 AI Engineer postings the market is hiring ~29 FDEs — 5× the cloud-era SA/SWE rate. MIT's NANDA Initiative just reported 95% of enterprise AI pilots produce zero P&L impact, not because of the models but because of deployment. The market is pricing that into role counts.

The skill mix validates the analogy in detail. FDE postings ask for LLMs, RAG, agents, and production AI at AIE-like intensity (3-10× SA). They ask for stakeholder management and customer success at SA-like intensity — statistically indistinguishable from SA on both, p > 0.10. The one place FDE diverges from SA is the formal pre-sales motion (13% vs 36%). SAs sell, FDEs implement. So FDE is the post-sales technical embed: the customer-success and consulting halves of SA, minus the formal pre-sales motion, plus the LLM stack of AIE.

Twist: the role has already diffused beyond frontier labs — and the entry rung looks hype-rebranded. Top FDE employers are Databricks, Parloa, OpenAI, Workato, Anthropic, Chalk, GitLab. FDE entry-share averages 13.9%, above my 10% "tech entry door" threshold from yesterday. But the average hides a tier split: frontier labs 6.5%, everyone else 14.4%. OpenAI and Anthropic combined have zero entry-level FDE postings. Chalk alone has 16. Smaller startups are using "Forward Deployed Engineer" to relabel early-career customer-engineering — the same pattern SA postings showed in 2009-2012 before the role settled into a senior-only steady state.

Full analysis with 30 skill comparisons and chi-square tests in comments.

Frontier-lab FDE or diffusion-tier FDE — which are you seeing more of?


<!-- model score (v3 final, picked after 3 iterations)
{
    "predictions": {
        "impressions": {
            "predicted": 2096.8,
            "log_predicted": 7.649,
            "cv_r2": 0.268,
            "cv_mae_orig": 1204.1
        },
        "engagements": {
            "predicted": 29.0,
            "log_predicted": 3.4,
            "cv_r2": 0.402,
            "cv_mae_orig": 16.6
        },
        "followers_3d": {
            "predicted": 14.4,
            "log_predicted": 2.732,
            "cv_r2": -0.254,
            "cv_mae_orig": 9.7
        }
    },
    "drivers": {
        "numeric_positive": [
            {
                "feature": "upper_word_ratio",
                "contrib": 0.579
            },
            {
                "feature": "dow",
                "contrib": 0.244
            },
            {
                "feature": "followers_at_post",
                "contrib": 0.223
            },
            {
                "feature": "word_count",
                "contrib": 0.222
            },
            {
                "feature": "ends_with_question",
                "contrib": 0.191
            }
        ],
        "numeric_negative": [
            {
                "feature": "has_link",
                "contrib": -0.129
            },
            {
                "feature": "hour",
                "contrib": -0.085
            },
            {
                "feature": "exclamation_count",
                "contrib": -0.063
            },
            {
                "feature": "emoji_count",
                "contrib": -0.033
            },
            {
                "feature": "question_count",
                "contrib": -0.01
            }
        ],
        "text_positive": [],
        "text_negative": []
    },
    "suggestions": [
        "Add an exclamation in the hook line \u2014 exclamation_count was a small positive driver."
    ],
    "draft_metadata": {
        "has_image": false,
        "has_video": false,
        "has_link": false,
        "dow": -1,
        "hour": -1,
        "followers_at_post": 3609
    }
}

-->

<!-- v1: imp=1984, eng=25.9, fol=18.8
     v2: imp=1974, eng=26.9, fol=15.5  (tightened bullets to prose)
     v3: imp=2097, eng=29.0, fol=14.4  (punchier hook with 5x number) FINAL -->
