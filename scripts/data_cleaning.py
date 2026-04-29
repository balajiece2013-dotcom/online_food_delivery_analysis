import pandas as pd  # data handling
import numpy as np    # numerical operations
from sqlalchemy import create_engine  # MySQL connection

# -------------------------------
# LOAD DATA FROM CSV
# -------------------------------
def load_data(path):
    df = pd.read_csv(path)  # read csv file

    # standardize column names (remove spaces + lowercase)
    df.columns = df.columns.str.strip().str.lower()

    return df


# -------------------------------
# CLEAN DATA FUNCTION
# -------------------------------
def clean_data(df):

    # ---------------------------
    # HANDLE NUMERIC MISSING VALUES
    # ---------------------------
    num_cols = ["customer_age", "delivery_time_min", "distance_km", "order_value"]

    for col in num_cols:
        if col in df.columns:
            # fill missing values with median (safe for outliers)
            df[col] = df[col].fillna(df[col].median())

    # ---------------------------
    # HANDLE CATEGORICAL MISSING VALUES
    # ---------------------------
    if "customer_gender" in df.columns:
        # fill with most frequent value
        df["customer_gender"] = df["customer_gender"].fillna(df["customer_gender"].mode()[0])

    # default category for missing values
    df["cuisine_type"] = df["cuisine_type"].fillna("Others")
    df["payment_mode"] = df["payment_mode"].fillna("Others")

    # ---------------------------
    # STANDARDIZE CITY & AREA
    # ---------------------------
    df["city"] = df["city"].fillna("Others").replace("unknown", "Others").str.strip().str.title()
    df["area"] = df["area"].fillna("Others").replace("unknown", "Others").str.strip().str.title()

    # ---------------------------
    # BUSINESS RULE FIXES
    # ---------------------------
    df["discount_applied"] = df["discount_applied"].fillna(0)
    df["cancellation_reason"] = df["cancellation_reason"].fillna("Not Cancelled")

    # ---------------------------
    # DELIVERY RATING CLEANING
    # ---------------------------
    df["delivery_rating"] = pd.to_numeric(df["delivery_rating"], errors="coerce")
    df["delivery_rating"] = df["delivery_rating"].fillna(df["delivery_rating"].median())

    # ---------------------------
    # OUTLIER HANDLING (IQR METHOD)
    # ---------------------------
    if "order_value" in df.columns:
        Q1 = df["order_value"].quantile(0.25)
        Q3 = df["order_value"].quantile(0.75)
        IQR = Q3 - Q1

        # clip extreme values
        df["order_value"] = np.clip(df["order_value"], Q1 - 1.5*IQR, Q3 + 1.5*IQR)

    if "delivery_time_min" in df.columns:
        Q1 = df["delivery_time_min"].quantile(0.25)
        Q3 = df["delivery_time_min"].quantile(0.75)
        IQR = Q3 - Q1

        df["delivery_time_min"] = np.clip(df["delivery_time_min"], Q1 - 1.5*IQR, Q3 + 1.5*IQR)

    # ---------------------------
    # INVALID VALUE CORRECTION
    # ---------------------------
    # rating should be max 5
    df.loc[df["restaurant_rating"] > 5, "restaurant_rating"] = df["restaurant_rating"].median()

    # profit cannot be negative
    df.loc[df["profit_margin"] < 0, "profit_margin"] = 0

    # ---------------------------
    # FINAL AMOUNT CALCULATION
    # ---------------------------
    df["final_amount"] = df["final_amount"].fillna(
        df["order_value"].fillna(0) - df["discount_applied"].fillna(0)
    )

    # ---------------------------
    # DATE & TIME PROCESSING
    # ---------------------------
    df = df.dropna(subset=["order_date"]).copy()

    # fill missing time
    df.loc[:, "order_time"] = df["order_time"].fillna(df["order_time"].mode()[0])

    # combine date + time into datetime
    df.loc[:, "order_datetime"] = pd.to_datetime(
        df["order_date"].astype(str) + " " + df["order_time"].astype(str),
        errors="coerce"
    )

    # drop invalid datetime rows
    df = df.dropna(subset=["order_datetime"])

    # extract useful time features
    df["order_hour"] = df["order_datetime"].dt.hour
    df["order_month"] = df["order_datetime"].dt.month
    df["order_weekday"] = df["order_datetime"].dt.day_name()

    # ---------------------------
    # PEAK HOUR FEATURE
    # ---------------------------
    df["peak_hour"] = df["order_hour"].apply(lambda x: 18 <= x <= 21)

    return df


# -------------------------------
# MAIN EXECUTION
# -------------------------------
if __name__ == "__main__":

    # load dataset
    df = load_data("../data/online_food_delivery_analysis.csv")

    # clean dataset
    df = clean_data(df)

    # ---------------------------
    # CONNECT TO MYSQL DATABASE
    # ---------------------------
    engine = create_engine(
        "mysql+mysqlconnector://root:Balaji%4012345@localhost/food_delivery_db"
    )

    # save cleaned data into MySQL table
    df.to_sql("cleaned_data", engine, if_exists="replace", index=False)

    print("✅ Data Cleaning Done & Saved to MySQL")

    # check missing values summary
    print("\nMissing Values:\n", df.isnull().sum())