from email_reader import extract_order_info
from inventory_updater import update_inventory
from stock_checker import check_and_generate_restock_messages
from email_sender import send_email

def run_warehouse_automation():
    # 1️⃣ Simulate email content (can also read from real mailbox)
    # Note: The Chinese test data below is kept for demonstration purposes
    # In production, this would be replaced with real English email content
    email_content = """
    订单编号：#20250412-001
    客户姓名：李四
    订购物品：
    - A4打印纸（型号：P500） 数量：40
    - 无线鼠标（型号：M102）数量：15
    预计发货日期：2025年4月13日
    客户邮箱：lisi@gmail.com
    """

    # 2️⃣ Extract order information
    print("📩 Extracting order information...")
    order_info = extract_order_info(email_content)
    print("✅ Extraction successful:", order_info)

    # 3️⃣ Update inventory
    print("📦 Updating inventory...")
    update_inventory(order_info, "inventory.xlsx")
    print("✅ Inventory updated")

    # 4️⃣ Check low inventory → Generate restocking reminders
    print("📉 Checking low inventory products...")
    restock_messages = check_and_generate_restock_messages("inventory.xlsx")

    # 5️⃣ Send reminder emails
    if not restock_messages:
        print("✅ All products have sufficient inventory, no restocking needed.")
    else:
        for recipient, messages in restock_messages.items():
            subject = "【AI Auto Alert】The following products have insufficient inventory, please restock promptly"
            content = "\n\n".join(messages)
            print(f"📬 Sending email to {recipient}...")
            send_email(recipient, subject, content)

    print("\n🎉 Automation workflow completed!")

if __name__ == "__main__":
    run_warehouse_automation()
