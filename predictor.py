import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np


def load_order_data(filepath="order_history.csv"):
    df = pd.read_csv(filepath)
    df["日期"] = pd.to_datetime(df["日期"])
    return df


def forecast_product_demand(df, model_code, days=7):
    df_model = df[df["型号"] == model_code].copy()
    if df_model.empty:
        print(f"⚠️ 没有找到型号为 {model_code} 的历史订单数据。")
        return 0

    # 按日期汇总订单数量
    df_daily = df_model.groupby("日期")["数量"].sum().reset_index()

    # 构建训练数据：将日期映射为数值（天数）
    df_daily["days_since_start"] = (df_daily["日期"] - df_daily["日期"].min()).dt.days
    X = df_daily[["days_since_start"]]
    y = df_daily["数量"]

    # 拟合线性回归模型
    model = LinearRegression()
    model.fit(X, y)

    # 预测未来几天的订单量
    future_days = np.array([[X["days_since_start"].max() + i] for i in range(1, days+1)])
    predictions = model.predict(future_days)
    predicted_demand = int(predictions.sum())

    print(f"🔮 预测型号 {model_code} 未来 {days} 天订单量约为：{predicted_demand}")
    return predicted_demand


# 示例用法
df_orders = load_order_data("order_history.csv")
forecast_product_demand(df_orders, model_code="M102", days=7)  # 预测无线鼠标
