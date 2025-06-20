import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("your_cleaned_ny_data.csv")  # Replace with your actual cleaned dataset path

# Only include transportation hubs
transportation_categories = [
    'Air Transportation',
    'Rail Transportation',
    'Transit and Ground Passenger Transportation',
    'Support Activities for Transportation',
    'Postal Service',
    'Couriers and Messengers',
    'Warehousing and Storage'
]
df = df[df['top_category'].isin(transportation_categories)]

# Determine traffic pattern
df['traffic_pattern'] = df.apply(lambda row: 'Weekend-heavy' if row['weekend_visits'] > row['weekday_visits'] else 'Weekday-heavy', axis=1)

# Sidebar filters
st.sidebar.title("Filters")
selected_pattern = st.sidebar.radio("Select Traffic Pattern", ['All', 'Weekday-heavy', 'Weekend-heavy'])

if selected_pattern != 'All':
    df = df[df['traffic_pattern'] == selected_pattern]

# Main Title
st.title("NYC Transportation Hubs Traffic Analysis")

# Bar Chart - Top Categories by Traffic Pattern
st.subheader("Top Categories - Traffic Distribution")
category_counts = df.groupby(['top_category', 'traffic_pattern']).size().reset_index(name='counts')
fig_bar = px.bar(category_counts, x='top_category', y='counts', color='traffic_pattern', barmode='group')
fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar)

# Map Visualization
st.subheader("Geographical Distribution of Transportation Hubs")
fig_map = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="traffic_pattern",
    hover_name="location_name",
    hover_data=["top_category", "weekday_visits", "weekend_visits"],
    zoom=10,
    height=600
)
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map)

# Notes
st.markdown("This dashboard provides a comparison between weekday and weekend traffic across transportation hubs in NYC based on foot traffic patterns.")
