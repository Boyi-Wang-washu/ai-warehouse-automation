import pandas as pd

# Custom procurement staff email addresses
# Note: Category names are in Chinese from the Excel file structure
# '日常消耗品' = 'Daily Consumables', '大件设备' = 'Large Equipment'
PROCUREMENT_EMAILS = {
    "日常消耗品": "wang_procure@example.com",  # Daily Consumables
    "大件设备": "li_procure@example.com"      # Large Equipment
}

def check_and_generate_restock_messages(inventory_file="inventory.xlsx"):
    """
    Check inventory levels and generate restocking messages
    
    Note: The Chinese column names are from the Excel file structure:
    '当前库存' = 'Current Inventory', '安全库存' = 'Safety Stock'
    '分类' = 'Category', '型号' = 'Model', '产品名称' = 'Product Name'
    """
    df = pd.read_excel(inventory_file)
    messages = {}

    for idx, row in df.iterrows():
        # Note: Chinese column names for Excel compatibility
        current_stock = row['当前库存']      # Current Inventory
        safe_stock = row['安全库存']        # Safety Stock
        category = row['分类']             # Category
        model = row['型号']               # Model
        name = row['产品名称']            # Product Name

        if current_stock < safe_stock:
            recipient = PROCUREMENT_EMAILS.get(category, "unknown@example.com")
            message = (
                f"Product: {name} (Model: {model})\n"
                f"Current inventory: {current_stock}, Safety stock: {safe_stock}\n"
                f"Please restock promptly to avoid shipping delays."
            )

            if recipient not in messages:
                messages[recipient] = []

            messages[recipient].append(message)

    return messages


# Test run
if __name__ == "__main__":
    messages = check_and_generate_restock_messages("inventory.xlsx")

    for email, msgs in messages.items():
        print(f"\n📩 To: {email}")
        print("Content:")
        for m in msgs:
            print("-" * 40)
            print(m)

