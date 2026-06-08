PageRank-style authority is the most boring possible way to rank the data-viz field — and the most accurate one we found.

We mined 428,774 blog posts in the Skillenai index for the most authoritative data-viz writing on the web. Three top-5 lists fell out — articles, authors, and the most interesting visualizations on display.

The top 5 dataviz authors by AA (authorAuthority) ended up being: Andrew Heiss (the working R / ggplot / Quarto / Observable Plot tutorial author of record, AA 1.70, 60 posts), Claus Wilke (Fundamentals of Data Visualization, AA 1.69), Tobias Macey (Data Engineering Podcast, 509 episodes, AA 1.56), Brian T. O'Neill (Designing for Analytics, 85 episodes on data-product UX, AA 0.45), and Mathias Schäfer at 9elements (the practitioner who shipped the WHO data.who.int dashboard, AA 0.19).

The top 5 visualizations on display: the WHO global-health dashboard at data.who.int, Heiss's animated dplyr verb explainer, kmcd.dev's annual Visualizing the Internet treemap, the MotherDuck × marimo text-embeddings explorer, and The Markup's scrollytelling test of AI vs. human dance.

What's not on the list says as much as what is. FlowingData, The Pudding, Reuters Graphics, NYT graphics — the canonical graphics-desk outlets — barely register in any RSS-driven blog index. The voices that surface are the ones with crawlable, citation-earning RSS feeds: academics, podcast hosts, and practitioners who keep an indexable blog.

PageRank-style authority is also the field's longest-running defense against content farms — exactly the AI-native synthetic-persona PBNs we've been writing about. Heiss and Wilke earned their AA the slow way: cited, year after year, in coursework, GitHub READMEs, and other people's blog posts.

That's the signal worth listening to. Everything else is taste.

Full lists and reproducible queries in the post — link in the first comment.

Which dataviz authors would you add — that don't post to RSS?

<!-- model score
baseline v1: impressions=942, engagements=16.4, followers_3d=16.3
v2 (compressed bullets, removed unicode ▪): impressions=1514, engagements=19.9, followers_3d=14.9
v3 (added punchy hook line, kept question, lightly tighter): impressions=1613, engagements=21.7, followers_3d=14.3
net gain: impressions +71%, engagements +32%, followers_3d -12%

drivers (v3 baseline):
+ ends_with_question (+0.19), word_count (+0.17), data ngram (+0.03), several acronyms (PageRank, RSS, AA, WHO, NYT, AI, R)
- line_count (only when bullets dominate — flattened in v2/v3), has_link (none in body, kept link in comments)
skipped suggestion: "Add an exclamation" — per skill memory this is unreliable (-5% impressions in past runs)
-->
