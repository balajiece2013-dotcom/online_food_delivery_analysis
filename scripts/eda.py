import pandas as pd  # data handling
from sqlalchemy import create_engine  # MySQL connection

# -------------------------------
# CREATE MYSQL CONNECTION
# -------------------------------
# Best practice: using SQLAlchemy engine for safe DB connection
engine = create_engine(
    "mysql+mysqlconnector://root:Balaji%4012345@localhost/food_delivery_db"
)

# confirmation message
print("✅ Connected to MySQL successfully!")

# -------------------------------
# TEST QUERY (SAMPLE DATA CHECK)
# -------------------------------
# fetching first 5 rows from engineered dataset
query = "SELECT * FROM engineered_food_delivery LIMIT 5"

df = pd.read_sql(query, engine)

# display sample data
print("\n📊 Sample Data:")
print(df.head())

# -------------------------------
# CHECK ALL TABLES IN DATABASE
# -------------------------------
# useful for verifying database structure
tables = pd.read_sql("SHOW TABLES", engine)

print("\n📂 Tables in Database:")
print(tables)