# SpendWise — Personal Expense Tracker

A local-first personal income and expense tracker built with Python, Streamlit, Pandas, Plotly, and SQLite.

## Features

- Record income and expenses
- Categorize transactions
- Dashboard with monthly totals
- Expense breakdown chart and daily spending chart
- Search and filter transactions
- Edit and delete transactions
- Local SQLite database (no external database account required)

## Requirements

- Python 3.10 or newer
- VS Code
- Internet connection for installing Python packages

## Run on Windows

Open this folder in VS Code, then run these commands in the integrated terminal:

```powershell
py -3 --version
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks virtual-environment activation, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

If the `py` launcher is unavailable, use `python` instead of `py -3` in the commands.

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.

## Database

The app automatically creates `expenses.db` in the project folder the first time it runs. The database is excluded from Git by `.gitignore`.

## Notes

- Amounts are displayed in PKR. Change `CURRENCY` in `app.py` if you want another currency label.
- The app uses a dark appearance configured in `.streamlit/config.toml`.
- Data is stored locally on the computer running the app.
- This is a learning project, not a banking or accounting system.
