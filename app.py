import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Global CO₂ Emissions Dashboard",
    layout="wide"
)


# Title and introduction

st.title("🌍 Global CO₂ Emissions Interactive Dashboard")

st.markdown("""
### Project Goal
This dashboard enables interactive exploration of global CO₂ emissions across countries
and over time. Users can compare total emissions, per-capita emissions, population,
and GDP to better understand global climate patterns.

**Data Source:** Our World in Data (University of Oxford)
""")

# Load dataset

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    return pd.read_csv(url)

df = load_data()


df = df[df["iso_code"].str.len() == 3]


# Sidebar controls (INTERACTIVITY)

st.sidebar.header("🔧 Interactive Controls")

countries = sorted(df["country"].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=["United States", "China", "India"]
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (1990, 2020)
)

metric_options = {
    "Total CO₂ Emissions (million tonnes)": "co2",
    "CO₂ Emissions per Capita": "co2_per_capita",
    "Population": "population",
    "GDP": "gdp"
}

selected_metric = st.sidebar.selectbox(
    "Select Metric",
    list(metric_options.keys())
)

metric = metric_options[selected_metric]

# Filter data

filtered_df = df[
    (df["country"].isin(selected_countries)) &
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]


# Line chart (trend over time)

st.subheader("📈 Trends Over Time")

line_fig = px.line(
    filtered_df,
    x="year",
    y=metric,
    color="country",
    markers=True,
    labels={
        "year": "Year",
        metric: selected_metric
    }
)

line_fig.update_layout(
    hovermode="x unified",
    height=500
)

st.plotly_chart(line_fig, use_container_width=True)


# Map visualization (latest year)

st.subheader("🗺️ Global Distribution (Latest Selected Year)")

latest_year = filtered_df["year"].max()
map_df = filtered_df[filtered_df["year"] == latest_year]

map_fig = px.choropleth(
    map_df,
    locations="iso_code",
    color=metric,
    hover_name="country",
    color_continuous_scale="Reds",
    labels={metric: selected_metric}
)

map_fig.update_layout(height=500)

st.plotly_chart(map_fig, use_container_width=True)


# Data table (details-on-demand)

st.subheader("📋 Data Table")

st.dataframe(
    map_df[["country", "year", metric]]
    .sort_values(metric, ascending=False),
    use_container_width=True
)


# Narrative and conclusion

st.markdown("""
### Key Insights
- Large economies tend to produce higher total emissions.
- Per-capita emissions reveal different patterns across countries.
- Interactive visualizations reveal trends not visible in static charts.

### Future Improvements
- Add renewable energy indicators
- Include emission forecasting
- Highlight major climate policy milestones
""")

st.markdown("---")
st.markdown("**Final Project – Interactive Visualization using Streamlit**")
