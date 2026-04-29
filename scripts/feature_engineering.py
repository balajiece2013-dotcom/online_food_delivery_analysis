import pandas as pd  # data handling
import numpy as np   # numerical operations
from sqlalchemy import create_engine  # MySQL connection

# -------------------------------
# FEATURE ENGINEERING FUNCTION
# -------------------------------
def feature_engineering(df):

    # -------------------------------
    # CUSTOMER AGE GROUP FEATURE
    # -------------------------------
    # This function categorizes customers based on age
    def age_group(age):
        if pd.isnull(age):  # handle missing age
            return "Unknown"
        elif age < 18:
            return "Teen"
        elif age < 30:
            return "Young Adult"
        elif age < 50:
            return "Adult"
        else:
            return "Senior"

    # apply age grouping to create new column
    df["customer_age_group"] = df["customer_age"].apply(age_group)

    # -------------------------------
    # DELIVERY PERFORMANCE FEATURE
    # -------------------------------
    # classify delivery based on time taken
    def delivery_performance(time):
        if pd.isnull(time):  # missing delivery time
            return "Unknown"
        elif time <= 30:
            return "Fast"
        elif time <= 60:
            return "Moderate"
        else:
            return "Delayed"

    # create delivery performance column
    df["delivery_performance"] = df["delivery_time_min"].apply(delivery_performance)

    # -------------------------------
    # PROFIT MARGIN PERCENTAGE
    # -------------------------------
    # calculate profit percentage based on final amount
    df["profit_margin_percent"] = np.where(
        df["final_amount"] > 0,
        (df["profit_margin"] / df["final_amount"]) * 100,
        0
    )

    # handle infinite values if any division error occurs
    df["profit_margin_percent"] = df["profit_margin_percent"].replace([np.inf, -np.inf], 0)

    # replace missing values with 0
    df["profit_margin_percent"] = df["profit_margin_percent"].fillna(0)

    return df  # return updated dataset


# -------------------------------
# MAIN EXECUTION BLOCK
# -------------------------------
if __name__ == "__main__":

    # -------------------------------
    # CONNECT TO MYSQL DATABASE
    # -------------------------------
    engine = create_engine(
        "mysql+mysqlconnector://root:Balaji%4012345@localhost/food_delivery_db"
    )

    # -------------------------------
    # LOAD CLEANED DATA FROM SQL
    # -------------------------------
    df = pd.read_sql("SELECT * FROM cleaned_data", engine)

    # -------------------------------
    # APPLY FEATURE ENGINEERING
    # -------------------------------
    df = feature_engineering(df)

    # -------------------------------
    # SAVE FINAL DATA BACK TO SQL
    # -------------------------------
    df.to_sql(
        "engineered_food_delivery",  # new table name
        engine,
        if_exists="replace",
        index=False
    )

    # -------------------------------
    # SUCCESS MESSAGE
    # -------------------------------
    print("✅ Feature Engineering Done & Saved to MySQL")

    # optional: check missing values
    print("\nMissing Values:\n", df.isnull().sum())