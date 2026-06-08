# Authoritative Data Visualization in the Skillenai Blog Corpus

**Date:** 2026-06-07
**Source:** `prod-enriched-blog` (428,774 posts, Skillenai Data Products API)
**Author:** Skillenai AI Analyst

Three top-5 lists curated from the Skillenai blog index by author + domain
PageRank-style authority scores, filtered through the synthetic-persona
denylist surfaced in the [SKI-376 Private Blog Network investigation](../synthetic-breakout-may-2026/README.md)
and the standard `source_type=blog` leaky-domain set.

- **Top 5 most authoritative articles about data visualization**
- **Top 5 most authoritative data-viz authors**
- **Top 5 most interesting visualizations on display in the corpus**

> **Methodology note:** "Authoritative" here is operationalized as Skillenai's
> `authorAuthority` and `domainAuthority` — PageRank-style citation scores
> computed from the cross-document link graph. The corpus is blog-only (no
> social posts, no podcast audio analysis, no NYT/Reuters/FT graphics-desk
> subdomains beyond what RSS picks up), so the rankings are best read as
> *"who carries authority among the voices Skillenai indexes"* rather than an
> all-time global ranking of data-viz luminaries.

![Methodology guardrails](05_methodology_guardrails.png)

---

## Why this corpus is the right place to ask the question

Of 428,774 enriched blog posts in the index, **3,883 (0.9%)** mention a
data-visualization phrase in the body — "data visualization", "data viz",
"dataviz", "interactive visualization", "infographic", "data journalism",
"D3.js", "Chart.js". Of those, 116 carry a data-viz term in the **title**.

![Corpus overview](04_corpus_overview.png)

The right-hand panel above tells a humbling story: the canonical data-viz
publications a working dataviz designer would name — FlowingData, The Pudding,
Datawrapper's blog, Reuters Graphics — are essentially absent from the
crawled corpus. NYT carries only four indexed pieces. So this analysis ranks
authority *as seen through Skillenai's lens*, not as it sits in the public
imagination. The voices that surface are the ones who post to public RSS
feeds with crawlable bylines: working academics, podcast hosts, and
practitioners who keep an indexable personal blog.

---

## Top 5 most authoritative articles about data visualization

![Top articles](02_top_articles.png)

| # | Title | Author | Domain | Authority |
|---|---|---|---|---|
| 1 | [Teaching data visualization in the time of generative AI](https://blog.genesmindsmachines.com/p/teaching-data-visualization-in-the) | Claus Wilke | blog.genesmindsmachines.com | AA 1.69 |
| 2 | [Modern Data Visualization with Robert Kosara](https://softwareengineeringdaily.com/2025/09/02/modern-data-visualization-with-robert-kosara) | Software Engineering Daily | softwareengineeringdaily.com | DA 5.7e-6 |
| 3 | [The Collaborative Blueprint: The Open Visualization Academy as a Community of Learning and Friendship](https://nightingaledvs.com/the-collaborative-blueprint) | Alberto Cairo | nightingaledvs.com | AA 0.63 |
| 4 | [Episode 140 — Why Data Visualization Alone Doesn't Fix UI/UX Design Problems in Analytical Data Products](https://brian2r.podbean.com/e/why-data-visualization-alone-doesn-t-fix-uiux-design-problems-in-analytical-data-products-with-t-from-data-rocks-nz) | Brian T. O'Neill | designingforanalytics.com | AA 0.45 |
| 5 | [The history of data journalism](https://datajournalism.com/read/longreads/the-history-of-data-journalism) | Brant Houston | datajournalism.com | AA 0.28 |

**1 — Teaching data visualization in the time of generative AI** is Claus
Wilke (author of *Fundamentals of Data Visualization*, UT Austin) thinking
out loud about what to do with the dataviz classroom now that students can
ask Claude to render a chart for them. The post sits inside a long tradition
of Wilke's pedagogy and is unusual for taking the AI prompt seriously rather
than dismissing it.

**2 — Modern Data Visualization with Robert Kosara** is the Software
Engineering Daily interview with the Tableau Research veteran (formerly of
Eagereyes.org), recorded under the show's high domain-authority masthead.
Kosara's perspective on why most "modern" dashboards are really 1980s
business graphics with a fresh paintjob is the closest thing the show has
to a foundational episode on data visualization theory.

**3 — The Collaborative Blueprint** is Alberto Cairo (Knight Chair at the
University of Miami) writing in Nightingale, the Data Visualization Society's
flagship publication, about the launch of his free Open Visualization
Academy. This is the field's senior practitioner explaining how he intends
to replace tuition-gated coursework with a Creative Commons library — and
his AA of 0.63 makes him the highest-cited "named-author at a publication"
in this entire list.

**4 — Why Data Visualization Alone Doesn't Fix UI/UX Design Problems** is
episode 140 of Brian T. O'Neill's *Designing for Analytics* podcast,
interviewing T at Data Rocks NZ. The thesis — that visualizations live or
die by the UI/UX scaffolding around them — is one of the few takes in this
list that argues *against* dataviz exceptionalism.

**5 — The history of data journalism** is Brant Houston's long-form for
the European Journalism Centre's datajournalism.com — the closest thing the
discipline has to a canonical "where did we come from" essay. Pairs well
with #3 (which is "where are we going").

---

## Top 5 most authoritative data-viz authors

![Top authors](01_top_authors.png)

| # | Author | Domain | n | Avg authorAuthority |
|---|---|---|---|---|
| 1 | [Andrew Heiss](https://www.andrewheiss.com) | andrewheiss.com | 60 | 1.70 |
| 2 | [Claus Wilke](https://blog.genesmindsmachines.com) | blog.genesmindsmachines.com | 20 | 1.69 |
| 3 | [Tobias Macey](https://www.dataengineeringpodcast.com) | dataengineeringpodcast.com | 509 | 1.56 |
| 4 | [Brian T. O'Neill](https://designingforanalytics.com) | designingforanalytics.com | 85 | 0.45 |
| 5 | [Mathias Schäfer](https://9elements.com/blog) | 9elements.com | 37 | 0.19 |

**1 — Andrew Heiss** is an assistant professor at Georgia State who has
quietly become *the* working data-viz tutorial author on the open R / ggplot /
Quarto / Observable Plot stack. 60 posts in the corpus and an AA of 1.70.
His back catalog includes the now-viral animated explainer of `dplyr`'s
verbs (see Viz #2 below) plus a steady stream of map-making, regression-
visualization, and "how to make this chart correctly" walkthroughs.

**2 — Claus Wilke** runs `blog.genesmindsmachines.com` and is best known as
the author of *Fundamentals of Data Visualization* (O'Reilly, 2019). 20 posts
at AA 1.69. His blog reads like the senior-IC counterpart to a Wilke
textbook chapter: each post explains a chart design principle by walking
through an actual visualization decision he made.

**3 — Tobias Macey** is the host of the *Data Engineering Podcast*, with
509 indexed episode-posts at AA 1.56. He doesn't ship visualizations
himself, but the show is the de-facto interview-of-record for vendors and
practitioners building visualization-adjacent infrastructure (dbt, Tableau,
ThoughtSpot, Hex, Snowflake's data app surface, etc.). He's also the
top-volume author on nearly every data-engineering skill we've analyzed in
the past — that "always on the leaderboard" pattern is now well-established.

**4 — Brian T. O'Neill** runs *Designing for Analytics*, the longest-running
podcast on data-product UX. 85 episodes in the corpus at AA 0.45. He's the
person quoted when someone in a data team needs to argue that "you can't
chart your way out of a bad analytical product".

**5 — Mathias Schäfer** at 9elements (Bochum, Germany) is the practitioner
on this list. His agency built the data.who.int health-data dashboard (Viz
#1 below), the GED VIZ tool for the Bertelsmann Foundation, and several
other commission-grade interactive pieces. The corpus has 37 posts under
his byline — fewer than the academics above, but each one ships a real
piece of dataviz infrastructure.

---

## Top 5 most interesting visualizations on display in the corpus

![Top viz pieces](03_top_viz_pieces.png)

| # | Visualization | By | Where |
|---|---|---|---|
| 1 | [data.who.int — global health data interface](https://9elements.com/blog/visualizing-global-health-data-on-data-who-int) | Mathias Schäfer | 9elements.com |
| 2 | [Animated dplyr verb explainer: mutate / summarize / group_by / ungroup](https://www.andrewheiss.com/blog/2024/04/04/group_by-summarize-ungroup-animations) | Andrew Heiss | andrewheiss.com |
| 3 | [Visualizing the Internet (2025)](https://kmcd.dev/posts/internet-map-2025) | kmcd.dev | kmcd.dev |
| 4 | [Visualizing text embeddings using MotherDuck and marimo](https://motherduck.com/blog/MotherDuck-Visualize-Embeddings-Marimo) | MotherDuck team | motherduck.com |
| 5 | [Generative AI is eating culture. See how close it's getting to disrupting dance](https://themarkup.org/artificial-intelligence/2026/01/21/our-video-tests-prove-generative-ai-still-sucks-at-dancing-see-for-yourself) | Khari Johnson & Levi Sumagaysay | themarkup.org |

**1 — data.who.int** is the official World Health Organization dashboard
for global health indicators (mortality, disease burden, immunization
coverage). Schäfer's writeup at 9elements walks through the choices around
geographic granularity, the Observable Plot rewrite, and the accessibility
work that the WHO required before sign-off. This is the most consequential
single dataviz project surfaced anywhere in the corpus — billions of users
indirectly, public-health policy directly.

**2 — Animated dplyr verb explainer** is Heiss's now-classic short post
turning `mutate()`, `summarize()`, `group_by()`, and `ungroup()` into tiny
animations that show how each verb shuffles rows of a tibble. Two years
after it landed it remains the explainer that R newcomers get sent by their
seniors more than any other.

**3 — "Visualizing the Internet (2025)"** at kmcd.dev is the annual treemap
showing global Internet traffic share, allocated bandwidth, and platform
concentration. It's the rare piece of dataviz that holds up year over year
because the data changes meaningfully every twelve months.

**4 — text embeddings explorer with MotherDuck + marimo** is the MotherDuck
team's interactive notebook that takes a text-embedding model output and
renders a UMAP plot you can scrub through. This is the cleanest single
example of the "AI artifact you can poke at in a notebook" genre that has
arguably replaced the static dashboard as the dataviz unit of 2026.

**5 — "Generative AI is eating culture..."** is The Markup's scrollytelling
data-journalism feature on how badly generative video models still handle
human dance. Side-by-side video comparisons, frame-level annotation, and
the kind of forensic "we tested this empirically" framing that The Markup
brought into mainstream data journalism. It's the closest thing in our
sample to the classic NYT/Pudding-style "scrollytelling visual essay".

---

## What this listicle is *not*

- Not a global ranking. Our blog crawl undersamples the dedicated
  graphics-desk subdomains (`graphics.reuters.com`, `graphics.wsj.com`,
  `pudding.cool`, `flowingdata.com`) that own most of the public "best
  dataviz" canon.
- Not a popularity ranking. `authorAuthority` and `domainAuthority` are
  link-graph PageRank-style citation scores, not view counts or social-share
  metrics. An article with low AA can still be wildly popular; high AA
  reflects how often other authoritative pages link in.
- Not a quality judgment about anyone *excluded*. The selection space was
  pre-narrowed to posts in the Skillenai blog index that mention data-viz
  phrases. Practitioners who publish primarily to Observable, Twitter/X,
  Instagram, or LinkedIn won't surface here at all.

## Why the framing matters

The dataviz field has spent fifteen years arguing about how to value its
own work. *"Authoritativeness"* is the most boring possible answer — but
it has the virtue of being computable. A 333-domain Private Blog Network
operator can flood Google with bylined posts; PageRank-style authority is
the field's longest-running defense against that exact attack. The two
academic blogs at the top of our list (Heiss and Wilke) earned their AA
the hard way — by being cited, year after year, in coursework, GitHub
READMEs, and other people's blog posts. That's the signal worth listening
to.

## Data quality notes

- The [SKI-376 Private Blog Network](../synthetic-breakout-may-2026/README.md)
  contributed 333 cheaply-registered domains and 221+ fake bylines that
  would have polluted any naive ranking of dataviz authors and articles.
  Every figure here applies that denylist.
- Junk-author strings (empty, `admin`, `Editorial Staff`, embedded HTML,
  email-as-author, multi-comma multi-author blobs) are filtered from
  author rankings.
- Leaky `source_type=blog` domains (`search.jobs.barclays`,
  `jobs.paloaltonetworks.com`, `vascularnews.com`, `researchsquare.com`,
  `lup.lub.lu.se`, `nofluffjobs.com`) are excluded from every count and
  ranking.
- Generated by the [Skillenai Data Products API](https://api.skillenai.com).
  All counts and authority scores reproducible from the `raw_picks.json`
  and `authors.json` snapshots in this folder.
