import pandas as pd

def update_inventory(order_info, inventory_file="inventory.xlsx"):
    """
    根据订单信息更新库存 Excel 表格
    """
    # 读取库存 Excel 表格
    df = pd.read_excel(inventory_file)

    for item in order_info['products']:
        model = item['model']
        quantity = item['quantity']

        # 查找型号对应的库存记录
        match = df[df['型号'] == model]

        if not match.empty:
            current_index = match.index[0]
            current_stock = df.at[current_index, '当前库存']

            # 扣减库存数量
            new_stock = max(0, current_stock - quantity)
            df.at[current_index, '当前库存'] = new_stock

            print(f"已更新：{item['name']}（{model}） 库存从 {current_stock} → {new_stock}")
        else:
            print(f"⚠️ 找不到型号为 {model} 的产品，无法更新库存")

    # 保存更新后的库存表
    df.to_excel(inventory_file, index=False)
    print("✅ 库存已更新并保存。")


# 测试代码
if __name__ == "__main__":
    # 你可以把这里换成 email_reader.py 解析出的结果
    sample_order = {
        'order_number': '20250401-001',
        'products': [
            {'name': 'A4打印纸', 'model': 'P500', 'quantity': 20},
            {'name': '无线鼠标', 'model': 'M102', 'quantity': 5}
        ]
    }

    update_inventory(sample_order, "inventory.xlsx")
