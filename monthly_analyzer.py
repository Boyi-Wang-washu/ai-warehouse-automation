import pandas as pd
from datetime import datetime, timedelta
from predictor import load_order_data, forecast_product_demand
from email_sender import send_email

def generate_monthly_trend_report(order_file="order_history.csv", inventory_file="inventory.xlsx"):
    """
    Generate monthly market trend analysis report
    
    Note: The Chinese column names are from the data file structure:
    '日期' = 'Date', '产品名称' = 'Product Name', '型号' = 'Model', '数量' = 'Quantity'
    '当前库存' = 'Current Inventory'
    """
    df_orders = load_order_data(order_file)
    df_inventory = pd.read_excel(inventory_file)

    today = datetime.today()
    last_3_months = today - timedelta(days=90)

    # Get data from last 90 days
    # Note: '日期' means 'Date' in Chinese
    df_recent = df_orders[df_orders["日期"] >= last_3_months].copy()
    report_lines = ["📈 Market Trend Analysis Report\n"]

    # Summarize product sales performance
    # Note: Chinese column names for data compatibility
    product_trends = df_recent.groupby(["产品名称", "型号"])["数量"].agg(['count', 'sum']).reset_index()
    product_trends.columns = ["产品名称", "型号", "Order Frequency", "Total Sales"]

    for _, row in product_trends.iterrows():
        name = row["产品名称"]  # Product Name
        model = row["型号"]     # Model
        freq = row["Order Frequency"]
        total = row["Total Sales"]
        forecast = forecast_product_demand(df_orders, model, days=7)
        # Note: '当前库存' means 'Current Inventory' in Chinese
        stock = df_inventory[df_inventory["型号"] == model]["当前库存"].values[0]

        recommendation = "✅ Sufficient inventory"
        if forecast > stock:
            recommendation = f"⚠️ Predicted demand exceeds inventory, recommend restocking {forecast - stock} units"
        elif total < 20:
            recommendation = "📉 Low demand, consider reducing restocking frequency"

        report_lines.append(
            f"Product: {name} (Model: {model})\n - Order frequency: {freq} times\n - Total sales: {total} units\n - Current inventory: {stock} units\n - 7-day forecast: {forecast} units\n - Recommendation: {recommendation}\n"
        )

    report_content = "\n".join(report_lines)
    subject = "【Monthly Report】Market Trend Analysis and Procurement Recommendations"
    to_email = "boyiwanglance@gmail.com"
    send_email(to_email, subject, report_content)

    print("✅ Monthly trend analysis report generated and sent to CEO.")

# Example execution
if __name__ == "__main__":
    generate_monthly_trend_report()
