# The Sugar Trap — Snack Market Gap Analysis
### Helix CPG Partners | Strategic Food & Beverage Consultancy

---

## A. Executive Summary

Analysis of 12,645 genuine snack products from the Open Food Facts database
reveals a clear and significant Blue Ocean in the snack market: only 7.6% of
products currently occupy the high-protein (>15g), low-sugar (<10g) space.
The market is heavily dominated by Candy & Chocolate products (42.1% of all
snacks), with an average sugar content of 26.2g per 100g across the entire
snack aisle — more than three times the average protein content of 7.5g.
The biggest market opportunity lies in the Nuts & Seeds
category, where demand for healthier, high-protein snacking is not being met
by current product offerings.
A new snack product targeting above 15g protein and below 10g sugar would
face minimal direct competition and would serve a fast-growing consumer segment
prioritising functional nutrition over indulgence.

---

## B. Project Links

- **Notebook:** [Google Colab — Sugar Trap EDA](https://colab.research.google.com/drive/1K7FcNy8eb1EWa2bN8-bXSYfmUSBBtYQG?usp=sharing)
- **Dashboard:** [Streamlit — Sugar Trap Dashboard](https://mgabackup-psh4scjtimzsa23etkgkge.streamlit.app/)
- **Presentation:** [Slide Deck — PDF](https://docs.google.com/presentation/d/1vCXjfQZy568ZCLzTAR1C9HUx-wA7SRHJi90C57k5i0Q/edit?usp=sharing)


> All links are publicly accessible. Verified in incognito mode.

---

## C. Technical Explanation

### Data Cleaning

The raw dataset contained 500,000 rows loaded from the Open Food Facts `.csv.gz`
file using a chunked pandas read to manage memory. Cleaning was performed in
three steps:

1. **Null removal** — dropped all rows where `product_name`, `sugars_100g`,
   or `proteins_100g` were null, reducing the dataset to 95,379 rows.
2. **Outlier removal** — filtered out biologically impossible values by
   keeping only rows where all nutrient columns (`sugars_100g`,
   `proteins_100g`, `fat_100g`) fell within the 0–100g per 100g range.
3. **Snack-only filtering** — the `categories_tags` column was parsed using
   a keyword-matching function to assign each product a `primary_category`.
   Products tagged as staple groceries (bread, pasta, condiments, meals,
   meats) were labelled `Drop` and removed entirely, since the client brief
   is specifically about the snack aisle. Products with null `categories_tags`
   were also dropped as they could not be reliably categorised. This reduced
   the dataset to 12,645 verified snack products across 9 clean categories
   with zero uncategorised rows.

### Candidate's Choice — Nutritional Fingerprint Heatmap

As the Candidate's Choice addition, I built a **nutritional fingerprint
heatmap** showing the average Sugar, Protein, and Fat content per snack
category side by side.

**Why this adds value:** The scatter plot shows where individual products sit —
but a client executive or R&D director needs to understand the *category-level
signature* at a glance. The heatmap makes it immediately obvious which
categories are nutritionally weakest (high sugar, low protein) and therefore
most ripe for disruption, without needing to interpret hundreds of individual
data points. In a client presentation, this is the slide that drives the
strategic conversation — it takes 5 seconds to read and communicates the
entire opportunity landscape. It is included both in the notebook (Section 8)
and as a live interactive chart in the Streamlit dashboard, where it responds
dynamically to the category filter.

---

*Data source: [Open Food Facts](https://world.openfoodfacts.org/data) —
open database of food products worldwide.*
*Analysis completed as part of the Helix CPG Partners data engineering
assessment.*
