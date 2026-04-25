import pandas as pd
from sqlalchemy import create_engine

# -------------------------------
# CONNECT TO SQL
# -------------------------------
engine = create_engine("mysql+mysqlconnector://root:Balaji%4012345@localhost/food_delivery_db")

# -------------------------------
# LOAD DATA FROM SQL
# -------------------------------
df = pd.read_sql("SELECT * FROM engineered_food_delivery", engine)

# -------------------------------
# BASIC INFO
# -------------------------------
print("📊 BASIC INFO")
print("Shape:", df.shape)
print("\nColumns:\n", df.columns)

# -------------------------------
# TOP ANALYSIS
# -------------------------------
print("\n🏙 Top Cities")
print(df["city"].value_counts().head())

print("\n🍔 Top Cuisines")
print(df["cuisine_type"].value_counts().head())

# -------------------------------
# KPI ANALYSIS
# -------------------------------
print("\n💰 Avg Order Value:", round(df["order_value"].mean(), 2))

print("\n⏱ Avg Delivery Time:", round(df["delivery_time_min"].mean(), 2))

print("\n❌ Cancellation Rate:",
      round((df["order_status"] == "Cancelled").mean() * 100, 2), "%")

print("\n⭐ Avg Delivery Rating:",
      round(df["delivery_rating"].mean(), 2))

print("\n🔥 Peak Hour Orders:")
print(df["peak_hour"].value_counts())

# -------------------------------
# ADVANCED INSIGHTS (🔥 ADD THIS)
# -------------------------------
print("\n📈 Revenue by City:")
print(df.groupby("city")["order_value"].sum().sort_values(ascending=False).head())

print("\n📉 Profit Margin by Cuisine:")
print(df.groupby("cuisine_type")["profit_margin_percent"].mean().sort_values(ascending=False).head())

print("\n🚚 Delivery Time by City:")
print(df.groupby("city")["delivery_time_min"].mean().sort_values())

print("\n❌ Cancellation by Restaurant:")
print(df[df["order_status"] == "Cancelled"]["restaurant_name"].value_counts().head())