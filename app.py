import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Market Gap Analysis", layout="wide")

st.title("The Sugar Trap — Market Gap Analysis")
st.markdown("**Client:** Helix CPG Partners | **Analyst:** Esther")
st.markdown("---")

st.success("Dashboard is live and working!")

st.markdown("### Sample Chart")

sample_data = {
    "Category": ["Sweet & Sugary Snacks", "Sports & Protein", "Dairy", "Grains & Carbs", "Fruits, Veg & Nuts", "Meat & Fish"],
    "Avg Sugar": [26.5, 7.4, 8.8, 8.3, 8.1, 1.9],
    "Avg Protein": [5.9, 31.0, 7.0, 9.2, 6.1, 16.8]
}

df = pd.DataFrame(sample_data)

fig = px.bar(df, x="Category", y=["Avg Sugar", "Avg Protein"],
             barmode="group",
             title="Market Saturation Index")
st.plotly_chart(fig, use_container_width=True)
