import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="NYC Transportation Hubs Traffic Analysis", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_foot_traffic_smallest")  # <-- Make sure this CSV is uploaded

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_categories = st.sidebar.multiselect(
    "Select Transportation Categories",
    options=sorted(df['top_category'].unique()),
    default=sorted(df['top_category'].unique())
)

traffic_filter = st.sidebar.radio(
    "Select Traffic Pattern",
    options=["All", "Weekday-heavy", "Weekend-heavy"]
)

# Filter data
filtered_df = df[df['top_category'].isin(selected_categories)]
if traffic_filter != "All":
    filtered_df = filtered_df[filtered_df["traffic_pattern"] == traffic_filter]

# Title
st.title("NYC Transportation Hubs Traffic Analysis")

# Traffic pattern counts
st.subheader("Top Categories - Traffic Distribution")
traffic_counts = (
    filtered_df.groupby(["top_category", "traffic_pattern"])
    .size()
    .reset_index(name="count")
)
fig_bar = px.bar(
    traffic_counts,
    x="top_category",
    y="count",
    color="traffic_pattern",
    barmode="group",
    title="Traffic Pattern by Transportation Category"
)
fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar, use_container_width=True)

# Map section
st.subheader("Geographical Distribution of Transportation Hubs")
fig_map = px.scatter_mapbox(
    filtered_df,
    lat="latitude",
    lon="longitude",
    color="traffic_pattern",
    hover_name="location_name",
    hover_data=["top_category", "weekday_visits", "weekend_visits", "percentage_difference_normalized"],
    zoom=10,
    center={"lat": 40.7128, "lon": -74.0060},
    height=600
)
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
st.plotly_chart(fig_map, use_container_width=True)

# Dashboard note
st.markdown("This dashboard compares weekday and weekend traffic across NYC transportation hubs based on foot traffic patterns.")
