**Short answer: the line "this is not a research role" shows up in fewer than 3% of AI Engineer job ads, it carries no pay premium once you compare jobs at the same company, and the ads that use it ask for evaluation work at least as often as the ads that don't. The phrase that does carry a premium is the evaluation work itself.**

If you work in data science or ML, you have seen some version of this in a job ad:

> "This is not a research role. This is not a 'play with models in a lab' role. This is a builder role."

> "Production AI shipping experience, not just research, POCs, demos, or internal experiments."

One posting put it under the heading *You Might Not Be a Fit If*: "Your experience is limited to experimentation without production systems."

Read enough of these and it is easy to conclude that the market has turned on research, and that the safe move is to scrub it from your résumé and lead with "shipped to production." We checked that against **62,659 US tech job postings** from **8,728 employers**. It doesn't hold up.

## How common is it?

![Share of US tech postings that disclaim research versus those that name research, evals or experimentation as part of the job](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/22/e955cb79-d6bf-4b65-9c50-5facd727e73f/Eu4XfJq4zUE-01-who-disclaims-research.png)

| Role family | Ads that disclaim research | Ads that name research, evals or experimentation as the job |
|---|---:|---:|
| AI Engineer | **2.7%** | **43.3%** |
| ML Engineer | 1.9% | 43.4% |
| Data Scientist | 1.0% | 32.3% |
| Research / Applied Scientist | 0.8% | 73.2% |
| Data Engineer | 0.2% | 6.4% |
| Data Analyst | 0.0% | 8.5% |
| Software Engineer | 0.5% | 8.1% |

The impression that this is an AI-hiring habit is correct. An AI Engineer ad is about five times as likely as a software engineering ad to carry the line. But it is still a small habit. Across all US tech postings it appears in 0.7% of ads, and only **2.1% of employers** have written it even once.

For every AI Engineer ad that says the job isn't research, about 16 describe research, evaluation or experimentation as part of the job.

A few checks, since prevalence numbers are easy to inflate:

- **Longer ads mention more of everything.** Adjusting every role to the same mix of ad lengths moves AI Engineer from 2.74% to 2.66%.
- **Some companies post the same text dozens of times.** The 439 ads with the line come from 179 employers, and no single employer accounts for more than 13% of them.

## Does it pay?

![Advertised pay effect of each phrase, raw versus compared within the same employer](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/22/e955cb79-d6bf-4b65-9c50-5facd727e73f/E5nL-Uj1eN8-02-what-the-words-are-worth.png)

At first glance, yes. Ads with the line advertise a median of **$205,000**, against $190,000 for everything else.

That gap is about which companies write the line, not about the jobs. You can see this with a simple test: add a phrase to the model that can't possibly affect pay, and see what it's "worth." We used "equal opportunity employer."

Compared raw, "equal opportunity employer" looks like a **9.4% pay cut**. Even after controlling for seniority, role, state, work model and ad length, it still looks like a 6% cut. It obviously isn't one. The phrase just shows up more often at lower-paying companies, and every other phrase in the data has the same problem.

Compare each ad only against other ads **at the same company**, and "equal opportunity employer" drops to −0.4%, which is zero. That's the comparison worth trusting, and here is what it shows:

| Phrase in the ad | Raw gap | Same company, same level, same role |
|---|---:|---:|
| Evaluation work (evals, eval harness, offline or model evaluation) | +15.8% | **+2.5%** |
| PhD mentioned | +8.1% | **+2.8%** |
| Production-grade / production systems | +6.9% | **+1.1%** |
| "Ship fast", "bias for action", "move fast" | +6.8% | +0.3% |
| "This is not a research role" | +7.9% | −2.8% |
| *Control: "equal opportunity employer"* | *−9.4%* | *−0.4%* |

Bold values in the last column are statistically significant (p < 0.05).

The "ship fast" language is worth nothing. The companies that use it pay well, but the phrase doesn't mark a better-paid job at those companies.

The anti-research line is worth nothing or slightly less. Only 167 salaried ads carry it, so we can't pin it to exactly zero, but we can rule out a premium larger than about 4%.

The phrase with the clearest premium is the one the line disparages. **Ads that ask for evaluation work pay 2.5% more** than other ads at the same company, and that premium is significantly larger than the one for shipping language. It isn't just a marker of LLM jobs: controlling for whether the ad mentions LLMs or generative AI leaves it unchanged. Asking for a PhD comes with a 2.8% premium, not a penalty.

## What do those ads actually ask for?

![Share of LLM and generative-AI postings that ask for evaluation work, with and without the disclaimer](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/22/e955cb79-d6bf-4b65-9c50-5facd727e73f/H6HEgM4vzkY-03-asking-for-it-anyway.png)

We looked only at postings that mention LLMs or generative AI, so this compares AI jobs with AI jobs:

| Role family | Ads with the line that ask for eval work | Other ads that ask for eval work |
|---|---:|---:|
| Software Engineer | **64.0%** | 12.8% |
| ML Engineer | **56.9%** | 30.6% |
| AI Engineer | 41.4% | 40.5% |
| Data Scientist | 20.8% | 24.7% |
| **All four** | **53.1%** | **21.0%** |

A software engineering ad that says "this is not a research role" is five times as likely as its peers to go on and ask for an eval harness, offline evaluation or LLM-as-a-judge.

Inside AI Engineer the two numbers are the same: about 40% of ads ask for evaluation work whether or not they disclaim research. So the line doesn't tell you anything about the scope of the job. It tells you how the company wants to sound.

## Shipping and evaluating aren't a trade-off

Group ads by which kind of language they use:

| The ad talks about | Median advertised pay |
|---|---:|
| Neither | $178,100 |
| Shipping and production only | $197,500 |
| Research and evaluation only | $205,000 |
| **Both** | **$215,000** |

Hold the job fixed at a senior AI Engineer in California, working hybrid, and the model predicts **$233,207** for an ad that only talks about shipping and **$233,339** for one that only talks about research and evaluation. That's a $132 difference. The best-paying ads ask for both.

## To the people writing this line

The data can't show what happens to teams that go without evaluation. It can show that the employers writing this line are hiring for evaluation anyway, and that the market pays for it. What follows is our argument, built on that.

The worry behind the line is fair. Nobody wants a hire whose work never leaves a notebook. But the line doesn't screen for that. It screens for vocabulary. It tells the person who would have built your eval set that they aren't wanted, three paragraphs before the posting asks for an eval set.

For LLM products, evaluation is not a research phase you finish before shipping. It's how you find out whether the thing you shipped works. It's how you learn that last week's prompt change made the support bot worse before a customer tells you, and whether a model upgrade quietly broke a path nobody tested by hand. Experimentation is how you decide whether a change is an improvement. Prototyping is how you find out cheaply which ideas are worth building. A team without people who do this can still ship. It just can't tell whether what it shipped is any good.

If the job needs someone who owns a system in production, say that: "you'll own this end to end, including on-call." It describes the work without telling researchers to stay away.

## What to do with this

- **If you're job hunting:** don't write the evaluation and experimentation work out of your résumé to sound more production-minded. In this data the production language is worth nothing and the evaluation work is worth a premium. Lead with both.
- **If you see the line in an ad:** read it as tone, not scope. Ask what their eval process is. More than a third of AI Engineer ads ask for evaluation work, so there is a good chance they have one.
- **If you hire:** drop the line. It costs you candidates and, going by these numbers, buys you nothing.

## Methodology

We used 62,659 US postings from the Skillenai job index for AI, ML, data and software engineering roles, keeping only postings with real description text. Some applicant-tracking platforms deliver empty descriptions, and including them would understate every figure.

Each kind of language is a set of patterns matched against the cleaned posting text. We built the patterns from the postings themselves, by collecting sentences that pair research, papers, academia, prototypes or notebooks with a negation and writing up the phrasings that recur. We then read samples of matches to check they meant what we thought. One candidate, "without a PhD," turned out to be mostly welcoming ("researchers without a PhD are encouraged to apply") and was dropped.

Pay comes from 24,445 postings that list a salary range, across 3,788 employers. Hourly and annual ranges are put on the same basis, and job titles are grouped into role families with seniority words removed. The same-company comparison controls for employer, seniority, role family and ad length, with 95% confidence intervals and standard errors clustered by employer.

What this doesn't cover: whether the line is becoming more common (we only have two quarters of reliably dated postings, not enough for a trend); equity, since these are advertised base salaries; and hiring outcomes, since these are ads.

This fits with an [earlier analysis of the LLM evaluation landscape](https://github.com/skillenai/skillenai-notebooks/tree/master/llm-eval-landscape), which found that no named eval framework appears in even 1% of job postings. Employers ask for evaluation work all the time. They rarely name the tools.

[Full methodology, data and code](https://github.com/skillenai/skillenai-notebooks/tree/master/not-a-research-role)
