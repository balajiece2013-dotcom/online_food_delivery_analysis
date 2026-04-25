import pandas as pd
from sqlalchemy import create_engine

# -------------------------------
# CREATE CONNECTION (BEST PRACTICE 🔥)
# -------------------------------
engine = create_engine("mysql+mysqlconnector://root:Balaji%4012345@localhost/food_delivery_db")

print("✅ Connected to MySQL successfully!")

# -------------------------------
# TEST QUERY
# -------------------------------
query = "SELECT * FROM engineered_food_delivery LIMIT 5"

df = pd.read_sql(query, engine)

print("\n📊 Sample Data:")
print(df.head())

# -------------------------------
# CHECK TABLES (EXTRA 🔥)
# -------------------------------
tables = pd.read_sql("SHOW TABLES", engine)

print("\n📂 Tables in Database:")
print(tables)