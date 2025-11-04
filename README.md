# Codechino ☕💻
_Code at your favourite coffee place._

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30-orange.svg)](https://streamlit.io/)
[![GitHub release](https://img.shields.io/github/v/release/ViragSzabo/codechino?include_prereleases&label=release)](https://github.com/ViragSzabo/codechino/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/ViragSzabo/codechino)](https://github.com/ViragSzabo/codechino/issues)

A Python project to track coffee shop orders, spending,
and favourite tables, with interactive analytics.

---

## Features
- Track and analyze orders over time
- Calculate total spending per year, month, and category
- Identify most popular items and tables
- Export data to CSV and JSON
- Interactive dashboard with charts and filters (Streamlit)

---

## Installation
1. Clone the repository:

```bash
git clone https://github.com/yourusername/codechino.git
cd codechino
````

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
````

3. Install dependencies:
```bash
git clone https://github.com/yourusername/codechino.git
cd codechino
````

---

## Running the dashboard
Streamlit is used for the web-based dashboard. Run it using:
```bash
streamlit run dashboard.py
````
This will start a local server (usually at http://localhost:8501) where you can:
* Filter orders by date, table, or category
* View interactive charts
* Export filtered data to CSV or JSON

---

## File Structure
* sam_orders.json – JSON export of all orders
* sam_summary.csv – CSV summary of spending by category
* dashboard.py – Streamlit dashboard
* requirements.txt – Python dependencies
* README.md – Project description