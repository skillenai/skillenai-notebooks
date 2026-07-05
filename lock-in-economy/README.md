# The Lock-In Economy: Why Entry-Level Jobs Vanished — and Why It Probably Wasn't AI

**Skillenai AI Analyst · July 2026**

A viral essay, [*"AI has torched the market for junior programmers"*](https://seldo.com/posts/ai-has-torched-the-market-for-junior-programmers/) (Laurie Voss, July 2026), argues that agentic coding tools have gutted the junior-developer job market. The collapse it describes is real. But when we pulled the data sources it cites — and added two the essay didn't have (a supply-side hiring-flow panel and a job-postings demand index) — the *cause* points somewhere else: a labor market that **froze** after the 2022 interest-rate shock, in lockstep with the housing market, starving its own bottom rung first.

This report reproduces the essay's public data (Indeed, BLS, Fed NY), adds Skillenai's job-postings index and a workforce hiring-flow panel, and tests the AI-causation story against a frozen-market story. The frozen-market story wins on every test we could run.

> **Bottom line:** Entry-level hiring didn't collapse because AI learned to code. It collapsed because *nobody quit* — and a market where incumbents stop moving stops creating the vacancies newcomers need. The housing market, frozen by the same 2022 rate shock with no AI anywhere near it, is the control group that makes the point.

---

## What we used

| Source | Role in this analysis | Access |
|---|---|---|
| **Indeed Hiring Lab** Job Postings Tracker | Software/Data postings trend 2020–2026 | Public |
| **BLS JOLTS** (Information sector) | Hires / quits / layoffs turnover | Public API |
| **Fed NY** Recent College Graduates | Grad unemployment by major | Public |
| **NAR / FRED** existing-home sales | Housing-freeze control group | Public |
| **Skillenai jobs index** (110.8K US postings) | Entry-level share by role; AI-skill demand by seniority | Skillenai Data Products API |
| **Workforce hiring-flow panel** (workforce.ai) | Arrivals / departures / promotions by seniority | Licensed |

Skillenai's job index begins in early 2026, so **every multi-year time trend here comes from Indeed, BLS, the workforce panel, and NAR** — our index contributes the cross-sectional role and skill detail, not the trend.

---

## 1. The collapse is real

![US tech job postings never recovered from the 2022 freeze](01_indeed_postings.png)

Indeed's US **Software Development** postings index ran near 230 in early 2022, bottomed around 65 in early 2025, and has only crawled back to ~85 — still ~63% below peak. **Data & Analytics** is *still* sliding. The turn is sharp and it lines up with the **March 2022 Fed liftoff**, not with any single AI product launch.

The supply side agrees. In the workforce hiring-flow panel, actual *hires* into software-engineering roles fell hardest at the bottom:

| Seniority | 2022 arrivals | 2025 arrivals | Change |
|---|---|---|---|
| Entry (intern) | 39,833 | 17,397 | **−56%** |
| Rank-and-file IC | 268,302 | 150,541 | −44% |
| Senior IC | 116,613 | 94,604 | −19% |

A clean gradient: the more junior the role, the steeper the collapse. On this, the essay is right.

## 2. But it isn't tech-specific — and that breaks the AI story

If AI coding tools were the cause, the damage should concentrate in software. It doesn't. Entry-level hiring fell **50–74% across every job function we measured**, and Engineering and IT sit *mid-pack*:

![The entry-level collapse is economy-wide — software is mid-pack](03_intern_by_function.png)

Human Resources (−74%) and Marketing (−67%) were hit *harder* than Engineering (−65%) or IT (−63%). The Fed NY data says the same thing from the graduate side: recent-grad unemployment is elevated across nearly all majors, with **anthropology (7.9%) essentially tied with computer engineering (~8%)** at the top. A humanities major and a hardware-engineering major do not get automated by a coding assistant in the same quarter. This is a whole-economy entry freeze.

And within tech, the AI-heavy roles are the *friendliest* to entrants, not the harshest:

![If AI were killing juniors, AI roles should be worst — they're the best](05_entry_door_by_role.png)

Machine Learning Engineer (21% entry-level), Data Scientist (16%), and AI Engineer (16%) all match or beat plain Software Engineer (15%). The genuinely closed doors are lateral infrastructure specializations — Platform (2.5%), SRE (5.7%), Security (5.4%) — that were never entry points. We also find AI-skill demand is **flat across seniority** (25.1% of entry-level postings mention AI/ML skills vs. 25.1% of senior). Whatever is closing the junior door, it is not that entry jobs suddenly all require an LLM.

## 3. The real mechanism: nobody quit

The clearest tell is the **quit rate**. In the BLS Information sector it sits at **1.2% — below the pre-pandemic norm (~1.6%) and below even the COVID-shock year**. When incumbents stop quitting, the backfill vacancies that used to absorb newcomers never open. Meanwhile *departures also fell* across the panel — this is a market that seized on both sides, not one that shed workers.

The freeze then cascades **down** the ladder. With senior people staying put, promotions slow, and the bottom rung clogs worst:

![The ladder clogged worst at the bottom rung](04_promotion_velocity.png)

| Promotion | 2021–22 | 2024–25 | Fewer people | Slower |
|---|---|---|---|---|
| Intern → IC (entry conversion) | 6,804 @ 7.3 mo | 2,851 @ 9.6 mo | **−58%** | +32% |
| IC → Senior IC (first promo) | 29,114 @ 27.4 mo | 25,673 @ 34.9 mo | −12% | +27% |

Junior hiring is *discretionary pipeline-building*. When there is no vacancy above to justify it, it is the first line cut — and juniors are **complements to scarce senior time**, not substitutes for it. A junior only becomes productive after a senior spends bandwidth training and reviewing them. When senior time is the bottleneck and its price stays hot (senior comp never softened), the fully-loaded cost of a junior — salary *plus* the senior hours they consume — turns ROI-negative. That, not automation, is why the bottom rung emptied. (It also explains why AI gets blamed: AI competes with juniors for the *same* scarce senior-review attention.)

## 4. Housing is the control group

Why lean on housing? Because it ran the same experiment with **zero AI involvement**.

![Two markets, one freeze: homes and jobs both locked up after 2022](02_housing_vs_quits.png)

The 2022 rate shock froze both markets through the same **lock-in** mechanic. In housing, ~69% of mortgaged owners sit on rates at or below 5% and won't sell into a 7% market; existing-home sales fell to **4.06M in 2024, the lowest since 1995**, and stayed there. First-time buyers — the "entry-level" of housing — got locked out, not because they were unwanted but because *the turnover that used to free up starter homes stopped*.

That is the labor market's story in a different asset class. And the two are **causally coupled**: a senior engineer sitting on a 3% mortgage won't relocate for a new role, so a whole class of job-changes — and the backfill vacancies they create — simply don't happen. Housing lock-in is one of the reasons the quit rate is on the floor.

The rhetorical payoff: housing proves you don't need AI to break the bottom rung. You just need to stop the top from moving.

---

## What's ours vs. what we're citing

In the spirit of honest attribution:

- **Established, and cited — not our discovery:** that the labor market is frozen / "low-hire, low-fire" (St. Louis Fed; J. Politano, *Apricitas*; RBC Economics); that the entry-level decline is macro rather than AI (NBER WP 33777, Humlum & Vestergaard; Yale Budget Lab; the Economic Innovation Group's [*Looking for the Ladder*](https://agglomerations.eig.org/p/looking-for-the-ladder)); that mortgage-rate lock-in reduces labor mobility ([Fonseca & Liu, *J. Finance* 2024](https://onlinelibrary.wiley.com/doi/10.1111/jofi.13398)); and that AI acts as *seniority-biased* technical change (Hosseini & Lichtinger). The pro-AI case is anchored by the Stanford Digital Economy Lab's *Canaries in the Coal Mine?*.
- **New evidence we're introducing:** (1) the entry-level collapse quantified as **economy-wide across 10 job functions**, with tech mid-pack; (2) the **promotion-velocity clog** measured directly (entry conversions −58%, +32% slower); (3) Skillenai's finding that **AI-heavy roles retain the most open entry doors** and AI-skill demand is seniority-flat; and (4) **housing framed as a control group** — same trigger, same lock-in, same locked-out newcomer, no AI — that ties mortgage lock-in → low quits → clogged ladder into one chain.

## Methodology & caveats

- **Filters:** US postings only; the carpet-bombing spam employer *Speechify* excluded; company counts use canonical names. Role buckets under ~1,000 postings are read with caution.
- **Time trends are not from Skillenai.** Our index starts in early 2026; multi-year trends come from Indeed, BLS, the workforce panel, and NAR.
- **The workforce panel undercounts the most recent periods** (profile-update lag) and promotion velocity is right-censored — both bias *against* finding a slowdown, so the −58% / +27–32% figures are, if anything, conservative. We anchor comparisons on 2022 vs 2025.
- **The lock-in → quits link is the weakest joint.** The academic literature ties mortgage lock-in firmly to reduced *mobility*; its contribution to the aggregate *quits* decline is real but partial. We present it as one contributing driver, not the sole cause.
- **This is correlational.** We show AI's fingerprints are absent from the demand pattern; we can't rule out a second-order AI effect on the macro freeze.

## Takeaways

1. **The junior job market really did collapse** — entry-level hiring is down ~56% since 2022, steeper than any senior tier.
2. **It isn't software-specific.** Entry hiring fell 50–74% across HR, marketing, finance, legal, healthcare and more; grad unemployment is elevated across majors.
3. **The AI-heavy roles have the *most* open entry doors**, and AI-skill demand doesn't rise at entry level — the opposite of what an AI-displacement story predicts.
4. **The quit rate is the tell.** At a multi-decade low, it chokes off the backfill vacancies newcomers depend on and clogs the promotion ladder from the top.
5. **Housing is the proof.** The same 2022 rate shock froze the housing market — locking out first-time buyers with zero AI involved — and senior workers' own mortgage lock-in feeds the labor freeze.
6. **For new grads:** target the roles still creating entry openings (AI/ML, data, generalist software) over lateral specializations, and watch the quit rate — the entry market thaws when incumbents start moving again, not when AI gets worse at coding.
