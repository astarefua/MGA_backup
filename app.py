import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Market Gap Analysis", layout="wide")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/astarefua/MGA_backup/main/clean_food_data.csv"
    df = pd.read_csv(url)
    return df

# ── HEADER ─────────────────────────────────────────────────────────
st.title("The Sugar Trap — Market Gap Analysis")
st.markdown("**Client:** Helix CPG Partners | **Analyst:** Esther")
st.markdown("---")

# ── LOAD DATA ──────────────────────────────────────────────────────
with st.spinner("Loading data..."):
    df = load_data()

# ── KEY INSIGHT BOX ────────────────────────────────────────────────
st.markdown("### Key Insight")
st.success(
    "Based on the data, the biggest market opportunity is in the **Fruits, Veg & Nuts** category, "
    "specifically targeting products with **24g of protein** and less than **3g of sugar** per 100g. "
    "Only **3.6%** of analysed products occupy this high-protein, low-sugar space — "
    "a clear Blue Ocean for a new healthy snacking line."
)

# ── METRICS ROW ────────────────────────────────────────────────────
st.markdown("### Dataset Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", f"{len(df):,}")
col2.metric("Blue Ocean Products", "1,334")
col3.metric("Blue Ocean %", "3.6%")
col4.metric("Top Protein Source", "Peanuts")
st.markdown("---")

# ── SCATTER PLOT ───────────────────────────────────────────────────
st.markdown("### Nutrient Matrix — Sugar vs Protein by Category")

df_plot = df[~df["primary_category"].isin(["Unknown","Other"])]
categories = sorted(df_plot["primary_category"].unique().tolist())
selected = st.multiselect("Filter by category:", options=categories, default=categories)
df_filtered = df_plot[df_plot["primary_category"].isin(selected)]

fig1 = px.scatter(
    df_filtered,
    x="sugars_100g", y="proteins_100g",
    color="primary_category",
    title="Sugar vs Protein — each dot is one product",
    labels={"sugars_100g":"Sugar per 100g",
            "proteins_100g":"Protein per 100g",
            "primary_category":"Category"},
    opacity=0.5,
    hover_data=["product_name"]
)
fig1.add_hline(y=15, line_dash="dash", line_color="gray",
               annotation_text="High Protein threshold")
fig1.add_vline(x=10, line_dash="dash", line_color="gray",
               annotation_text="Low Sugar threshold")
st.plotly_chart(fig1, use_container_width=True)
st.markdown("---")

# ── MARKET SATURATION INDEX ─────────────────────────────────────────
st.markdown("### Market Saturation Index — Candidate's Choice")
st.caption(
    "Why I added this: the scatter plot shows individual products. "
    "This chart gives executives a clean category-level summary — "
    "showing exactly which categories are oversaturated with sugar "
    "and which are protein deserts."
)

summary = df[~df["primary_category"].isin(["Unknown","Other"])].groupby("primary_category").agg(
    avg_sugar=("sugars_100g","mean"),
    avg_protein=("proteins_100g","mean"),
    product_count=("product_name","count")
).round(1).reset_index()

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    name="Avg Sugar (g)",
    x=summary["primary_category"],
    y=summary["avg_sugar"],
    marker_color="#E8593C",
    text=summary["avg_sugar"],
    textposition="outside"
))
fig2.add_trace(go.Bar(
    name="Avg Protein (g)",
    x=summary["primary_category"],
    y=summary["avg_protein"],
    marker_color="#1D9E75",
    text=summary["avg_protein"],
    textposition="outside"
))
fig2.update_layout(
    barmode="group",
    xaxis_title="Category",
    yaxis_title="Grams per 100g",
    plot_bgcolor="white",
    yaxis=dict(gridcolor="#eeeeee")
)
st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")

# ── TOP PROTEIN SOURCES ────────────────────────────────────────────
st.markdown("### Top Protein Sources in Blue Ocean Products")

protein_data = {
    "Ingredient": ["Peanuts","Soy","Almonds","Sunflower Seeds","Whey","Sesame","Cashew","Egg"],
    "Products":   [378, 214, 158, 153, 66, 61, 41, 35]
}
df_protein = pd.DataFrame(protein_data)

fig3 = px.bar(
    df_protein,
    x="Products", y="Ingredient",
    orientation="h",
    title="Most common protein sources in High Protein + Low Sugar products",
    color="Products",
    color_continuous_scale=["#9FE1CB","#0F6E56"]
)
fig3.update_layout(plot_bgcolor="white", yaxis=dict(categoryorder="total ascending"))
st.plotly_chart(fig3, use_container_width=True)
