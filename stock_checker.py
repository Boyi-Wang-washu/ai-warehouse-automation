import pandas as pd

# 自定义采购员邮箱地址
PROCUREMENT_EMAILS = {
    "日常消耗品": "wang_procure@example.com",
    "大件设备": "li_procure@example.com"
}

def check_and_generate_restock_messages(inventory_file="inventory.xlsx"):
    df = pd.read_excel(inventory_file)
    messages = {}

    for idx, row in df.iterrows():
        current_stock = row['当前库存']
        safe_stock = row['安全库存']
        category = row['分类']
        model = row['型号']
        name = row['产品名称']

        if current_stock < safe_stock:
            recipient = PROCUREMENT_EMAILS.get(category, "unknown@example.com")
            message = (
                f"产品：{name}（型号：{model}）\n"
                f"当前库存：{current_stock}，安全库存：{safe_stock}\n"
                f"请及时补货，以避免影响发货。"
            )

            if recipient not in messages:
                messages[recipient] = []

            messages[recipient].append(message)

    return messages


# 测试运行
if __name__ == "__main__":
    messages = check_and_generate_restock_messages("inventory.xlsx")

    for email, msgs in messages.items():
        print(f"\n📩 发往：{email}")
        print("内容：")
        for m in msgs:
            print("-" * 40)
            print(m)

