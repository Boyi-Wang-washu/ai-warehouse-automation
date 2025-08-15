import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np


def load_order_data(filepath="order_history.csv"):
    """
    Load order data from CSV file
    
    Note: The Chinese column names ('日期', '型号', '数量') are from the CSV file structure
    and are kept for data compatibility. These mean 'Date', 'Model', 'Quantity' respectively.
    """
    df = pd.read_csv(filepath)
    # Note: '日期' means 'Date' in Chinese
    df["日期"] = pd.to_datetime(df["日期"])
    return df


def forecast_product_demand(df, model_code, days=7):
    """
    Forecast product demand using linear regression
    
    Args:
        df: DataFrame with order data (Chinese column names: '型号'=Model, '数量'=Quantity)
        model_code: Product model code to forecast
        days: Number of days to forecast
    """
    # Note: '型号' means 'Model' in Chinese
    df_model = df[df["型号"] == model_code].copy()
    if df_model.empty:
        print(f"⚠️ No historical order data found for model {model_code}.")
        return 0

    # Aggregate order quantities by date
    # Note: '日期' means 'Date', '数量' means 'Quantity' in Chinese
    df_daily = df_model.groupby("日期")["数量"].sum().reset_index()

    # Build training data: map dates to numerical values (days)
    df_daily["days_since_start"] = (df_daily["日期"] - df_daily["日期"].min()).dt.days
    X = df_daily[["days_since_start"]]
    y = df_daily["数量"]

    # Fit linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future days order quantities
    future_days = np.array([[X["days_since_start"].max() + i] for i in range(1, days+1)])
    predictions = model.predict(future_days)
    predicted_demand = int(predictions.sum())

    print(f"🔮 Predicted demand for model {model_code} in next {days} days: approximately {predicted_demand}")
    return predicted_demand


# Example usage
df_orders = load_order_data("order_history.csv")
forecast_product_demand(df_orders, model_code="M102", days=7)  # Predict wireless mouse demand
