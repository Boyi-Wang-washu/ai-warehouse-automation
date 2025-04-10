from email_reader import extract_order_info
from inventory_updater import update_inventory
from stock_checker import check_and_generate_restock_messages
from gmail_api_sender import send_email

def run_warehouse_automation():
    # 1️⃣ 模拟邮件内容（也可以从真实邮箱读取）
    email_content = """
    订单编号：#20250412-001
    客户姓名：李四
    订购物品：
    - A4打印纸（型号：P500） 数量：40
    - 无线鼠标（型号：M102）数量：15
    预计发货日期：2025年4月13日
    客户邮箱：lisi@gmail.com
    """

    # 2️⃣ 提取订单信息
    print("📩 正在提取订单信息...")
    order_info = extract_order_info(email_content)
    print("✅ 提取成功：", order_info)

    # 3️⃣ 更新库存
    print("📦 正在更新库存...")
    update_inventory(order_info, "inventory.xlsx")
    print("✅ 库存已更新")

    # 4️⃣ 检查低库存 → 生成补货提醒
    print("📉 正在检查低库存产品...")
    restock_messages = check_and_generate_restock_messages("inventory.xlsx")

    # 5️⃣ 发送提醒邮件
    if not restock_messages:
        print("✅ 所有产品库存充足，无需补货。")
    else:
        for recipient, messages in restock_messages.items():
            subject = "【AI自动提醒】以下产品库存不足，请及时补货"
            content = "\n\n".join(messages)
            print(f"📬 向 {recipient} 发送邮件...")
            send_email(recipient, subject, content)

    print("\n🎉 自动化流程已全部完成！")

if __name__ == "__main__":
    run_warehouse_automation()
