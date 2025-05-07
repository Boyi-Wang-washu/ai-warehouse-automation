import pandas as pd
from datetime import datetime, timedelta
from predictor import load_order_data, forecast_product_demand
from email_sender import send_email

def generate_monthly_trend_report(order_file="order_history.csv", inventory_file="inventory.xlsx"):
    df_orders = load_order_data(order_file)
    df_inventory = pd.read_excel(inventory_file)

    today = datetime.today()
    last_3_months = today - timedelta(days=90)

    # 获取近90天数据
    df_recent = df_orders[df_orders["日期"] >= last_3_months].copy()
    report_lines = ["📈 市场趋势分析报告\n"]

    # 汇总产品销售情况
    product_trends = df_recent.groupby(["产品名称", "型号"])["数量"].agg(['count', 'sum']).reset_index()
    product_trends.columns = ["产品名称", "型号", "订单频率", "总销量"]

    for _, row in product_trends.iterrows():
        name = row["产品名称"]
        model = row["型号"]
        freq = row["订单频率"]
        total = row["总销量"]
        forecast = forecast_product_demand(df_orders, model, days=7)
        stock = df_inventory[df_inventory["型号"] == model]["当前库存"].values[0]

        recommendation = "✅ 库存充足"
        if forecast > stock:
            recommendation = f"⚠️ 预测需求高于库存，建议补货 {forecast - stock} 件"
        elif total < 20:
            recommendation = "📉 需求偏低，可考虑减少补货频率"

        report_lines.append(
            f"产品：{name}（型号：{model}）\n - 订单频率：{freq} 次\n - 总销量：{total} 件\n - 当前库存：{stock} 件\n - 未来7天预测：{forecast} 件\n - 建议：{recommendation}\n"
        )

    report_content = "\n".join(report_lines)
    subject = "【月度报告】市场趋势分析与采购建议"
    to_email = "boyiwanglance@gmail.com"
    send_email(to_email, subject, report_content)

    print("✅ 月度趋势分析报告已生成并发送给 CEO。")

# 示例执行
if __name__ == "__main__":
    generate_monthly_trend_report()
