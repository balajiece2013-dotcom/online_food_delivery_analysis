# ================================
# FINAL STREAMLIT DASHBOARD 
# ================================

import pandas as pd  # data handling
import streamlit as st  # dashboard framework
import plotly.express as px  # interactive visualizations
import seaborn as sns  # statistical plots
import matplotlib.pyplot as plt  # heatmap plotting
from sqlalchemy import create_engine  # MySQL connection

# -------------------------------
# LOAD DATA FROM MYSQL (CACHED FOR PERFORMANCE 🔥)
# -------------------------------
@st.cache_data
def load_data():
    # create connection to MySQL database
    engine = create_engine(
        "mysql+mysqlconnector://root:Balaji%4012345@localhost/food_delivery_db"
    )

    # fetch engineered dataset from SQL table
    query = "SELECT * FROM engineered_food_delivery"
    df = pd.read_sql(query, engine)

    # standardize column names
    df.columns = df.columns.str.strip().str.lower()

    return df


# load data into dataframe
df = load_data()

# -------------------------------
# DASHBOARD TITLE
# -------------------------------
st.markdown("""
<h1 style='text-align: center; color: #FF4B4B;'>🍔 Online Food Delivery Analysis</h1>
<h4 style='text-align: center; color: gray;'>Data-Driven Business Insights Dashboard</h4>
""", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# SIDEBAR FILTERS (USER INTERACTION 🔥)
# -------------------------------
st.sidebar.header("📊 Filters")

# select city filter
city = st.sidebar.selectbox(
    "Select City",
    sorted(df["city"].dropna().unique())
)

# select cuisine filter
cuisine = st.sidebar.selectbox(
    "Select Cuisine",
    ["All"] + sorted(df["cuisine_type"].dropna().unique())
)

# filter dataset based on selected city
df_city = df[df["city"] == city]

# apply cuisine filter if not "All"
if cuisine != "All":
    df_city = df_city[df_city["cuisine_type"] == cuisine]

# -------------------------------
# KPI SECTION (BUSINESS METRICS 🔥)
# -------------------------------
col1, col2, col3 = st.columns(3)
col4, col5, col6, col7 = st.columns(4)

# key business KPIs
col1.metric("Total Orders", f"{len(df_city):,}")
col2.metric("Total Revenue", f"{df_city['final_amount'].sum():,.0f}")
col3.metric("Avg Order Value", f"{df_city['final_amount'].mean():,.2f}")

col4.metric("Avg Delivery Time", f"{df_city['delivery_time_min'].mean():.1f} min")

col5.metric(
    "Cancellation Rate",
    f"{(df_city['order_status'].str.lower()=='cancelled').mean()*100:.2f}%"
)

col6.metric("Avg Delivery Rating", f"{df_city['delivery_rating'].mean():.2f}")
col7.metric("Profit Margin %", f"{df_city['profit_margin_percent'].mean():.2f}%")

st.markdown("---")

# -------------------------------
# ROW 1: REVENUE ANALYSIS
# -------------------------------
col1, col2 = st.columns(2)

# revenue by cuisine type
with col1:
    cuisine_data = df_city.groupby("cuisine_type")["final_amount"].sum().reset_index()
    fig1 = px.bar(cuisine_data, x="cuisine_type", y="final_amount",
                  title="Revenue by Cuisine", color="cuisine_type")
    st.plotly_chart(fig1, use_container_width=True)

# top cities by revenue
with col2:
    city_revenue = df.groupby("city")["final_amount"].sum().reset_index() \
                     .sort_values(by="final_amount", ascending=False).head(10)

    fig2 = px.bar(city_revenue, x="city", y="final_amount",
                  title="Top Cities by Revenue", color="city")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# ROW 2: CUSTOMER & ORDER BEHAVIOR
# -------------------------------
col1, col2 = st.columns(2)

# customer age group distribution
with col1:
    age_data = df_city["customer_age_group"].value_counts().reset_index()
    age_data.columns = ["age_group", "count"]

    fig3 = px.pie(age_data, names="age_group", values="count",
                  title="Customer Age Group")
    st.plotly_chart(fig3, use_container_width=True)

# order trend by hour
with col2:
    hour_data = df_city["order_hour"].value_counts().sort_index().reset_index()
    hour_data.columns = ["hour", "orders"]

    fig4 = px.line(hour_data, x="hour", y="orders", markers=True,
                   title="Order Trend by Hour")
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# ROW 3: RESTAURANT ANALYSIS
# -------------------------------
col1, col2 = st.columns(2)

# top restaurants by revenue
with col1:
    rest_data = df_city.groupby("restaurant_name")["final_amount"].sum() \
                       .reset_index().sort_values(by="final_amount", ascending=False).head(10)

    fig5 = px.bar(rest_data, x="restaurant_name", y="final_amount",
                  title="Top Restaurants by Revenue")
    st.plotly_chart(fig5, use_container_width=True)

# restaurants with highest cancellations
with col2:
    cancel_data = df_city[df_city["order_status"].str.lower()=="cancelled"] \
                  ["restaurant_name"].value_counts().head(10).reset_index()

    cancel_data.columns = ["restaurant", "cancellations"]

    fig6 = px.bar(cancel_data, x="restaurant", y="cancellations",
                  title="Top Restaurants by Cancellation",
                  color_discrete_sequence=["#FF4B4B"])
    st.plotly_chart(fig6, use_container_width=True)

# -------------------------------
# ROW 4: DELIVERY ANALYSIS
# -------------------------------
col1, col2 = st.columns(2)

# distance vs delivery time
with col1:
    fig7 = px.scatter(df_city, x="distance_km", y="delivery_time_min",
                      title="Distance vs Delivery Time", opacity=0.4)
    st.plotly_chart(fig7, use_container_width=True)

# monthly revenue trend
with col2:
    monthly = df_city.groupby("order_month")["final_amount"].sum().reset_index()

    fig8 = px.line(monthly, x="order_month", y="final_amount", markers=True,
                   title="Monthly Revenue Trend")
    st.plotly_chart(fig8, use_container_width=True)

# -------------------------------
# ROW 5: ADVANCED ANALYSIS
# -------------------------------
col1, col2 = st.columns(2)

# delivery rating vs time (boxplot)
with col1:
    fig9 = px.box(df_city, x="delivery_rating", y="delivery_time_min",
                  title="Delivery Time Distribution by Rating")
    st.plotly_chart(fig9, use_container_width=True)

# discount vs profit impact
with col2:
    fig10 = px.box(df_city, x="discount_applied", y="profit_margin_percent",
                   title="Profit Distribution by Discount")
    st.plotly_chart(fig10, use_container_width=True)

# -------------------------------
# ROW 6: WEEKDAY & DISTRIBUTION
# -------------------------------
col1, col2 = st.columns(2)

# orders by weekday
with col1:
    week_data = df_city["order_weekday"].value_counts().reset_index()
    week_data.columns = ["day", "orders"]

    fig11 = px.bar(week_data, x="day", y="orders",
                   title="Orders by Weekday")
    st.plotly_chart(fig11, use_container_width=True)

# order value distribution
with col2:
    fig12 = px.histogram(df_city, x="final_amount", nbins=30,
                         title="Order Value Distribution")
    st.plotly_chart(fig12, use_container_width=True)

# -------------------------------
# ROW 7: PROFIT & CANCEL REASON
# -------------------------------
col1, col2 = st.columns(2)

# profit margin by cuisine
with col1:
    profit = df_city.groupby("cuisine_type")["profit_margin_percent"].mean().reset_index()

    fig13 = px.bar(profit, x="cuisine_type", y="profit_margin_percent",
                   title="Profit Margin by Cuisine")
    st.plotly_chart(fig13, use_container_width=True)

# cancellation reasons
with col2:
    cancel_reason = df_city["cancellation_reason"].value_counts().reset_index()
    cancel_reason.columns = ["reason", "count"]

    fig14 = px.pie(cancel_reason, names="reason", values="count",
                   title="Cancellation Reasons")
    st.plotly_chart(fig14, use_container_width=True)

# -------------------------------
# CORRELATION HEATMAP 🔥
# -------------------------------
st.subheader("📊 Correlation Heatmap")

# correlation matrix of key numerical features
corr = df[["final_amount", "delivery_time_min", "distance_km", "profit_margin_percent"]].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig)

# -------------------------------
# FINAL INSIGHTS SECTION
# -------------------------------
st.markdown("## 📌 Key Insights")

st.write("""
- Evening hours show peak order demand  
- Higher distance increases delivery time  
- Some cuisines yield higher profit margins  
- Discounts slightly reduce profitability  
- Few cities dominate overall revenue  
""")