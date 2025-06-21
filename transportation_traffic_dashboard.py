# transportation_dashboard.py

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Read dataset
df = pd.read_csv("cleaned_foot_traffic_smallest.csv")

# Clean and process
df['visits_by_day'] = df['visits_by_day'].apply(eval)
df['weekday_visits'] = df['visits_by_day'].apply(lambda x: sum(x[:5]))
df['weekend_visits'] = df['visits_by_day'].apply(lambda x: sum(x[5:]))
df['avg_weekday_visits'] = df['weekday_visits'] / 5
df['avg_weekend_visits'] = df['weekend_visits'] / 2
df['percentage_difference'] = df.apply(
    lambda row: ((row['avg_weekend_visits'] - row['avg_weekday_visits']) / row['avg_weekday_visits']) * 100
    if row['avg_weekday_visits'] != 0 else 0, axis=1
)

# Filter only transportation-related categories
transport_keywords = ['transport', 'airport', 'station', 'bus', 'rail', 'subway', 'transit']
df_transport = df[df['top_category'].str.contains('|'.join(transport_keywords), case=False, na=False)]

# Classification column
df_transport['traffic_pattern'] = df_transport.apply(
    lambda row: 'Weekend-heavy' if row['avg_weekend_visits'] > row['avg_weekday_visits'] else 'Weekday-heavy',
    axis=1
)

st.title("Transportation Hub Traffic Analysis Dashboard")

# Sidebar filters
with st.sidebar:
    selected_pattern = st.selectbox("Select Traffic Pattern", ['All', 'Weekday-heavy', 'Weekend-heavy'])
    selected_categories = st.multiselect("Select Top Categories", df_transport['top_category'].unique(),
                                         default=df_transport['top_category'].unique())

# Apply filters
df_filtered = df_transport[df_transport['top_category'].isin(selected_categories)]
if selected_pattern != 'All':
    df_filtered = df_filtered[df_filtered['traffic_pattern'] == selected_pattern]

# Graph 1: Top Weekend Traffic Categories
weekend_top = df_filtered.groupby('top_category')['weekend_visits'].sum().nlargest(10).reset_index()
fig1 = px.bar(weekend_top, x='top_category', y='weekend_visits',
              title="Top Categories by Weekend Traffic", labels={'weekend_visits': 'Weekend Visits'},
              color='weekend_visits')

# Graph 2: Top Weekday Traffic Categories
weekday_top = df_filtered.groupby('top_category')['weekday_visits'].sum().nlargest(10).reset_index()
fig2 = px.bar(weekday_top, x='top_category', y='weekday_visits',
              title="Top Categories by Weekday Traffic", labels={'weekday_visits': 'Weekday Visits'},
              color='weekday_visits')

# Graph 3: Percentage Difference
diff_avg = df_filtered.groupby('top_category')['percentage_difference'].mean().sort_values(ascending=False).head(10).reset_index()
fig3 = px.bar(diff_avg, x='top_category', y='percentage_difference',
              title="Avg. % Difference (Weekend vs Weekday)", color='percentage_difference',
              labels={'percentage_difference': 'Percentage Difference (%)'})

# Graph 4: Map
fig4 = px.scatter_mapbox(df_filtered, lat="latitude", lon="longitude", hover_name="top_category",
                         hover_data=["traffic_pattern", "weekday_visits", "weekend_visits"],
                         color="traffic_pattern", zoom=9, height=500)
fig4.update_layout(mapbox_style="carto-positron")
fig4.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, title="Geographic Distribution of Transportation Hubs")

# Layout: 2x2 grid
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    st.plotly_chart(fig4, use_container_width=True)
