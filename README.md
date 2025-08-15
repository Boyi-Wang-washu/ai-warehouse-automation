# 🧠 AI-Driven Warehouse Automation System

A comprehensive warehouse management automation system that integrates AI inventory prediction, email processing, automatic report generation, and cloud-based scheduled tasks, suitable for enterprise inventory fine-grained management scenarios.

## 📦 Core Features

- 📩 **Order Parsing**: Extract order information from emails (product name, model, quantity, customer, etc.)
- 📊 **Inventory Updates**: Automatically update Excel inventory database with real-time inventory changes
- 🔮 **Inventory Prediction**: Predict future 7-day demand based on historical orders
- ⚠️ **Stock Alerts**: Automatically send email warnings when inventory falls below predicted demand
- 📈 **Weekly Reports**: Automatically generate inventory trend reports and email them to procurement staff
- 📉 **Monthly Analysis**: Automatically generate market trend + restocking recommendation reports for CEO
- ☁️ **GitHub Actions Scheduling**: Supports automatic execution every Friday / 30th of each month

## 🗂️ Project Structure

```
ai-warehouse-automation/
├── inventory.xlsx
├── order_history_updated.csv
├── predictor.py
├── gmail_api_sender.py
├── weekly_reporter.py
├── monthly_analyzer.py
├── scheduler.py
├── requirements.txt
└── .github/
    └── workflows/
        ├── weekly.yml
        └── monthly.yml
```

## 🚀 Tech Stack

- Python + Pandas + Scikit-learn + Matplotlib
- Gmail API (OAuth2)
- GitHub Actions (Automated scheduled tasks)
- Excel + Visual reporting

## 🎯 Demo Instructions

- Can run locally with `scheduler.py` for demonstration
- Or check GitHub → Actions → to see if weekly/monthly reports run automatically

## 🔧 Installation & Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Gmail API credentials (see `gmail_api_sender_backup.py`)
4. Configure environment variables for SMTP settings
5. Run `python scheduler.py` to test the complete workflow

## 📊 Key Components

- **Email Reader**: Parses order emails using regex patterns
- **Inventory Manager**: Updates Excel inventory based on orders
- **AI Predictor**: Uses machine learning to forecast demand
- **Stock Checker**: Monitors inventory levels and generates alerts
- **Report Generator**: Creates weekly/monthly analysis reports
- **Email Sender**: Automated email notifications using Gmail API/SMTP
- **Scheduler**: Orchestrates the entire automation workflow

## 🌟 Use Cases

- Small to medium enterprise warehouse management
- Automated inventory tracking and updates
- Demand forecasting and procurement planning
- Automated reporting and alerting systems
- Integration with existing email workflows
