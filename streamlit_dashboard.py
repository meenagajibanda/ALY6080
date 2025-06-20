
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load data
df = pd.read_csv('cleaned_foot_traffic_smallest.csv')  # Replace with your actual CSV filename

# Preprocessing
df = df.dropna(subset=['percentage_difference_normalized', 'avg_weekday_visits', 'avg_weekend_visits', 'top_category'])
df = df[df['avg_weekday_visits'] > 0]

# Encode categorical feature
df_encoded = pd.get_dummies(df[['avg_weekday_visits', 'avg_weekend_visits', 'top_category']], drop_first=True)
X = df_encoded
y = df['percentage_difference_normalized']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=50, n_jobs=-1, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Streamlit App
st.title("🚦 Foot Traffic Pattern Dashboard")
st.markdown("This app predicts the normalized percentage difference between average weekend and weekday visits across industries.")

# Performance Metrics
st.subheader("✅ Model Performance")
st.write(f"**MAE:** {mean_absolute_error(y_test, y_pred):.2f}")
st.write(f"**RMSE:** {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
st.write(f"**R² Score:** {r2_score(y_test, y_pred):.4f}")

# Actual vs Predicted Plot
st.subheader("📊 Actual vs Predicted")
fig1, ax1 = plt.subplots()
sns.scatterplot(x=y_test, y=y_pred, alpha=0.5, ax=ax1)
ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r')
ax1.set_xlabel("Actual")
ax1.set_ylabel("Predicted")
st.pyplot(fig1)

# Bar Chart by Category
st.subheader("📈 Average Percentage Difference by Category")
avg_diff = df.groupby('top_category')['percentage_difference_normalized'].mean().sort_values()
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x=avg_diff.values, y=avg_diff.index, ax=ax2)
ax2.set_xlabel("% Difference")
st.pyplot(fig2)

# Category Filter
st.subheader("🔎 Explore by Category")
selected_cat = st.selectbox("Select a Category to Explore", sorted(df['top_category'].unique()))
cat_df = df[df['top_category'] == selected_cat]
st.write(f"Showing {len(cat_df)} records for **{selected_cat}**")
st.dataframe(cat_df[['avg_weekday_visits', 'avg_weekend_visits', 'percentage_difference_normalized']])

# Feature Importance
st.subheader("📌 Feature Importance (Top 10)")
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False).head(10)
st.bar_chart(importances)
