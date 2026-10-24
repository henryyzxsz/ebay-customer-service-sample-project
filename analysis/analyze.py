"""Consumer-psychology analysis of written buyer feedback for eBay seller zhashuzhan.

Input : data/raw_feedback_public.json (public feedback page, as captured) and data/profile_summary.json
Output: data/buyer_comments.csv, results/*.csv, figures/*.png
Buyer usernames are dropped and never written to any output.
"""
import json, re
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ROOT = Path(__file__).resolve().parent.parent
BUCKETS = ["More than a year ago", "Past year", "Past 6 months", "Past month"]  # oldest -> newest

raw = json.load(open(ROOT / "data/raw_feedback_public.json"))
df = pd.DataFrame(raw)

def source(f):
    if f.startswith("Buyer"):
        return "Written by buyers"
    if f.startswith("eBay automated"):
        return "eBay automated"
    return "Received as a buyer (excluded)"

df["source"] = df["from"].map(source)
df = df.drop(columns=["from"])  # remove usernames immediately
(ROOT / "results").mkdir(exist_ok=True)
src_counts = df["source"].value_counts()
src_counts.to_csv(ROOT / "results/feedback_by_source.csv", header=["count"])

# 1. Clean dataset of buyer-written comments only
b = df[df["source"] == "Written by buyers"].copy()
b["comment"] = b["comment"].str.replace(r"\s+", " ", regex=True).str.strip().str.strip("“”\"")
b["item"] = b["item"].str.replace(r"\s*\(#\d+\)", "", regex=True).str.strip()
b["price_usd"] = b["price"].str.replace("US $", "", regex=False).astype(float)
b = b.rename(columns={"when": "time_bucket"})
b["time_bucket"] = pd.Categorical(b["time_bucket"], BUCKETS, ordered=True)

# 2. Theme coding
codebook = {k: v for k, v in json.load(open(ROOT / "analysis/codebook.json")).items() if not k.startswith("_")}
for theme, pats in codebook.items():
    b[theme] = b["comment"].apply(lambda c: int(any(re.search(p, c, re.I) for p in pats)))
themes = list(codebook)
pos = b[b["rating"] == "positive"]
theme_counts = pd.DataFrame({
    "comments_mentioning": pos[themes].sum(),
    "pct_of_positive_comments": (pos[themes].mean() * 100).round(1),
}).sort_values("comments_mentioning", ascending=False)
theme_counts.to_csv(ROOT / "results/theme_counts.csv")

# 3. VADER sentiment
sia = SentimentIntensityAnalyzer()
b["vader_compound"] = b["comment"].apply(lambda c: sia.polarity_scores(c)["compound"])
by_bucket = b.groupby("time_bucket", observed=False).agg(
    n_comments=("comment", "size"),
    mean_vader=("vader_compound", "mean"),
    positive=("rating", lambda s: (s == "positive").sum()),
    negative=("rating", lambda s: (s == "negative").sum()),
).round(3)
by_bucket.to_csv(ROOT / "results/sentiment_by_bucket.csv")

b = b.sort_values("time_bucket")
b[["comment", "rating", "time_bucket", "item", "price_usd", "vader_compound"] + themes].to_csv(
    ROOT / "data/buyer_comments.csv", index=False)

# all public feedback (buyer + automated) by bucket
allfb = df[df["source"] != "Received as a buyer (excluded)"]
pn = pd.crosstab(pd.Categorical(allfb["when"], BUCKETS, ordered=True), allfb["rating"]).reindex(BUCKETS, fill_value=0)
pn.to_csv(ROOT / "results/pos_neg_by_bucket_all_sales_feedback.csv")

# 4. Charts
F = ROOT / "figures"
plt.rcParams.update({"figure.dpi": 150, "font.size": 10})

sales = src_counts.drop("Received as a buyer (excluded)")
sales_pct = (sales / sales.sum() * 100).round(1)
sales_pct.index = ["eBay automated\n(problem-free transactions)", "Written by buyers"]
ax = sales_pct.plot.barh(color=["#7f8c8d", "#2e86c1"], figsize=(7, 2.8))
ax.set_xlim(0, 100); ax.set_xlabel("% of sales feedback")
ax.set_title("Figure 1. Composition of sales feedback")
for i, v in enumerate(sales_pct): ax.text(v + 1, i, f"{v:.1f}%", va="center")
plt.tight_layout(); plt.savefig(F / "fig1_feedback_by_source.png"); plt.close()

tc = theme_counts["pct_of_positive_comments"][::-1]
ax = tc.plot.barh(color="#2e86c1", figsize=(7, 3.6))
ax.set_xlim(0, 100); ax.set_xlabel("%% of positive buyer-written comments mentioning theme (n = %d)" % len(pos))
ax.set_title("Figure 2. What buyers wrote about")
for i, v in enumerate(tc): ax.text(v + 1, i, f"{v:.1f}%", va="center")
plt.tight_layout(); plt.savefig(F / "fig2_theme_frequency.png"); plt.close()

fig, ax = plt.subplots(figsize=(7, 3.6))
ax.bar(range(len(BUCKETS)), by_bucket["mean_vader"], color=["#c0392b" if v < 0 else "#27ae60" for v in by_bucket["mean_vader"]])
ax.set_xticks(range(len(BUCKETS)))
ax.set_xticklabels([f"{k}\n(n = {n})" for k, n in zip(BUCKETS, by_bucket["n_comments"])])
ax.axhline(0, color="black", lw=0.8); ax.set_ylim(-1, 1)
ax.set_ylabel("Mean VADER compound"); ax.set_title("Figure 3. Sentiment of written buyer comments by eBay time bucket")
for i, v in enumerate(by_bucket["mean_vader"]): ax.text(i, v + (0.05 if v >= 0 else -0.1), f"{v:.2f}", ha="center")
plt.tight_layout(); plt.savefig(F / "fig3_sentiment_by_bucket.png"); plt.close()

pn_pct = pn.div(pn.sum(axis=1), axis=0) * 100
pn_pct.to_csv(ROOT / "results/pos_neg_pct_by_bucket_all_sales_feedback.csv")
ax = pn_pct.plot.bar(stacked=True, color={"positive": "#27ae60", "negative": "#c0392b"}, figsize=(7, 3.6), rot=0)
ax.set_ylim(0, 105); ax.set_ylabel("% of sales feedback in bucket")
ax.set_title("Figure 4. Positive vs. negative sales feedback by eBay time bucket")
for i, v in enumerate(pn_pct["positive"]): ax.text(i, min(v, 100) + 1 if v > 0 else 1, f"{v:.0f}% positive", ha="center", fontsize=8)
ax.legend(loc="lower right")
ax.set_xticklabels([f"{k}\n(n = {n})" for k, n in zip(BUCKETS, pn.sum(axis=1))])
ax.set_xlabel("")
plt.tight_layout(); plt.savefig(F / "fig4_pos_neg_by_bucket.png"); plt.close()

print(src_counts, "\n", theme_counts, "\n", by_bucket, "\n", pn)
print("overall mean VADER (positive comments):", round(pos["vader_compound"].mean() if "vader_compound" in pos else b[b.rating=="positive"].vader_compound.mean(), 3))
print("overall mean VADER (all):", round(b.vader_compound.mean(), 3))
print("comments with 2+ themes excl. general praise:", int((b[b.rating=='positive'][themes[:-1]].sum(axis=1) >= 2).sum()))
print("comments mentioning any of shipping/described/packaging:", int((b[b.rating=='positive'][themes[:4]].sum(axis=1) >= 1).sum()))
