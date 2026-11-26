import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from db import init_db, add_transaction, get_transactions, delete_transaction, update_transaction, get_categories

st.set_page_config(
    page_title="SpendWise | Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

CURRENCY = "PKR"

init_db()

st.title("💸 SpendWise")
st.caption("A simple, private space to understand where your money goes.")

with st.sidebar:
    st.title("SpendWise")
    page = st.radio("Navigation", ["Dashboard", "Add transaction", "Manage transactions"], label_visibility="collapsed")
    st.divider()
    st.caption("Your records are stored locally in an SQLite database on this computer.")
    st.caption("Currency: PKR")

df = get_transactions()

def money(value):
    return f"{CURRENCY} {value:,.2f}"

if page == "Dashboard":
    st.subheader("Your overview")
    if df.empty:
        st.info("No transactions yet. Add your first income or expense to see your dashboard.")
        st.page_link if False else None
    else:
        today = date.today()
        month_df = df[(pd.to_datetime(df["transaction_date"]).dt.year == today.year) &
                      (pd.to_datetime(df["transaction_date"]).dt.month == today.month)]
        income = float(month_df.loc[month_df["kind"] == "Income", "amount"].sum())
        expenses = float(month_df.loc[month_df["kind"] == "Expense", "amount"].sum())
        balance = income - expenses

        c1, c2, c3 = st.columns(3)
        c1.metric("Income this month", money(income))
        c2.metric("Expenses this month", money(expenses))
        c3.metric("Net this month", money(balance), delta=money(balance))

        st.markdown("### Spending breakdown")
        expense_df = df[df["kind"] == "Expense"].copy()
        left, right = st.columns([1.1, 1])
        with left:
            if expense_df.empty:
                st.info("Add an expense to see category breakdown.")
            else:
                by_category = expense_df.groupby("category", as_index=False)["amount"].sum()
                fig = px.pie(by_category, names="category", values="amount", hole=0.62,
                             title="Expenses by category")
                fig.update_layout(margin=dict(t=55, b=10, l=10, r=10), legend_title_text="")
                st.plotly_chart(fig, width="stretch")
        with right:
            if expense_df.empty:
                st.info("Your expense trend will appear here.")
            else:
                trend = expense_df.copy()
                trend["transaction_date"] = pd.to_datetime(trend["transaction_date"])
                trend = trend.groupby("transaction_date", as_index=False)["amount"].sum()
                fig = px.bar(trend, x="transaction_date", y="amount", title="Daily expenses",
                             labels={"transaction_date": "Date", "amount": f"Amount ({CURRENCY})"})
                fig.update_layout(margin=dict(t=55, b=10, l=10, r=10))
                st.plotly_chart(fig, width="stretch")

        st.markdown("### Recent transactions")
        recent = df.sort_values(["transaction_date", "id"], ascending=False).head(8)
        st.dataframe(recent[["transaction_date", "kind", "category", "description", "amount"]],
                     width="stretch", hide_index=True)

elif page == "Add transaction":
    st.subheader("Add a transaction")
    st.write("Record money received or spent.")
    with st.form("add_transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        kind = col1.selectbox("Transaction type", ["Expense", "Income"])
        category_options = get_categories(kind)
        category = col2.selectbox("Category", category_options)
        description = st.text_input("Description", placeholder="e.g. Grocery shopping")
        amount = st.number_input("Amount (PKR)", min_value=0.01, step=100.0, format="%.2f")
        transaction_date = st.date_input("Date", value=date.today())
        submitted = st.form_submit_button("Save transaction", type="primary", width="stretch")
        if submitted:
            if not description.strip():
                st.error("Please enter a short description.")
            else:
                add_transaction(kind, category, description.strip(), float(amount), transaction_date.isoformat())
                st.success("Transaction saved successfully.")
                st.rerun()

elif page == "Manage transactions":
    st.subheader("Manage transactions")
    if df.empty:
        st.info("There are no transactions to manage yet.")
    else:
        filter_col1, filter_col2 = st.columns(2)
        kinds = ["All"] + sorted(df["kind"].unique().tolist())
        chosen_kind = filter_col1.selectbox("Filter by type", kinds)
        search = filter_col2.text_input("Search description or category")
        view = df.copy()
        if chosen_kind != "All":
            view = view[view["kind"] == chosen_kind]
        if search.strip():
            mask = (view["description"].str.contains(search, case=False, na=False) |
                    view["category"].str.contains(search, case=False, na=False))
            view = view[mask]

        st.dataframe(view[["id", "transaction_date", "kind", "category", "description", "amount"]],
                     width="stretch", hide_index=True)

        st.markdown("#### Edit or delete a transaction")
        ids = view["id"].astype(int).tolist()
        if ids:
            selected_id = st.selectbox("Select transaction ID", ids)
            selected = view[view["id"] == selected_id].iloc[0]
            with st.expander("Edit selected transaction"):
                with st.form("edit_transaction_form"):
                    e1, e2 = st.columns(2)
                    edit_kind = e1.selectbox("Type", ["Expense", "Income"],
                                             index=0 if selected["kind"] == "Expense" else 1)
                    edit_categories = get_categories(edit_kind)
                    current_cat = selected["category"] if selected["category"] in edit_categories else edit_categories[0]
                    edit_category = e2.selectbox("Category", edit_categories,
                                                 index=edit_categories.index(current_cat))
                    edit_description = st.text_input("Description", value=str(selected["description"]))
                    edit_amount = st.number_input("Amount (PKR)", min_value=0.01,
                                                  value=float(selected["amount"]), step=100.0)
                    edit_date = st.date_input("Date", value=pd.to_datetime(selected["transaction_date"]).date())
                    save_edit = st.form_submit_button("Save changes", type="primary")
                    if save_edit:
                        if not edit_description.strip():
                            st.error("Description cannot be empty.")
                        else:
                            update_transaction(int(selected_id), edit_kind, edit_category,
                                               edit_description.strip(), float(edit_amount), edit_date.isoformat())
                            st.success("Transaction updated.")
                            st.rerun()

            confirm = st.checkbox("I understand this permanently deletes the selected transaction.")
            if st.button("Delete selected transaction", type="secondary", disabled=not confirm):
                delete_transaction(int(selected_id))
                st.success("Transaction deleted.")
                st.rerun()

st.divider()
st.caption("SpendWise • Local-first expense tracking • Your data stays in the project database.")
