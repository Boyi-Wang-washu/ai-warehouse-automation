import pandas as pd

def update_inventory(order_info, inventory_file="inventory.xlsx"):
    """
    Update inventory Excel table based on order information
    
    Note: The Chinese column names ('型号', '当前库存') are from the Excel file structure
    and are kept for data compatibility. In a production environment, these could be
    standardized to English column names.
    """
    # Read inventory Excel table
    df = pd.read_excel(inventory_file)

    for item in order_info['products']:
        model = item['model']
        quantity = item['quantity']

        # Find inventory record matching the model
        # Note: '型号' means 'Model' in Chinese, kept for Excel compatibility
        match = df[df['型号'] == model]

        if not match.empty:
            current_index = match.index[0]
            # Note: '当前库存' means 'Current Inventory' in Chinese
            current_stock = df.at[current_index, '当前库存']

            # Deduct inventory quantity
            new_stock = max(0, current_stock - quantity)
            df.at[current_index, '当前库存'] = new_stock

            print(f"Updated: {item['name']} ({model}) inventory from {current_stock} → {new_stock}")
        else:
            print(f"⚠️ Product with model {model} not found, cannot update inventory")

    # Save updated inventory table
    df.to_excel(inventory_file, index=False)
    print("✅ Inventory updated and saved.")


# Test code
if __name__ == "__main__":
    # You can replace this with the result parsed from email_reader.py
    sample_order = {
        'order_number': '20250401-001',
        'products': [
            {'name': 'A4 Paper', 'model': 'P500', 'quantity': 20},
            {'name': 'Wireless Mouse', 'model': 'M102', 'quantity': 5}
        ]
    }

    update_inventory(sample_order, "inventory.xlsx")
