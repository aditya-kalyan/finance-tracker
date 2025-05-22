import streamlit as st
from datetime import datetime
import pandas as pd
from utils.session import init_session
from utils.api_calls import (
    get_monthly_summary,
    create_income,
    create_expense,
    get_all_expenses,
    get_all_income,
    update_expense,
    delete_expense,
)

init_session()

if not st.session_state.token:
    st.warning("Please login first!")
    st.stop()

st.title("📊 Dashboard")

year = st.number_input("Year", value=datetime.now().year)
month = st.number_input("Month", value=datetime.now().month, min_value=1, max_value=12)

# Monthly summary
if st.button("🔄 Load Monthly Summary"):
    summary = get_monthly_summary(st.session_state.token, year, month)
    income_total = summary.get("total_income", 0)
    expenses_total = summary.get("total_expenses", 0)
    balance = income_total - expenses_total

    st.metric("💰 Total Income", f"₹{income_total}")
    st.metric("💸 Total Expenses", f"₹{expenses_total}")
    st.metric("🧮 Balance", f"₹{balance}")

st.markdown("---")
st.subheader("➕ Add Income / Expense")

col1, col2 = st.columns(2)

# Add Income
with col1:
    income_amt = st.number_input("Income Amount", value=0)
    income_src = st.text_input("Income Source")
    if st.button("➕ Add Income"):
        create_income(st.session_state.token, {"amount": income_amt, "source": income_src})
        st.success("Income added!")

# Add Expense
with col2:
    exp_amt = st.number_input("Expense Amount", value=0, key="exp_amt")
    exp_cat = st.text_input("Expense Category")
    if st.button("➖ Add Expense"):
        create_expense(st.session_state.token, {"amount": exp_amt, "category": exp_cat})
        st.success("Expense added!")

st.markdown("---")
st.subheader("📂 Incomes & Expenses")

# Get data
expenses = get_all_expenses(st.session_state.token)
incomes = get_all_income(st.session_state.token)

# Filter by selected month/year
expenses_filtered = [
    exp for exp in expenses
    if exp.get("date") and pd.to_datetime(exp["date"]).year == year and pd.to_datetime(exp["date"]).month == month
]
incomes_filtered = [
    inc for inc in incomes
    if inc.get("date") and pd.to_datetime(inc["date"]).year == year and pd.to_datetime(inc["date"]).month == month
]

# Show Incomes
st.markdown("### 💰 Incomes")
if incomes_filtered:
    df_inc = pd.DataFrame(incomes_filtered)
    if "source" not in df_inc.columns:
        df_inc["source"] = ""
    st.dataframe(df_inc[["amount", "source", "date"]], use_container_width=True)
else:
    st.info("No incomes for this month.")

# Show Expenses
st.markdown("### 💸 Expenses")
if expenses_filtered:
    df_exp = pd.DataFrame(expenses_filtered)
    df_exp["id"] = df_exp["id"].astype(str)  # Ensure string for display
    if "category" not in df_exp.columns:
        df_exp["category"] = ""
    st.dataframe(df_exp[["id", "amount", "category", "date"]], use_container_width=True)
else:
    st.info("No expenses for this month.")

st.markdown("---")
st.subheader("✏️ Update / ❌ Delete an Expense")

if expenses_filtered:
    expense_ids = [exp["id"] for exp in expenses_filtered]
    selected_id = st.selectbox("Select Expense ID to Update/Delete", expense_ids)

    selected_exp = next((exp for exp in expenses_filtered if exp["id"] == selected_id), None)

    if selected_exp:
        upd_amt = st.number_input("Update Amount", value=float(selected_exp["amount"]), key="upd_amt")
        upd_cat = st.text_input("Update Category", value=selected_exp.get("category", ""), key="upd_cat")

        col_upd, col_del = st.columns(2)
        with col_upd:
            if st.button("✅ Update Expense"):
                update_expense(st.session_state.token, selected_id, {
                    "amount": upd_amt,
                    "category": upd_cat
                })
                st.success("Expense updated! Please reload the summary to see changes.")

        with col_del:
            if st.button("🗑️ Delete Expense"):
                delete_expense(st.session_state.token, selected_id)
                st.success("Expense deleted! Please reload the summary to see changes.")
else:
    st.info("No expenses available to update or delete for the selected month.")
