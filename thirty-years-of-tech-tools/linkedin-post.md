Novell, Windows NT and Delphi are at zero. Not "declining" — zero.

I traced 633,386 dated job positions from 178,469 careers back to 1996, and asked a simple question: of every named technology people listed, how much of its own peak does it still hold?

Not one of the 28 that peaked before 2002 still holds half. Java comes closest at 48%. COBOL, Unix and Visual Basic are at 2%.

Then the churn stopped. Of technologies peaking 1996-2007, 45% fell below half their peak within five years. Of those peaking 2008-2020: 11%. Same five-year follow-up for every tool, so nothing is credited as a survivor just for being young.

Java and Perl peaked in the same quarter, after identical 19-quarter climbs. Java holds 48% today. Perl holds 1.8%.

Meanwhile Python, SQL, AWS and Docker have climbed for a decade with no serious challenger. SQL rose for 114 straight quarters and peaked last year; Excel rose for 116 and peaked this year. A 1974 query language and a 1985 spreadsheet, both at all-time highs.

And one thing is moving at 1990s speed: LLMs went from a quarter of their peak to their peak in 9 quarters. The median technology took 31.

The AI stack isn't adding to a churning market. It's landing on one that had been quiet for seventeen years.

One more thing, because it cost me the original version of this analysis: I first ran it with a skill vocabulary built from today's job postings. Every term in that dictionary survives to today by construction — so the tools that vanished outright were invisible, and the answer came out backwards.

An instrument anchored in the present cannot measure disappearance.

What's the tool you learned that's now worth nothing?

<!-- model score
scripts/linkedin_scoring/score.py, 2026-09-16. Four drafts scored; v4 shipped.

  draft  impressions  engagements  followers_3d
  v1           863.9          8.6          17.3   base
  v2           844.1          8.6          16.2   paragraphs consolidated -> WORSE, reverted
  v3           823.1          8.7          16.9   acronym line as its own block -> impressions -4.7%, reverted
  v4           921.0          9.5          17.4   same acronyms merged into an existing block  <-- shipped

Read: upper_word_ratio was the top negative driver on v1, so the model wanted more
capitalised acronyms. Adding them as a NEW paragraph (v3) cost more via line_count
than the acronyms gained; folding the identical words into an existing paragraph
(v4) got the gain without the block. Consolidating paragraphs wholesale (v2) did
not help here, contrary to the usual line_count advice - tested, not assumed.
Not applied: "add an exclamation in the hook" - the hook is a flat statement of
fact and an exclamation undercuts it. cv_r2 is 0.27 impressions / 0.40 engagements,
so treat these as a relative ranking between drafts, not as forecasts.
Link goes in the first comment, not the body (has_link is a negative driver).
-->
