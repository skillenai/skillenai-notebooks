**Short answer: machine learning and AI research roles. Research Scientist at $215K and ML Engineer at $209K lead the senior rung, with AI Engineer fourth at $198K.**

The longer answer is more useful. The gap between ML Engineer and a plain software engineer is about $16K. The gap between a mid-level and a staff-level engineer *doing the same job* is $65K.

We measured advertised pay across **62,805 US job postings** that disclose a structured salary range, covering 26 role families at four seniority rungs.

![Advertised pay by role and seniority rung across 28 tech role families, US postings 2026](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/12/e955cb79-d6bf-4b65-9c50-5facd727e73f/im4lmKMFgdA-01-pay-by-role-and-level.png)

## The leaderboard

Senior rung only, so none of this is a seniority-mix artifact.

| # | Role | Median | 95% CI | Postings |
|---|---|---:|---|---:|
| 1 | Research Scientist | **$215K** | $200K–$222K | 265 |
| 2 | ML Engineer | **$209K** | $205K–$213K | 529 |
| 3 | Product Engineer | **$200K** | $192K–$209K | 68 |
| 4 | AI Engineer | **$198K** | $193K–$206K | 164 |
| 5 | Backend Engineer | **$196K** | $192K–$200K | 383 |
| 6 | Frontend Engineer | **$195K** | $190K–$200K | 180 |
| 7 | Software Engineer | **$193K** | $192K–$194K | 5,855 |
| 8 | Infrastructure Engineer | **$192K** | $182K–$200K | 121 |
| 9 | Security Engineer | **$189K** | $180K–$190K | 422 |
| 10 | Product Manager | **$185K** | $183K–$190K | 458 |
| 11 | Platform Engineer | **$183K** | $178K–$195K | 145 |
| 12 | Site Reliability Engineer | **$183K** | $178K–$190K | 319 |
| 13 | Full Stack Engineer | **$180K** | $175K–$185K | 595 |
| 14 | Product Designer | **$179K** | $175K–$184K | 458 |
| 15 | Data Scientist | **$175K** | $167K–$178K | 666 |
| 18 | DevOps Engineer | **$170K** | $165K–$172K | 224 |
| 21 | Data Engineer | **$166K** | $162K–$170K | 435 |
| 23 | Systems Engineer | **$154K** | $148K–$160K | 725 |
| 24 | QA / SDET Engineer | **$147K** | $138K–$153K | 234 |
| 25 | Data Analyst | **$130K** | $123K–$140K | 187 |
| 26 | Business Analyst | **$120K** | $120K–$125K | 132 |

Two things to notice before you rearrange your career around row one.

**The top two are a tie.** Research Scientist and ML Engineer are not statistically separable — Mann-Whitney p = 0.83, and a bootstrap confidence interval on the difference in medians comfortably spans zero. Anyone reporting a single winner here is reporting noise.

**The top is compressed.** Ranks 1 through 13 span $215K down to $180K. That is a $35K band containing most of the engineering job market. Several adjacent pairs have overlapping intervals and should be read as ties rather than as a ranking.

## The ML Engineer premium is real

One role-level premium is solid enough to state plainly. Against Software Engineer at the same rung:

| Check | ML Engineer | Software Engineer | Gap |
|---|---:|---:|---:|
| All postings | $209K | $193K | **+$16K** |
| Excluding its largest employer | $205K | $192K | +$12K |
| California only | $231K | $205K | +$26K |
| Within-employer paired | — | — | **+$12.7K** |

That last row is the one that matters. Across the 37 employers that post *both* roles at the senior rung, ML Engineer pays more at **25 of them** (Wilcoxon signed-rank p = 0.0006). Same companies, same rung, same market — a real premium, not a difference in who happens to be hiring.

With seniority and state controlled, the premium is +8.1%. It is the only role on the board holding a premium above 5% over Software Engineer.

## Now the part that should change your decisions

![Comparing the pay gain from one promotion against the gain from switching to the best-paying role](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/12/e955cb79-d6bf-4b65-9c50-5facd727e73f/EVjEO68Zacc-02-promote-or-switch.png)

For a senior software engineer:

| Move | Gain |
|---|---:|
| Promote to Staff+, same role | **+$40K** |
| Mid to Staff+, same role | **+$65K** |
| Switch to the best-paying role at your rung | +$22K |
| Switch specifically to ML Engineer | +$16K |

One rung is **three times** the best available role switch.

But this flips depending on where you start, and that is the genuinely useful finding. Promotion beats switching for 11 of 21 roles — and they are the 11 best-paid ones. For a **Data Analyst**, a promotion is worth +$23K while moving into the best-paying role is worth **+$86K**; for a **QA / SDET engineer** the same comparison is +$24K against +$68K.

So the advice inverts by tier. If you are already in a well-paid engineering role, the ladder is your lever and shopping titles is close to a rounding error. If you are in the QA or analyst tier, the opposite holds and it is not close.

## There are two cliffs below the engineering tier

The biggest gaps on the board are not between engineering roles. They are below them, and there are two.

| Role | Senior median | vs Software Engineer | Effect size |
|---|---:|---:|---:|
| Software Engineer | $193K | — | — |
| **QA / SDET Engineer** | $147K | **−$46K** | r = −0.543 |
| **Data Analyst** | $130K | **−$63.5K** | r = −0.685 |
| Business Analyst | $120K | −$73K | — |

Both are large effects. With seniority and state controlled, QA carries a −20.9% penalty and Data Analyst −31.6%.

No engineer-versus-engineer comparison comes close. Data Scientist to Software Engineer, often discussed as a major divide, is $18K — a quarter of the QA gap.

The QA number deserves a note, because it nearly went missing from this analysis. "QA Engineer" is fragmented across fourteen different titles in our index — `QA Engineer`, `Quality Assurance Engineer`, `Software Test Engineer`, `Software Development Engineer in Test`, `SDET` and so on — and not one of them individually clears the sample threshold we require. Assembled as a single family it is 487 postings, 234 at the senior rung, one of the better-populated roles on the board.

One title that is *not* on the board: **"Test Engineer."** It is the largest test-related title we have (949 US postings) and it is tempting to read it as software QA. Its top skill term is *manufacturing*, at 25.6%, against Selenium at 6.7% and pytest at 1.6%; its leading employers are hardware and aerospace firms. It is a discipline-mixed bucket spanning manufacturing, hardware and some software test, so its median cannot be attributed to either and does not belong next to Software Engineer. `QA Engineer` and `SDET` are unambiguous by comparison — zero mentions of oscilloscopes or soldering between them.

## How much does the title explain at all?

![Share of pay variation explained by seniority rung, employer, US state, and role label](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/12/e955cb79-d6bf-4b65-9c50-5facd727e73f/GsZ8PyAH6RE-03-variance-explained.png)

Fit advertised pay on each factor by itself, and the role label comes last of the four — despite carrying the most categories:

| Factor | Categories | Variation explained (R²) |
|---|---:|---:|
| Seniority rung | 4 | **0.263** |
| Employer | 60 | 0.224 |
| US state | 15 | 0.186 |
| **Role label** | 26 | **0.149** |

Adding rung on top of role lifts explained variation by 0.221. Adding role on top of rung lifts it by only 0.108. The ordering does not drive the result.

This is not a claim that job titles are meaningless — 0.149 is not zero, and the QA and analyst cliffs above are title effects. It is narrower and more actionable than that: **of the four things setting your pay, the title is the one you would optimise last.** Which sits comfortably alongside an earlier finding of ours that [job titles explain under 10% of the skills a tech job actually requires](https://skillenai.com/2026/09/08/job-titles-explain-under-10-of-the-skills-a-tech-job-requires).

Geography makes the point concrete. Holding role and rung constant, a posting in Florida advertises **32.6% less** than the same role and rung in California, and Texas 22.8% less. That single dimension moves pay more than almost any role switch available to you.

## The eight titles we threw out

Our first version of this leaderboard was topped by Research Engineer at $260K. That number was an artifact: 26.8% of senior Research Engineer postings came from a single employer, and removing them dropped the median to $220K.

So every role here had to clear a gate — **at least 10 distinct employers, and no single employer holding more than a quarter of the senior rung.** Eight titles failed on concentration:

| Title | Top employer's share | Median | Without them |
|---|---:|---:|---:|
| Mission Software Engineer | 85.5% | $222K | too few left |
| Firmware Engineer | 54.4% | $193K | $193K |
| Applied Scientist | 53.8% | $200K | $207K |
| Cybersecurity Specialist | 44.2% | $125K | $124K |
| Solutions Architect | 39.7% | $210K | $175K |
| Forward Deployed Engineer | 36.2% | $215K | $196K |
| Technical Program Manager | 30.8% | $190K | $177K |
| Research Engineer | 26.8% | $260K | $220K |

These exclusions are themselves informative. When 85% of "Mission Software Engineer" postings trace to one defense manufacturer, that title is a single company's internal ladder, not a market rate. Ranking it against Software Engineer would be a category error.

Three further titles are excluded for a different reason: the bucket is not comparable to the rest of the board. "Test Engineer" is discipline-mixed (above); "Engineering Manager" is 93% people-management and belongs in a management comparison; "IT Specialist" is a federal job-series classification rather than a market role title.

Worth noting how nearly we missed the concentration problem: our index held one large employer under three different canonical names. Before we normalised them, three of the eight titles above passed the 25% test. Any concentration check run on raw employer names will under-detect.

## What this measures, and what it does not

- **Advertised base pay only.** No equity, no bonus, no sign-on. This understates total compensation most at AI labs and at senior levels, which is exactly where equity is largest.
- **Only postings that disclose a range** — roughly 15% of US postings, and disclosure varies widely by applicant-tracking platform.
- **Big Tech is largely absent.** Google, Apple, Microsoft, Meta and Netflix use systems we do not index. The mix skews toward defense-tech, AI labs and scale-ups.
- **Management is held out** so the ranking compares individual contributors like for like. Labels that are majority people-management — Program Manager at 83%, Product Manager at 56% — would otherwise blend two different jobs into one median.
- **A posting is not a hire.** These are advertised ranges, not accepted offers.

## What to do with this

**If you are choosing a specialisation:** machine learning is the one that pays a real, replicable premium, and it is about $16K at the senior rung. Worth having. Not worth reorganising a career you otherwise like.

**If you are a mid-level engineer:** the promotion is the whole game. $65K to staff, against $16–22K for any lateral title move. Optimise for scope and the next rung, not the label.

**If you are in QA or an analyst role:** you are the exception. The tier boundary is worth $46K–$86K, far more than any promotion inside the tier. For QA and SDET specifically, the move into product engineering is worth roughly three promotions. Moving to engineering, analytics engineering or data science is the highest-value move on this entire board.

**If you are hiring:** your salary band is competing against seniority, geography and your own employer brand before it competes on job title. Retitling a role does much less than you think.

[Full methodology and data](https://github.com/skillenai/skillenai-notebooks/tree/master/tech-role-pay-2026)

## Methodology

62,805 US postings from the Skillenai labor-market index with a USD salary currency and both range bounds populated; 31,407 across the 26 role families clearing the gates. Pay is the advertised base-range midpoint. 400 hourly-rate postings were converted at 2,080 hours; 107 in an ambiguous weekly-or-monthly band were dropped rather than guessed.

Seniority words are stripped from titles so that "Staff Software Engineer" folds into Software Engineer rather than competing with it as a separate role — otherwise a leaderboard just surfaces senior-sounding titles. Software QA is assembled explicitly from fourteen fragmented titles, since none clears the threshold alone. Titles that can span hardware and software were tested by measuring skill-term prevalence inside the posting text rather than trusting the title, which is what removed "Test Engineer." Rungs are Entry (entry + junior), Mid, Senior, and Staff+ (staff + principal); management and exec rows are held out.

All median confidence intervals are bootstrapped over 4,000 resamples. Two-group comparisons use Mann-Whitney U with rank-biserial correlation for effect size; the within-employer comparison uses Wilcoxon signed-rank. Role premiums come from OLS on log pay with rung, state and employer controls.

