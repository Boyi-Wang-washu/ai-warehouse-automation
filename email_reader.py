import re

def extract_order_info(email_content):
    """
    从邮件内容中提取订单信息，包括订单号、客户姓名、产品详情、发货日期和客户邮箱
    """
    order_info = {}

    # 订单编号
    match = re.search(r"订单编号[:：]?\s*#?([\d\-]+)", email_content)
    if match:
        order_info["order_number"] = match.group(1)

    # 客户姓名
    match = re.search(r"客户姓名[:：]?\s*(\S+)", email_content)
    if match:
        order_info["customer_name"] = match.group(1)

    # 客户邮箱
    match = re.search(r"客户邮箱[:：]?\s*(\S+@\S+)", email_content)
    if match:
        order_info["customer_email"] = match.group(1)

    # 发货日期
    match = re.search(r"预计发货日期[:：]?\s*([\d\-年月日\s]+)", email_content)
    if match:
        order_info["delivery_date"] = match.group(1).strip()

    # 提取所有产品信息
    product_lines = re.findall(r"-\s*(.*?)（型号[:：]?\s*(.*?)）数量[:：]?\s*(\d+)", email_content)
    products = []
    for name, model, quantity in product_lines:
        products.append({
            "name": name.strip(),
            "model": model.strip(),
            "quantity": int(quantity)
        })
    order_info["products"] = products

    return order_info


# 测试用例
if __name__ == "__main__":
    email_sample = """
    订单编号：#20250401-001
    客户姓名：李四
    订购物品：
    - A4打印纸（型号：P500） 数量：20
    - 无线鼠标（型号：M102）数量：5
    预计发货日期：2025年4月3日
    客户邮箱：lisi@gmail.com
    """

    info = extract_order_info(email_sample)
    print(info)
