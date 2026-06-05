**FDEs from frontier labs are to AI Engineers what Solutions Architects from cloud providers were to Software Engineers.**

I wrote that line on Andrew Ng's recent LinkedIn post about the buzzy new Forward Deployed Engineer (FDE) role. Then I tested the analogy against ~44,000 job postings from our index. The data agrees — quantitatively, with two twists I didn't expect.

We pulled four role buckets — Forward Deployed Engineer (877 postings), AI Engineer (3,004), Solutions Architect (2,198), Software Engineer (38,313) — and asked: what skills do these postings actually call for?

## Finding 1: The FDE skill mix is literally AIE on the AI axis, SA on the customer axis

If the analogy is right, an FDE posting should read like an AI Engineer on the LLM/RAG/agents/production-AI stack, and like a Solutions Architect on the stakeholder/customer-success/consulting motion. Both halves land.

![FDE skill mix is literally AIE on the AI axis, SA on the customer axis — grouped bars comparing FDE, AIE, SA, SWE prevalence on AI-platform, customer-facing, and hardcore-SWE skills](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/06/05/e955cb79-d6bf-4b65-9c50-5facd727e73f/O7LObyqAPP8-01-skill-blend.png)

**The AI axis** (FDE ≈ AIE, both ≫ SA):

| Skill | FDE | AIE | SA | SWE |
|---|---:|---:|---:|---:|
| LLMs | 29% | 49% | 8% | 7% |
| AI agents | 38% | 45% | 16% | 10% |
| RAG | 18% | 39% | 5% | 3% |
| **Production AI** | **28%** | **27%** | 4% | 5% |
| LangChain | 9% | 21% | 2% | 1% |
| Fine-tuning | 7% | 21% | 2% | 1% |

The single tightest match: *production AI*. FDE 28% vs AIE 27% — statistically indistinguishable (chi² = 0.27, p = 0.60). On every other AI concept FDE is below AIE, but the FDE-vs-SA gap is the bigger one by an order of magnitude. FDE doesn't go as deep as AIE on the model layer, but it lives in the same world.

**The customer axis** (FDE ≈ SA, both ≫ AIE):

| Skill | FDE | AIE | SA | SWE |
|---|---:|---:|---:|---:|
| **Stakeholders** | **48%** | 22% | **45%** | 17% |
| **Customer success** | **19%** | 3% | **19%** | 2% |
| Consulting | 25% | 9% | 28% | 2% |
| Communication | 32% | 18% | 27% | 26% |
| Travel required | 17% | 1% | 11% | 1% |
| Pre-sales | 13% | 2% | **36%** | 0% |

Stakeholder management: FDE 48% vs SA 45%, p = 0.10. Customer success: 19% vs 19%, p = 0.85. Statistically indistinguishable. The one place FDE and SA diverge is the formal pre-sales motion (13% vs 36%) — SAs sell, FDEs implement. The "FDE is just a rebranded sales engineer" reading doesn't survive contact with the data: the SA's defining feature is exactly where FDE differs most.

Better reading: **FDE is the post-sales technical embed — the customer-success and consulting halves of SA, minus the formal pre-sales motion, plus the LLM stack of AIE.** It even out-travels SA (17% vs 11%, p < 1e-6).

## Finding 2: The customer-facing layer is 5× thicker in AI than it was in cloud

![FDE/AIE = 29.2% vs SA/SWE = 5.7% — the customer-facing layer is 5.1× thicker in AI than it was in cloud](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/06/05/e955cb79-d6bf-4b65-9c50-5facd727e73f/hkZqiMp1i6E-02-role-ratio-5x.png)

The role-count math:

| Era | Customer-facing role | Adjacent tech role | Ratio |
|---|---|---|---:|
| AI | Forward Deployed Engineer (877) | AI Engineer (3,004) | **29.2%** |
| Cloud | Solutions Architect (2,198) | Software Engineer (38,313) | **5.7%** |

For every 100 AI Engineer postings, the market is hiring ~29 FDEs. For every 100 Software Engineer postings, it hired ~6 Solutions Architects. Andrew Ng's directional claim — that AIE will stay the bigger bucket — holds, but the *ratio* of customer-facing to technical roles is 5.1× higher than the cloud-era analog.

The mechanism is in the news: MIT's NANDA Initiative reported that 95% of enterprise AI pilots produced little or no measurable impact on profit and loss, and that the problem was not the models but how they were put into use. Deployment is harder than cloud deployment was, and the market is pricing that into role counts.

## Finding 3: The role has already diffused beyond frontier labs — and is being hype-rebranded on the way down

The analogy says "FDEs *from frontier labs*" — but the title has already escaped that origin.

![Top 20 FDE employers, colored by frontier-lab (red) vs other (gray). Databricks, Parloa, OpenAI, Workato, Anthropic, Chalk, GitLab top the list — the role has already diffused beyond frontier labs](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/06/05/e955cb79-d6bf-4b65-9c50-5facd727e73f/kpt1RFSTlwk-03-diffusion-employers.png)

Among the top 20 FDE employers by open posting count, **three of the four largest are not frontier labs**: Databricks (30), Parloa (25), then OpenAI (23) and Workato (23), then Anthropic (21), Chalk (16), GitLab (14). Frontier labs account for roughly 7% of FDE postings. The rest is enterprise SaaS (Databricks, Workato, GitLab, Intercom, UiPath, Adobe, Vercel) and AI-native startups (Parloa, Chalk, AssemblyAI, Cresta). This is exactly the shape Solutions Architect took on its way to maturity: invented at AWS / Azure / GCP, adopted by every enterprise that consumed those platforms.

### The entry-rung twist

[Yesterday I argued](https://skillenai.com/blog/two-career-entry-doors-in-tech-software-engineer-and-data-analyst) that tech roles with ≥10% entry-share are *tech entry doors*; roles below 10% are *lateral specializations* that require prior experience. Solutions Architect sat dramatically below the line at **1.0% entry-share** — purely senior.

FDE is doing something different.

![Two panels: left shows FDE entry-share by employer tier — frontier labs 6.5% vs everyone else 14.4%; right shows where FDE sits on yesterday's per-role entry-share ladder, slotting between Research Engineer and Research Scientist at 13.9%](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/06/05/e955cb79-d6bf-4b65-9c50-5facd727e73f/w43fM6_IKPQ-04-entry-share-tier-split.png)

Overall FDE entry-share is **13.9%** — comfortably above the 10% door, slotting between Research Engineer (14.0%) and Research Scientist (13.0%) on yesterday's ladder. By that framework, FDE is a tech entry door, not a senior-only lateral specialization.

But the average hides the tier split:

|  | Postings | Entry-level | Entry-share |
|---|---:|---:|---:|
| Frontier labs (OpenAI, Anthropic, Cohere, Mistral, …) | 31 | 2 | **6.5%** |
| Everyone else (Databricks, Chalk, Workato, …) | 423 | 61 | **14.4%** |

At the frontier labs, FDE behaves like SA used to at AWS: senior-only, ~6%. **Everywhere else, FDE behaves like a tech entry door.** The 2.2× tier gap is directional but underpowered on this snapshot (small frontier N, p ≈ 0.19). The supporting employer-by-employer data is the cleaner signal: zero entry-level FDE postings at OpenAI or Anthropic — and 16 entry-level FDE postings at Chalk alone.

A reasonable reading: the title was invented at frontier labs and Palantir as a senior-expert role with seven-figure compensation aspirations (the trade press has cited $385K mid, $610K staff, $1.2M principal at the top of the market). Smaller startups and enterprise SaaS — sitting on the same wave — are using "Forward Deployed Engineer" to relabel early-career customer-engineering and customer-success-engineering roles. Salary samples on the entry-level postings ($100–$220K total base) are normal junior-to-mid customer-engineering pay, not the headline frontier-lab numbers.

This is the *hype-follower* pattern, and it's exactly what early SA postings looked like in 2009–2012 before the role settled into a senior-only steady state. Expect FDE entry-share at non-frontier employers to drift down over the next two years as the role matures and salaries reset toward the frontier-lab anchor.

## What this means

**If you want to be an FDE.** The frontier-lab door (OpenAI, Anthropic, Cohere, Mistral) is overwhelmingly senior — not the on-ramp. The diffusion-tier door (Databricks, Chalk, Workato, Parloa, GitLab, Intercom, Vercel) is open, including at the entry level. Chalk alone has 16 entry-level FDE postings. The pay is normal customer-engineering pay, not the headline numbers — but the skill ramp gets you to the frontier-lab senior FDE role in three to five years.

**If you're a Solutions Architect considering the move.** Your customer-axis skills are already at FDE-level intensity. The on-ramp is the model-layer half: LLMs, RAG, agents, production AI, prompt engineering. Frontier-lab postings are also where the comp ceiling is.

**If you're hiring.** For every 100 AI Engineers, the market is hiring ~29 FDEs. That's a 5× richer customer-facing layer than the cloud era ran. Plan your headcount accordingly — the 95% deployment-failure rate isn't going to fix itself. If you're using "FDE" to relabel a customer-success engineer role, expect that to get diluted as the frontier-lab steady state filters down to your tier.

---

*Full methodology, raw counts, chi-square stats, and figure-generation code: [skillenai-notebooks/fde-as-new-sa](https://github.com/skillenai/skillenai-notebooks/tree/master/fde-as-new-sa).*

*Source data: Skillenai `prod-enriched-jobs` index, 211,909 postings snapshot 2026-06-04. Chi-square 2×2 tests of independence; full results in `stats.json`. Methodology consistent with the senior-club post (2026-06-03) for the entry-share ladder.*
