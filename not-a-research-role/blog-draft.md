Somewhere in the last year, a new sentence started showing up in AI job ads.

> "This is not a research role. This is not a 'play with models in a lab' role. This is a builder role."

It comes in variations. "Production AI shipping experience, not just research, POCs, demos, or internal experiments." "You've owned models beyond the notebook." One company listed it under *You Might Not Be a Fit If*: "Your experience is limited to experimentation without production systems."

The message to anyone with a research background is hard to miss. The market wants builders, research is a liability, and the smart move is to scrub the experiments and the evaluation work from your résumé and lead with what you shipped.

That message is wrong, and job postings themselves are the evidence. Across **62,659 US tech job postings** from **8,728 employers**, the anti-research line turns out to be rare, it carries no pay premium, and the ads that use it are often asking for exactly the research skills they claim not to want.

## A loud line, rarely written

![Share of US tech postings that disclaim research versus those that name research, evals or experimentation as part of the job](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/22/e955cb79-d6bf-4b65-9c50-5facd727e73f/Eu4XfJq4zUE-01-who-disclaims-research.png)

The line is memorable, which makes it feel common. It isn't.

| Role family | Ads that disclaim research | Ads that name research, evals or experimentation as the job |
|---|---:|---:|
| AI Engineer | **2.7%** | **43.3%** |
| ML Engineer | 1.9% | 43.4% |
| Data Scientist | 1.0% | 32.3% |
| Research / Applied Scientist | 0.8% | 73.2% |
| Data Engineer | 0.2% | 6.4% |
| Data Analyst | 0.0% | 8.5% |
| Software Engineer | 0.5% | 8.1% |

It is concentrated where you would expect. An AI Engineer ad is about five times as likely as a software engineering ad to carry it. But even there it appears in fewer than 3 ads in 100. Across all US tech postings it's 0.7%, and only 2.1% of employers have ever written it.

The opposite message is everywhere. For every AI Engineer ad that says the job isn't research, about 16 describe research, evaluation or experimentation as part of the work.

This isn't an artifact of a few companies spamming the same posting. The 439 ads carrying the line come from 179 different employers, and none accounts for more than 13% of them.

## The line doesn't pay

![Advertised pay effect of each phrase, raw versus compared within the same employer](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/22/e955cb79-d6bf-4b65-9c50-5facd727e73f/E5nL-Uj1eN8-02-what-the-words-are-worth.png)

On the surface, the builder-not-researcher ads look like the better-paid ones. They advertise a median of **$205,000**, against $190,000 for everything else.

That gap says more about the companies than the jobs. The clearest way to see it is to test a phrase that can't possibly change what a job pays, like "equal opportunity employer." Compared naively, ads containing it pay 9.4% less. Nobody believes that sentence costs anyone money. It simply turns up more often at lower-paying companies, and every other phrase in a job ad carries the same kind of baggage.

Compare each ad only with other ads **at the same company**, and "equal opportunity employer" falls to −0.4%, effectively zero. That's the fair comparison. Here's what the rest of the language is worth under it:

| Phrase in the ad | Naive gap | Same company, level and role |
|---|---:|---:|
| Evaluation work (evals, eval harness, offline or model evaluation) | +15.8% | **+2.5%** |
| PhD mentioned | +8.1% | **+2.8%** |
| Production-grade / production systems | +6.9% | **+1.1%** |
| "Ship fast", "bias for action", "move fast" | +6.8% | +0.3% |
| "This is not a research role" | +7.9% | −2.8% |
| *Control: "equal opportunity employer"* | *−9.4%* | *−0.4%* |

*Bold values in the last column are statistically significant (p < 0.05).*

"Ship fast" and "bias for action" are worth nothing. Companies that talk that way do pay well, but the phrase doesn't identify a better-paid job inside them.

The anti-research line is worth nothing or slightly less. Only 167 of these ads list a salary, so the estimate is loose, but it rules out any premium bigger than about 4%.

The language with the clearest premium is the language the line looks down on. Ads that ask for **evaluation work pay 2.5% more** than other ads at the same company, a significantly bigger premium than shipping language earns. That holds after accounting for whether the job involves LLMs at all. And ads that mention a PhD pay 2.8% more, not less.

## Disclaiming research, then asking for it

![Share of LLM and generative-AI postings that ask for evaluation work, with and without the disclaimer](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/22/e955cb79-d6bf-4b65-9c50-5facd727e73f/H6HEgM4vzkY-03-asking-for-it-anyway.png)

Read past the disclaimer and a different job often appears. Among postings for LLM and generative-AI work:

| Role family | Ads with the line that ask for eval work | Other ads that ask for eval work |
|---|---:|---:|
| Software Engineer | **64.0%** | 12.8% |
| ML Engineer | **56.9%** | 30.6% |
| AI Engineer | 41.4% | 40.5% |
| Data Scientist | 20.8% | 24.7% |
| **All four** | **53.1%** | **21.0%** |

A software engineering ad that opens with "this is not a research role" is five times as likely as its peers to go on to ask for an eval harness, offline evaluation or LLM-as-a-judge.

For AI Engineer roles, the line makes no difference at all. About 40% of those ads ask for evaluation work whether they disclaim research or not. The disclaimer tells you how a company wants to sound. It tells you nothing about the work.

## Shipping and research aren't rivals

The ads imply a choice between building and investigating. Pay data shows no such choice.

| The ad talks about | Median advertised pay |
|---|---:|
| Neither | $178,100 |
| Shipping and production only | $197,500 |
| Research and evaluation only | $205,000 |
| **Both** | **$215,000** |

For a fixed job, a senior AI Engineer working hybrid in California, an ad that talks only about shipping predicts **$233,207**. One that talks only about research and evaluation predicts **$233,339**. The difference is $132. The best-paid ads want both.

## Why the line is a mistake

The worry behind the sentence is reasonable. Every hiring manager has met the candidate whose work never left a notebook, and nobody wants to hire that person into a role that has to ship.

But the line doesn't screen for that person. It screens for vocabulary. The candidate it turns away is the one who talks about experiments and evaluation, which, as these ads themselves show, is often the person the team needs.

For LLM products especially, evaluation isn't a research phase you finish before production. It's how a team knows whether what it shipped works. It's how you learn that last week's prompt change made the support bot worse before a customer tells you, or that a model upgrade quietly broke a path nobody tests by hand. Experimentation is how you know whether a change is an improvement. Prototyping is how you find out cheaply which ideas deserve to be built properly. A team without people doing this work can still ship. It just can't tell whether what it shipped is any good.

If the job really needs someone who owns a system in production, the ad can say exactly that: "you'll own this end to end, including on-call." That describes the work without warning off the people who would make it reliable.

## What this means for your career

- **If you have a research or evaluation background,** don't edit it out to sound more production-minded. In this data, production language is worth nothing extra and evaluation work carries a premium. Show both.
- **If you see the line in a posting,** treat it as tone rather than scope, and ask about the team's evaluation process in the interview. More than a third of AI Engineer ads ask for evaluation work, so there's a good chance the role involves it.
- **If you write job ads,** drop the line. It narrows your pipeline and, going by these numbers, buys you nothing.

## Methodology

The analysis covers 62,659 US postings from the Skillenai job index for AI, ML, data and software engineering roles, limited to postings with real description text. Some applicant-tracking platforms deliver empty descriptions, and including them would understate every figure.

Each type of language is a set of text patterns matched against the posting. The patterns were built from the postings themselves, by collecting sentences that pair research, papers, academia, prototypes or notebooks with a negation and writing up the phrasings that recur, then reading samples of matches to confirm what they meant. One candidate, "without a PhD," turned out to be mostly welcoming ("researchers without a PhD are encouraged to apply") and was dropped. Prevalence figures were checked against differences in ad length and against companies posting the same text repeatedly.

Pay comes from 24,445 postings that list a salary range, across 3,788 employers. Hourly and annual ranges are converted to the same basis, and job titles are grouped into role families with seniority words removed. The same-company comparison controls for employer, seniority, role family and ad length, with 95% confidence intervals and standard errors clustered by employer.

Three limits are worth knowing. With only two quarters of reliably dated postings, there isn't enough history to say whether the line is spreading. These are advertised base salaries, so equity isn't captured. And these are ads, not hiring outcomes.

The findings sit alongside an [earlier analysis of the LLM evaluation landscape](https://github.com/skillenai/skillenai-notebooks/tree/master/llm-eval-landscape), which found that no named eval framework appears in even 1% of job postings. Employers ask for evaluation work constantly. They rarely name the tools.

[Full methodology, data and code](https://github.com/skillenai/skillenai-notebooks/tree/master/not-a-research-role)
