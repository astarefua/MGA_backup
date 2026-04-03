import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Sugar Trap Dashboard",
    page_icon="🥤",
    layout="wide"
)

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('snack_data_clean.csv')

df = load_data()

# ── Palette — matches your 9 final categories exactly ─────────
PALETTE = {
    'Candy & Chocolate':      '#9b59b6',
    'Cereals & Granola':      '#1abc9c',
    'Chips & Savoury Snacks': '#e74c3c',
    'Nuts & Seeds':           '#f39c12',
    'Spreads & Dips':         '#795548',
    'Ice Cream & Frozen':     '#00bcd4',
    'Fruit Snacks':           '#3498db',
    'Baked Goods & Biscuits': '#e67e22',
    'Protein & Sport':        '#2ecc71',
}

# ── Header ────────────────────────────────────────────────────
st.markdown(
    "<h2 style='margin-bottom:0'>🥤 The Sugar Trap — Snack Market Gap Analysis</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='margin-top:25px; margin-bottom:2px;'>"
    "<em>Identifying the Blue Ocean in the snack aisle for Helix CPG Partners</em></p>",
    unsafe_allow_html=True
)
st.divider()

# ── Sidebar filters ───────────────────────────────────────────
st.sidebar.header("Filters")

all_categories = sorted(df['primary_category'].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Select categories",
    options=all_categories,
    default=all_categories
)

sugar_max = st.sidebar.slider(
    "Max sugar (g per 100g)",
    min_value=0, max_value=100, value=100
)

protein_min = st.sidebar.slider(
    "Min protein (g per 100g)",
    min_value=0, max_value=100, value=0
)

st.sidebar.divider()
st.sidebar.caption(
    f"Dataset: {len(df):,} snack products · "
    f"{df['primary_category'].nunique()} categories · "
    "Source: Open Food Facts"
)

# ── Filter ────────────────────────────────────────────────────
filtered = df[
    (df['primary_category'].isin(selected_categories)) &
    (df['sugars_100g'] <= sugar_max) &
    (df['proteins_100g'] >= protein_min)
].copy()

# ── KPI cards ─────────────────────────────────────────────────
# blue_ocean     = filtered[(filtered['sugars_100g'] < 10) & (filtered['proteins_100g'] > 15)]
# blue_ocean_pct = len(blue_ocean) / len(filtered) * 100 if len(filtered) > 0 else 0
# avg_market_sugar = filtered['sugars_100g'].mean() if len(filtered) > 0 else 0

blue_ocean     = df[(df['sugars_100g'] < 10) & (df['proteins_100g'] > 15)]
blue_ocean_pct = len(blue_ocean) / len(df) * 100
avg_market_sugar   = df['sugars_100g'].mean()
avg_market_protein = df['proteins_100g'].mean()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total snack products",   f"{len(df):,}")
c2.metric("Filtered products",      f"{len(filtered):,}")
c3.metric("Blue ocean products",    f"{len(blue_ocean):,}")
c4.metric("Blue ocean share",       f"{blue_ocean_pct:.1f}%",
          delta="market gap")
c5.metric("Avg market sugar",       f"{avg_market_sugar:.1f}g",
          delta=f"vs {df['proteins_100g'].mean():.1f}g protein",
          delta_color="off")

st.divider()

# ── Scatter plot ──────────────────────────────────────────────
st.subheader("Nutrient Matrix — Sugar vs Protein by Category")

if filtered.empty:
    st.warning("No products match the current filters. Adjust the sidebar sliders.")
else:
    fig, ax = plt.subplots(figsize=(13, 8))

    plot_sample = (
        filtered.sample(n=min(4000, len(filtered)), random_state=42)
        if len(filtered) > 4000 else filtered
    )

    for category, group in plot_sample.groupby('primary_category'):
        ax.scatter(
            group['sugars_100g'],
            group['proteins_100g'],
            label=f"{category} ({len(group):,})",
            alpha=0.5,
            s=22,
            color=PALETTE.get(category, '#95a5a6')
        )

    # Blue ocean quadrant
    ax.axvline(x=10, color='green', linestyle='--', linewidth=1.8, alpha=0.8)
    ax.axhline(y=15, color='green', linestyle='--', linewidth=1.8, alpha=0.8)
    ax.fill_between([0, 10], [15, 15], [100, 100], alpha=0.07, color='green')

    ax.text(0.5, 88,
            'BLUE OCEAN\nHigh Protein + Low Sugar\n(Market Opportunity)',
            fontsize=10, color='#1a7a3c', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#d5f5e3',
                      alpha=0.9, edgecolor='#2ecc71'))

    ax.text(52, 3,
            'SUGAR TRAP\nLow Protein + High Sugar\n(Overcrowded)',
            fontsize=10, color='#7b241c', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#fadbd8',
                      alpha=0.9, edgecolor='#e74c3c'))

    ax.set_xlabel('Sugar per 100g (g)', fontsize=12)
    ax.set_ylabel('Protein per 100g (g)', fontsize=12)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right', fontsize=8.5, framealpha=0.85,
              title='Category (n shown)', title_fontsize=9)
    ax.grid(True, alpha=0.15)
    ax.set_title(
        'Each dot = one snack product  |  Green zone = Blue Ocean  |  '
        'Use sidebar filters to explore',
        fontsize=10, color='#555', style='italic'
    )

    st.pyplot(fig)
    plt.close()

st.divider()

# ── Two charts side by side ───────────────────────────────────
left, right = st.columns(2)

# Left — category breakdown
# with left:
#     st.markdown("<h4 style='margin-bottom:0'>Products per category</h4>", unsafe_allow_html=True)
#     st.caption("Distribution of snack products across categories in the dataset")
#     cat_counts = filtered['primary_category'].value_counts()

#     fig2, ax2 = plt.subplots(figsize=(6, 5))
#     if cat_counts.empty:
#         ax2.text(0.5, 0.5, 'No categories selected',
#                  ha='center', va='center', fontsize=12)
#         ax2.axis('off')
#     else:
#         colors = [PALETTE.get(c, '#95a5a6') for c in cat_counts.index]
#         bars = ax2.barh(cat_counts.index, cat_counts.values,
#                         color=colors, edgecolor='white', height=0.65)
#         for bar, n in zip(bars, cat_counts.values):
#             ax2.text(bar.get_width() + 8, bar.get_y() + bar.get_height()/2,
#                      f'{n:,}', va='center', fontsize=9)
#         ax2.set_xlabel('Number of products')
#         ax2.set_xlim(0, cat_counts.max() * 1.15)
#         ax2.grid(axis='x', alpha=0.3)
#         ax2.spines[['top', 'right']].set_visible(False)

#     st.pyplot(fig2)
#     plt.close()
    

# Right — nutritional fingerprint heatmap
# with right:
    st.markdown("<h4 style='margin-bottom:0'>Nutritional fingerprint by category</h4>", unsafe_allow_html=True)
    st.caption("Candidate's choice — avg Sugar, Protein & Fat per segment for R&D")
    heat_data = (
        filtered
        .groupby('primary_category')
        .agg(Sugar=('sugars_100g', 'mean'),
             Protein=('proteins_100g', 'mean'),
             Fat=('fat_100g', 'mean'))
        .round(1)
        .sort_values('Protein', ascending=False)
    )

    fig3, ax3 = plt.subplots(figsize=(6, 5))
    if heat_data.empty:
        ax3.text(0.5, 0.5, 'No categories selected',
                 ha='center', va='center', fontsize=12)
        ax3.axis('off')
    else:
        sns.heatmap(
            heat_data,
            annot=True, fmt='.1f',
            cmap='RdYlGn_r',
            linewidths=0.5,
            ax=ax3,
            cbar_kws={'label': 'g per 100g'},
            annot_kws={'size': 11}
        )
        ax3.set_ylabel('')
        ax3.tick_params(axis='y', rotation=0)

    st.pyplot(fig3)
    plt.close()

st.divider()

# ── Nutri-Score breakdown ─────────────────────────────────────
st.subheader("Nutri-Score Distribution")
st.caption("How healthy is the current snack market? A = healthiest, E = least healthy")

nutri = (
    filtered['nutriscore_grade']
    .str.lower().str.strip()
    .pipe(lambda s: s[s.isin(['a', 'b', 'c', 'd', 'e'])])
)
grade_counts = nutri.value_counts().reindex(['a', 'b', 'c', 'd', 'e']).fillna(0)
grade_colors = {'a': '#27ae60', 'b': '#82c341', 'c': '#f4d03f',
                'd': '#e67e22', 'e': '#e74c3c'}

fig4, ax4 = plt.subplots(figsize=(8, 3.5))
bars = ax4.bar(
    grade_counts.index,
    grade_counts.values,
    color=[grade_colors[g] for g in grade_counts.index],
    edgecolor='white', width=0.6
)
for bar, n in zip(bars, grade_counts.values):
    if n > 0:
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                 f'{int(n):,}', ha='center', fontsize=10)
ax4.set_xlabel('Nutri-Score Grade')
ax4.set_ylabel('Number of products')
ax4.grid(axis='y', alpha=0.3)
ax4.spines[['top', 'right']].set_visible(False)

st.pyplot(fig4)
plt.close()

st.divider()

# ── Key insight ───────────────────────────────────────────────
st.subheader("Key Insight")

if len(blue_ocean) > 0:
    top_cat   = blue_ocean['primary_category'].value_counts().idxmax()
    avg_prot  = round(blue_ocean['proteins_100g'].mean(), 1)
    avg_sugar = round(blue_ocean['sugars_100g'].mean(), 1)

    st.success(
        f"📊 Based on **{len(df):,} snack products** analysed, the biggest market "
        f"opportunity is in **{top_cat}**, specifically targeting products with "
        f"**{avg_prot}g of protein** and less than **{avg_sugar}g of sugar**. "
        f"Only **{blue_ocean_pct:.1f}%** of current products occupy this "
        f"high-protein, low-sugar space — confirming a significant Blue Ocean opportunity."
    )

    # Show the actual blue ocean products as a table
    with st.expander("View Blue Ocean products in the dataset"):
        bo_display = (
            blue_ocean[['product_name', 'primary_category',
                        'proteins_100g', 'sugars_100g', 'fat_100g', 'nutriscore_grade']]
            .sort_values('proteins_100g', ascending=False)
            .reset_index(drop=True)
        )
        bo_display.columns = ['Product', 'Category', 'Protein (g)', 'Sugar (g)',
                              'Fat (g)', 'Nutri-Score']
        st.dataframe(bo_display, use_container_width=True)
else:
    st.info("No Blue Ocean products found with current filters.")

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.caption("Data source: Open Food Facts | Analysis by Helix CPG Partners | "
           f"Dataset: {len(df):,} snack products across {df['primary_category'].nunique()} categories")
