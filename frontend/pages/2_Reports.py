import streamlit as st
from datetime import datetime
from utils.api_calls import get_yearly_summary, get_by_month, download_excel_report

st.title("📂 Reports")

token = st.session_state.get("token", None)
if not token:
    st.warning("Please login first")
    st.stop()

year = st.number_input("Year", value=datetime.now().year)

if st.button("📈 Show Yearly Summary"):
    data = get_yearly_summary(token, year)
    st.write(data["monthly_summary"])

month = st.number_input("Month", value=datetime.now().month, min_value=1, max_value=12)

if st.button("📃 Show Monthly Details"):
    data = get_by_month(token, year, month)
    st.subheader("Income")
    st.table(data["incomes"])
    st.subheader("Expenses")
    st.table(data["expenses"])

st.subheader("📥 Download Report")
report_type = st.selectbox("Report Type", ["monthly", "yearly"])
if st.button("Download Excel"):
    report = download_excel_report(report_type, year, month if report_type == "monthly" else None)
    st.download_button("Download", report.content, f"{report_type}_report.xlsx")
