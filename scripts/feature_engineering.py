import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# -------------------------------
# FEATURE ENGINEERING
# -------------------------------
def feature_engineering(df):

    # -------------------------------
    # AGE GROUP
    # -------------------------------
    def age_group(age):
        if pd.isnull(age):
            return "Unknown"
        elif age < 18:
            return "Teen"
        elif age < 30:
            return "Young Adult"
        elif age < 50:
            return "Adult"
        else:
            return "Senior"

    df["customer_age_group"] = df["customer_age"].apply(age_group)

    # -------------------------------
    # DELIVERY PERFORMANCE
    # -------------------------------
    def delivery_performance(time):
        if pd.isnull(time):
            return "Unknown"
        elif time <= 30:
            return "Fast"
        elif time <= 60:
            return "Moderate"
        else:
            return "Delayed"

    df["delivery_performance"] = df["delivery_time_min"].apply(delivery_performance)

    # -------------------------------
    # PROFIT MARGIN %
    # -------------------------------
    df["profit_margin_percent"] = np.where(
        df["final_amount"] > 0,
        (df["profit_margin"] / df["final_amount"]) * 100,
        0
    )

    df["profit_margin_percent"] = df["profit_margin_percent"].replace([np.inf, -np.inf], 0)
    df["profit_margin_percent"] = df["profit_margin_percent"].fillna(0)

    return df


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    # -------------------------------
    # LOAD FROM SQL (IMPORTANT 🔥)
    # -------------------------------
    engine = create_engine("mysql+mysqlconnector://root:Balaji%4012345@localhost/food_delivery_db")

    df = pd.read_sql("SELECT * FROM cleaned_data", engine)

    # -------------------------------
    # APPLY FEATURE ENGINEERING
    # -------------------------------
    df = feature_engineering(df)

    # -------------------------------
    # SAVE BACK TO SQL
    # -------------------------------
    df.to_sql("engineered_food_delivery", engine, if_exists="replace", index=False)

    print("✅ Feature Engineering Done & Saved to MySQL")
    print("\nMissing Values:\n", df.isnull().sum())