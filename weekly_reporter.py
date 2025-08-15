import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from predictor import load_order_data, forecast_product_demand
from email_sender import send_email
import os

def generate_weekly_report(order_file="order_history.csv", inventory_file="inventory.xlsx"):
    """
    Generate weekly inventory and order trend report
    
    Note: The Chinese column names are from the data file structure:
    '日期' = 'Date', '型号' = 'Model', '数量' = 'Quantity'
    '产品名称' = 'Product Name', '当前库存' = 'Current Inventory'
    """
    df_orders = load_order_data(order_file)
    df_inventory = pd.read_excel(inventory_file)
    # ========== NEW: If order file is empty, skip report generation ==========
    if df_orders.empty:
        print("⚠️ No order data this week, skipping report generation.")
        return
    # ===================================================
    today = datetime.today()
    last_week = today - timedelta(days=7)

    # Filter orders from last 7 days
    # Note: '日期' means 'Date' in Chinese
    df_week = df_orders[df_orders["日期"] >= last_week]

    # Calculate weekly sales by model
    # Note: '型号' means 'Model', '数量' means 'Quantity' in Chinese
    df_summary = df_week.groupby("型号")["数量"].sum().reset_index()
    
    # ========== NEW: If weekly summary is empty, skip report generation ==========
    if df_summary.empty:
        print("⚠️ Weekly order list is empty, skipping report generation.")
        return
    # ===================================================

    report_lines = ["📊 Weekly Inventory and Order Report\n"]
    for _, row in df_summary.iterrows():
        model = row["型号"]  # Model
        # Note: '产品名称' means 'Product Name' in Chinese
        name = df_inventory[df_inventory["型号"] == model]["产品名称"].values[0]
        weekly_sales = row["数量"]  # Quantity
        forecast = forecast_product_demand(df_orders, model, days=7)
        # Note: '当前库存' means 'Current Inventory' in Chinese
        current_stock = df_inventory[df_inventory["型号"] == model]["当前库存"].values[0]

        report_lines.append(
            f"Product: {name} (Model: {model})\n - Weekly sales: {weekly_sales}\n - 7-day forecast: {forecast}\n - Current inventory: {current_stock}\n"
        )

    # Generate report content
    report_content = "\n".join(report_lines)

    # Optional: Generate chart and save
    fig, ax = plt.subplots()
    # Note: '型号' means 'Model', '数量' means 'Quantity' in Chinese
    df_summary.plot(kind='bar', x='型号', y='数量', ax=ax, legend=False)
    ax.set_title("📦 Weekly Product Sales")
    ax.set_ylabel("Sales")
    chart_path = "weekly_chart.png"
    plt.tight_layout()
    plt.savefig(chart_path)

    # Send email
    subject = "【Weekly Report】Inventory and Order Trend Analysis"
    to_email = "boyiwanglance@gmail.com"  # Can be set based on category
    send_email(to_email, subject, report_content)

    # Delete chart (if not needed to keep)
    if os.path.exists(chart_path):
        os.remove(chart_path)

    print("✅ Weekly report generated and sent.")

# Example call
if __name__ == "__main__":
    generate_weekly_report()
