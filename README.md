# 🧠 AI-Driven Warehouse Automation System

一个完整的仓库管理自动化系统，融合 AI 库存预测、邮件处理、自动报表生成与云端定时任务，适用于企业库存精细化管理场景。

## 📦 功能模块

- 📩 **订单解析**：从邮件中提取订单信息（产品名、型号、数量、客户等）
- 📊 **库存更新**：自动更新 Excel 库，实时记录库存变动
- 🔮 **库存预测**：基于历史订单，预测未来 7 天需求
- ⚠️ **缺货提醒**：判断库存与预测值，自动发出邮件警告
- 📈 **每周报告**：自动生成库存变化趋势报告，邮件发送采购员
- 📉 **每月分析**：自动生成市场趋势 + 补货建议报告，发送至 CEO
- ☁️ **GitHub Actions 定时运行**：支持每周五 / 每月30日自动执行

## 🗂️ 项目结构

ai-warehouse-automation/ ├── inventory.xlsx ├── order_history_updated.csv ├── predictor.py ├── gmail_api_sender.py ├── weekly_reporter.py ├── monthly_analyzer.py ├── scheduler.py ├── requirements.txt └── .github/ └── workflows/ ├── weekly.yml └── monthly.yml

## 🚀 技术栈

- Python + Pandas + Scikit-learn + Matplotlib
- Gmail API (OAuth2)
- GitHub Actions（自动定时任务）
- Excel + 可视化报表

## 🎯 展示方式建议

- 可本地运行演示 `scheduler.py`
- 或打开 GitHub → Actions → 查看周报/月报是否自动运行成功
