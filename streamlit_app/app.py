# ================================
# FINAL STREAMLIT DASHBOARD
# ================================

import os
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------
# LOAD DATA
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
data_path = os.path.join(ROOT_DIR, "data", "engineered_food_delivery.csv")

df = pd.read_csv(data_path)
df.columns = df.columns.str.strip().str.lower()

# -------------------------------
# TITLE
# -------------------------------
st.markdown("""
<h1 style='text-align: center; color: #FF4B4B;'>🍔 Online Food Delivery Analysis</h1>
<h4 style='text-align: center; color: gray;'>Data-Driven Business Insights Dashboard</h4>
""", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# KPI SECTION
# -------------------------------
col1, col2, col3 = st.columns(3)
col4, col5, col6, col7 = st.columns(4)

col1.metric("Total Orders", f"{len(df):,}")
col2.metric("Total Revenue", f"{df['order_value'].sum():,.0f}")
col3.metric("Avg Order Value", f"{df['order_value'].mean():,.2f}")
col4.metric("Avg Delivery Time", f"{df['delivery_time_min'].mean():.1f} min")
col5.metric("Cancellation Rate", f"{(df['order_status']=='Cancelled').mean()*100:.2f}%")
col6.metric("Avg Delivery Rating", f"{df['delivery_rating'].mean():.2f}")
col7.metric("Profit Margin %", f"{df['profit_margin_percent'].mean():.2f}%")

st.markdown("---")

# -------------------------------
# FILTER
# -------------------------------
city = st.selectbox("📍 Select City", sorted(df["city"].dropna().unique()))
df_city = df[df["city"] == city]

# -------------------------------
# ROW 1
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    cuisine_data = df_city.groupby("cuisine_type")["order_value"].sum().reset_index()
    fig1 = px.bar(cuisine_data, x="cuisine_type", y="order_value",
                  title="Revenue by Cuisine", color="cuisine_type")
    st.plotly_chart(fig1, width="stretch")

with col2:
    city_revenue = df.groupby("city")["order_value"].sum().reset_index().sort_values(by="order_value", ascending=False).head(10)
    fig2 = px.bar(city_revenue, x="city", y="order_value",
                  title="Top Cities by Revenue", color="city")
    st.plotly_chart(fig2, width="stretch")

# -------------------------------
# ROW 2
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    age_data = df_city["customer_age_group"].value_counts().reset_index()
    age_data.columns = ["age_group", "count"]
    fig3 = px.pie(age_data, names="age_group", values="count", title="Customer Age Group")
    st.plotly_chart(fig3, width="stretch")

with col2:
    hour_data = df_city["order_hour"].value_counts().sort_index().reset_index()
    hour_data.columns = ["hour", "orders"]
    fig4 = px.line(hour_data, x="hour", y="orders", markers=True,
                   title="Order Trend by Hour")
    st.plotly_chart(fig4, width="stretch")

# -------------------------------
# ROW 3
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    rest_data = df_city.groupby("restaurant_name")["order_value"].sum().reset_index().sort_values(by="order_value", ascending=False).head(10)
    fig5 = px.bar(rest_data, x="restaurant_name", y="order_value",
                  title="Top Restaurants by Revenue")
    st.plotly_chart(fig5, width="stretch")

with col2:
    cancel_data = df_city[df_city["order_status"]=="Cancelled"]["restaurant_name"].value_counts().head(10).reset_index()
    cancel_data.columns = ["restaurant","cancellations"]
    fig6 = px.bar(cancel_data, x="restaurant", y="cancellations",
                  title="Top Restaurants by Cancellation", color_discrete_sequence=["#FF4B4B"])
    st.plotly_chart(fig6, width="stretch")

# -------------------------------
# ROW 4 (DELIVERY)
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    fig7 = px.scatter(df_city, x="distance_km", y="delivery_time_min",
                      title="Distance vs Delivery Time",
                      color_discrete_sequence=["#00BFA6"])
    fig7.update_traces(marker=dict(size=6, opacity=0.5))
    st.plotly_chart(fig7, width="stretch")

with col2:
    monthly = df_city.groupby("order_month")["order_value"].sum().reset_index()
    fig8 = px.line(monthly, x="order_month", y="order_value", markers=True,
                   title="Monthly Revenue Trend")
    fig8.update_traces(line=dict(color="#00C853", width=3))
    st.plotly_chart(fig8, width="stretch")

# -------------------------------
# NEW CHARTS (IMPORTANT 🔥)
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    fig9 = px.scatter(df_city, x="delivery_time_min", y="delivery_rating",
                      title="Delivery Time vs Rating",
                      color_discrete_sequence=["#FF5733"])
    fig9.update_traces(marker=dict(size=6, opacity=0.5))
    st.plotly_chart(fig9, width="stretch")

with col2:
    fig10 = px.scatter(df_city, x="discount_applied", y="profit_margin_percent",
                       title="Discount vs Profit",
                       color_discrete_sequence=["#00C853"])
    fig10.update_traces(marker=dict(size=6, opacity=0.5))
    st.plotly_chart(fig10, width="stretch")

# -------------------------------
# ROW 5
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    week_data = df_city["order_weekday"].value_counts().reset_index()
    week_data.columns = ["day","orders"]
    fig11 = px.bar(week_data, x="day", y="orders",
                   title="Orders by Weekday")
    st.plotly_chart(fig11, width="stretch")

with col2:
    fig12 = px.histogram(df_city, x="order_value", nbins=30,
                         title="Order Value Distribution")
    st.plotly_chart(fig12, width="stretch")

# -------------------------------
# ROW 6
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    profit = df_city.groupby("cuisine_type")["profit_margin_percent"].mean().reset_index()
    fig13 = px.bar(profit, x="cuisine_type", y="profit_margin_percent",
                   title="Profit Margin by Cuisine")
    st.plotly_chart(fig13, width="stretch")

with col2:
    cancel_reason = df_city["cancellation_reason"].value_counts().reset_index()
    cancel_reason.columns = ["reason","count"]
    fig14 = px.pie(cancel_reason, names="reason", values="count",
                   title="Cancellation Reasons")
    st.plotly_chart(fig14, width="stretch")

# -------------------------------
# HEATMAP
# -------------------------------
st.subheader("📊 Correlation Heatmap")

corr = df[["order_value","delivery_time_min","distance_km","profit_margin_percent"]].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# -------------------------------
# INSIGHTS
# -------------------------------
st.markdown("## 📌 Key Insights")

st.write("""
- Evening hours show peak order demand  
- Higher distance leads to longer delivery time  
- Some cuisines generate higher profit margins  
- Discounts slightly reduce profit margins  
- Few restaurants dominate total revenue  
""")