import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from predictor import load_order_data, forecast_product_demand
from email_sender import send_email
import os

def generate_weekly_report(order_file="order_history.csv", inventory_file="inventory.xlsx"):
    df_orders = load_order_data(order_file)
    df_inventory = pd.read_excel(inventory_file)
    # ========== 新增：若订单文件为空，直接结束 ==========
    if df_orders.empty:
        print("⚠️ 本周没有任何订单数据，已跳过报告生成。")
        return
    # ===================================================
    today = datetime.today()
    last_week = today - timedelta(days=7)

    # 筛选最近7天的订单
    df_week = df_orders[df_orders["日期"] >= last_week]

    # 统计各型号本周销量
    df_summary = df_week.groupby("型号")["数量"].sum().reset_index()
    
    # ========== 新增：若本周汇总为空，直接结束 ==========
    if df_summary.empty:
        print("⚠️ 本周订单列表为空，已跳过报告生成。")
        return
    # ===================================================

    report_lines = ["📊 本周库存与订单报告\n"]
    for _, row in df_summary.iterrows():
        model = row["型号"]
        name = df_inventory[df_inventory["型号"] == model]["产品名称"].values[0]
        weekly_sales = row["数量"]
        forecast = forecast_product_demand(df_orders, model, days=7)
        current_stock = df_inventory[df_inventory["型号"] == model]["当前库存"].values[0]

        report_lines.append(
            f"产品：{name}（型号：{model}）\n - 本周销量：{weekly_sales}\n - 未来7天预测：{forecast}\n - 当前库存：{current_stock}\n"
        )

    # 生成报告内容
    report_content = "\n".join(report_lines)

    # 可选：生成图表并保存
    fig, ax = plt.subplots()
    df_summary.plot(kind='bar', x='型号', y='数量', ax=ax, legend=False)
    ax.set_title("📦 本周各产品销量")
    ax.set_ylabel("销量")
    chart_path = "weekly_chart.png"
    plt.tight_layout()
    plt.savefig(chart_path)

    # 发送邮件
    subject = "【每周报告】库存与订单趋势分析"
    to_email = "boyiwanglance@gmail.com"  # 可根据分类设置
    send_email(to_email, subject, report_content)

    # 删除图表（如不需要保留）
    if os.path.exists(chart_path):
        os.remove(chart_path)

    print("✅ 每周报告已生成并发送。")

# 示例调用
if __name__ == "__main__":
    generate_weekly_report()
