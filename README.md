# What Builds Buyer Trust? A Consumer-Psychology Analysis of Customer Feedback at a Family-Run eBay Shop

**Author:** Henry Zhang

## Abstract

Online buyers must trust sellers they never meet. This study examines the public feedback record of a small, family-run eBay resale shop (seller ID *zhashuzhan*, Top Rated Seller, member since June 2015) to ask which aspects of the buying experience customers mention when they choose to write about it. Of 257 captured feedback entries, 43 were comments written by buyers about purchases from the shop. These were coded with a transparent keyword codebook and scored with the VADER sentiment model. Buyers most often mentioned shipping speed (23 of 42 positive comments, 54.8%), the item matching its description (18, 42.9%), and packaging (10, 23.8%). Mean sentiment of positive comments was strongly positive (VADER compound = 0.59). The shop's only negative entry, a non-delivery complaint, falls in eBay's "More than a year ago" bucket; every entry in the past 12 months is positive (100% positive, 190 ratings per eBay). The findings suggest that, for this shop, buyer satisfaction is expressed mainly through *reliability signals*: fast shipping, accurate descriptions, careful packaging, and responsiveness when something goes wrong.

## Research Question

**When buyers of a small online shop write feedback, which aspects of the transaction do they talk about, and how consistent is their satisfaction across time?**

The sellers' working view is that the shop maintains consistently strong reviews *because it listens to its customers*. This report treats that as the sellers' practice and interpretation, and asks what the public feedback record shows that is consistent with it. It does not test it as a proven cause.

## Background

Buying from a stranger online is a trust problem. Mayer, Davis, and Schoorman (1995) describe trust as a willingness to be vulnerable to another party, based on perceptions of that party's *ability*, *benevolence*, and *integrity*. In online marketplaces, buyers judge these qualities through signals such as reputation scores and the written experiences of previous buyers (Resnick & Zeckhauser, 2002).

Service-quality research gives a vocabulary for what buyers evaluate. The SERVQUAL model (Parasuraman, Zeithaml, & Berry, 1988) identifies five dimensions: *reliability* (delivering what was promised), *responsiveness* (willingness to help promptly), *assurance*, *empathy*, and *tangibles*. For an eBay seller these map naturally onto shipping speed and accurate descriptions (reliability), handling of problems and messages (responsiveness, empathy), and physical packaging (tangibles).

A known feature of eBay's reputation system is that feedback is overwhelmingly positive (Resnick & Zeckhauser, 2002), so the *content* of written comments can be more informative than the positive/negative count alone. This study therefore focuses on what buyers wrote.

## Method

### Data source

The shop's public eBay feedback page was captured in full, giving 257 of the 259 entries listed (2 entries were not captured). Each entry includes the comment text, rating (positive/neutral/negative), eBay's time bucket (*Past month*, *Past 6 months*, *Past year*, *More than a year ago*), and, for sales, the item and price. eBay shows only these time buckets, not exact dates, so all time comparisons use them. Profile-level figures (positive-feedback percentage, detailed seller ratings) were taken from the same public profile and are saved in `data/profile_summary.json`.

Entries were classified by source:

| Source | n | Used in analysis? |
|---|---|---|
| Comments written by buyers of the shop | 43 | Yes, main sample |
| eBay automated feedback ("Order delivered on time with no issues") | 145 | Counts only (no buyer-written text) |
| Feedback the account received *as a buyer* from other sellers | 69 | No, excluded (not about this shop's service) |

![Figure 1](figures/fig1_feedback_by_source.png)

Buyer usernames were removed and appear nowhere in this repository.

### Theme coding

Each buyer comment was coded for seven themes using a keyword codebook (`analysis/codebook.json`). A comment receives a theme if any of that theme's patterns appears; a comment can receive several themes. The themes are shipping speed, communication/service, item as described/quality, packaging, price/value, would buy again/recommend, and general praise. Keyword coding is transparent and reproducible but less nuanced than human coding (see Limitations).

### Sentiment scoring

Each comment was scored with VADER (Hutto & Gilbert, 2014), a lexicon- and rule-based sentiment model built for short social-media-style text. VADER's *compound* score ranges from −1 (most negative) to +1 (most positive).

### Reproducing the analysis

```
pip install -r requirements.txt
python analysis/analyze.py
```

Outputs: `data/buyer_comments.csv` (cleaned sample), `results/*.csv`, and `figures/*.png`.

## Results

### Overall satisfaction

According to the eBay profile, the shop has **100% positive feedback over the past 12 months**, with **0 neutral and 0 negative** ratings in the past 1, 6, and 12 months, and positive counts of 19 (1 month), 127 (6 months), and 190 (12 months). All four Detailed Seller Ratings (accurate description, 33 ratings; reasonable shipping cost, 39; shipping speed, 40; communication, 40) are displayed at 5 stars. The shop holds eBay's Top Rated Seller status.

Of the 188 captured sales-feedback entries (buyer-written plus automated), 187 are positive and 1 is negative:

| eBay time bucket | Positive | Negative |
|---|---|---|
| More than a year ago | 0 | 1 |
| Past year | 63 | 0 |
| Past 6 months | 106 | 0 |
| Past month | 18 | 0 |

![Figure 4](figures/fig4_pos_neg_by_bucket.png)

### What buyers wrote about

Across the 42 positive buyer-written comments:

| Theme | Comments | % of positive comments |
|---|---|---|
| General praise | 35 | 83.3 |
| Shipping speed | 23 | 54.8 |
| Item as described / quality | 18 | 42.9 |
| Packaging | 10 | 23.8 |
| Price / value | 7 | 16.7 |
| Communication / service | 6 | 14.3 |
| Would buy again / recommend | 3 | 7.1 |

31 of the 42 positive comments (73.8%) mention at least one concrete reliability or tangibles theme (shipping speed, communication/service, accurate description, or packaging), and 21 (50.0%) mention two or more specific themes besides general praise.

![Figure 2](figures/fig2_theme_frequency.png)

### Sentiment

| eBay time bucket | Written comments | Mean VADER compound |
|---|---|---|
| More than a year ago | 1 | 0.273 |
| Past year | 24 | 0.593 |
| Past 6 months | 16 | 0.604 |
| Past month | 2 | 0.442 |

Mean compound across all 42 positive comments was 0.590. Sentiment was stable across the two buckets with meaningful sample sizes (Past year, 0.593; Past 6 months, 0.604). The "Past month" (n = 2) and "More than a year ago" (n = 1) means are based on too few comments to interpret.

Notably, VADER scored the single negative comment as mildly *positive* (+0.273): its text ("I never received the item on top of being charged…") contains no strongly negative words, so the model missed a clearly negative experience. This is a useful reminder that automated sentiment tools can misread complaints that are stated factually.

![Figure 3](figures/fig3_sentiment_by_bucket.png)

### Representative comments

Quoted verbatim (typos preserved); time bucket in brackets.

1. *"Seller did everything right. My purchase arrived very quickly in 3 days! It however, did not work/power-on and a Return was quickly accepted by the seller."* [Past 6 months]
2. *"An overall pleasant experience with the seller, good customer communication, thank you."* (excerpt) [Past 6 months]
3. *"Great seller, good communication, and a pleasure to deal with. A+"* [Past year]
4. *"Item as described, extremely well protected/ packaged. arrived in mint condition. Only complaint is user manual is in extremely small print ."* [Past month]
5. *"I never received the item on top of being charged for the item as well."* [More than a year ago; the shop's only negative entry]

## Discussion

**Consistency.** The clearest finding is consistency: every rating in the past 12 months is positive, and the sentiment of written comments is stable across the time buckets with enough data to compare. For a small family-run shop selling a wide range of consumer goods, sustaining that record across roughly 190 rated transactions in a year is itself the main result.

**Reliability is what buyers notice.** When buyers bothered to write something, they most often described *reliability*: the item arrived fast, matched its description, and was well packed. In SERVQUAL terms, reliability and tangibles dominate. This fits the trust framework of Mayer et al. (1995): delivering exactly what was promised is direct evidence of a seller's ability and integrity.

**Responsiveness when something goes wrong.** Communication was mentioned less often (6 comments), but it carries special weight. The most telling comment (quote 1) describes a product that *did not work*, yet the buyer still left positive feedback, crediting the seller's quick acceptance of a return. That is the service-recovery pattern: how a seller responds to a problem can matter as much as the problem itself. Communication is also one of the two highest-volume Detailed Seller Ratings (40 ratings), displayed at 5 stars.

**The single complaint.** The shop's only negative entry is a non-delivery complaint about an electric blanket, recorded "More than a year ago." Every entry since is positive. Because eBay's buckets are coarse and there is only one negative entry, this report does not claim the shop *changed because of* that complaint. It is consistent with the sellers' account that they listen to customer feedback, and the sellers' own description of what they changed is recorded below.

**Interpretation of "we listen to our customers."** The sellers attribute their record to listening to customers. The data here supports the *outcome* side of that account (consistent satisfaction, top communication ratings, buyers praising responsiveness) but, as an observational record, cannot prove the cause. The sellers' practices are described in their own words in the next section so readers can judge the connection.

## What we changed (in Henry's words)

> **[PLACEHOLDER — to be written by Henry.]**
> Describe, in your own words, specific things you and your father actually do or changed in response to buyer feedback (for example, how you handle messages, returns, packaging, or listing descriptions), and roughly when. Only include things that really happened.

## Limitations

- **Small sample of written comments.** Only 43 entries contain buyer-written text; 145 are eBay automated positives with no content to analyze.
- **Automated feedback.** eBay automatically leaves positive feedback for orders delivered on time with no issues, which inflates positive counts and contains no buyer opinion.
- **Coarse time information.** eBay shows only four time buckets, not dates, so change over time cannot be measured precisely, and two buckets contain only 1–2 comments.
- **Positive skew.** eBay feedback is known to be overwhelmingly positive (Resnick & Zeckhauser, 2002); dissatisfied buyers may leave no feedback at all.
- **Incomplete capture.** 2 of the 259 listed feedback entries were not captured, and captured counts are slightly lower than eBay's headline totals.
- **Keyword coding.** Themes were coded with keywords, not by trained human raters, so some comments may be miscoded (for example, "fast" in "fast transaction", or one comment coded as communication that says communication "was not necessary"). No inter-rater reliability was computed.
- **Sentiment model limits.** VADER misread the one negative comment as positive, showing it can miss factual complaints.
- **Correlational.** This is an observational analysis. It cannot establish that any seller practice caused the ratings.

## Repository Structure

| Path | Contents |
|---|---|
| `data/raw_feedback_public.json` | Captured public feedback, usernames removed |
| `data/profile_summary.json` | Public profile-level figures |
| `data/buyer_comments.csv` | Cleaned sample: 43 buyer-written comments with themes and sentiment |
| `analysis/codebook.json` | Keyword codebook for theme coding |
| `analysis/analyze.py` | Full analysis script |
| `results/` | Summary tables (CSV) |
| `figures/` | Figures 1–4 |

## References

Hutto, C. J., & Gilbert, E. (2014). VADER: A parsimonious rule-based model for sentiment analysis of social media text. *Proceedings of the International AAAI Conference on Web and Social Media, 8*(1), 216–225.

Mayer, R. C., Davis, J. H., & Schoorman, F. D. (1995). An integrative model of organizational trust. *Academy of Management Review, 20*(3), 709–734.

Parasuraman, A., Zeithaml, V. A., & Berry, L. L. (1988). SERVQUAL: A multiple-item scale for measuring consumer perceptions of service quality. *Journal of Retailing, 64*(1), 12–40.

Resnick, P., & Zeckhauser, R. (2002). Trust among strangers in Internet transactions: Empirical analysis of eBay's reputation system. In M. R. Baye (Ed.), *The economics of the Internet and e-commerce* (Advances in Applied Microeconomics, Vol. 11, pp. 127–157). Elsevier.
