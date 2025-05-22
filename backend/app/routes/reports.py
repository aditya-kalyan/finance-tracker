from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.core.database import database
from datetime import datetime
from typing import Dict,List
from calendar import monthrange, month_name
from io import BytesIO
from openpyxl import Workbook
from app.models.expense_model import ExpenseResponse
from app.models.income_model import IncomeResponse



router = APIRouter()

# Utility to get start & end dates for a given month
def get_month_date_range(year: int, month: int):
    start_date = datetime(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = datetime(year, month, last_day, 23, 59, 59)
    return start_date, end_date

def get_year_date_range(year: int):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31, 23, 59, 59)
    return start_date, end_date

@router.get("/month", tags=["Reports"])
async def get_monthly_summary(
    year: int = Query(default=datetime.now().year, ge=2000),
    month: int = Query(default=datetime.now().month, ge=1, le=12)
) -> Dict:
    """Returns total income and expenses for a given month/year"""
    start_date, end_date = get_month_date_range(year, month)

    expenses_cursor = database["expenses"].aggregate([
        {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ])
    incomes_cursor = database["income"].aggregate([
        {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ])

    expenses = await expenses_cursor.to_list(length=1)
    incomes = await incomes_cursor.to_list(length=1)

    return {
        "year": year,
        "month": month,
        "total_expenses": expenses[0]["total"] if expenses else 0,
        "total_income": incomes[0]["total"] if incomes else 0
    }

@router.get("/year", tags=["Reports"])
async def get_yearly_summary(
    year: int = Query(default=datetime.now().year, ge=2000)
) -> Dict:
    """Returns total income and expenses for a given year"""
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31, 23, 59, 59)

    expenses_cursor = database["expenses"].aggregate([
        {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ])
    incomes_cursor = database["incomes"].aggregate([
        {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ])

    expenses = await expenses_cursor.to_list(length=1)
    incomes = await incomes_cursor.to_list(length=1)

    return {
        "year": year,
        "total_expenses": expenses[0]["total"] if expenses else 0,
        "total_income": incomes[0]["total"] if incomes else 0
    }

@router.get("/by-month", response_model=List[ExpenseResponse])
async def get_monthly_income_expense(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12)
) -> Dict[str, List]:
    """Returns all expenses and incomes for a specific month and year"""

    # Time range
    start_date = datetime(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = datetime(year, month, last_day, 23, 59, 59)

    # Get expenses
    expenses = await database["expenses"].find({
        "date": {"$gte": start_date, "$lte": end_date}
    }).to_list(1000)
    expense_list = [ExpenseResponse(**expense, id=str(expense["_id"])) for expense in expenses]

    # Get incomes
    incomes = await database["incomes"].find({
        "date": {"$gte": start_date, "$lte": end_date}
    }).to_list(1000)
    income_list = [IncomeResponse(**income, id=str(income["_id"])) for income in incomes]

    return {
        "month": f"{month:02}-{year}",
        "expenses": expense_list,
        "incomes": income_list
    }

@router.get("/by-year", response_model=List[ExpenseResponse])
async def get_yearly_income_expense_summary(
    year: int = Query(default=datetime.now().year, ge=2000)
) :
    """Returns total expenses and income for each month in a given year"""

    monthly_summary = []

    for month in range(1, 13):
        start_date = datetime(year, month, 1)
        last_day = monthrange(year, month)[1]
        end_date = datetime(year, month, last_day, 23, 59, 59)

        # Aggregate expenses
        expense_cursor = database["expenses"].aggregate([
            {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ])
        expenses = await expense_cursor.to_list(length=1)
        total_expenses = expenses[0]["total"] if expenses else 0

        # Aggregate income
        income_cursor = database["incomes"].aggregate([
            {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ])
        incomes = await income_cursor.to_list(length=1)
        total_income = incomes[0]["total"] if incomes else 0

        monthly_summary.append({
            "month": month_name[month], 
            "total_expenses": total_expenses,
            "total_income": total_income
        })

    return {
        "year": year,
        "monthly_summary": monthly_summary
    }
    
@router.get("/reports/export")
async def generate_excel_report(
    report_type: str = Query(..., enum=["yearly", "monthly"]),
    year: int = Query(default=datetime.now().year),
    month: int = Query(None),
):
    wb = Workbook()
    ws = wb.active

    if report_type == "yearly":
        ws.title = f"Yearly Report {year}"
        ws.append(["Month", "Total Income", "Total Expenses"])

        for m in range(1, 13):
            start = datetime(year, m, 1)
            end = datetime(year, m + 1, 1) if m < 12 else datetime(year + 1, 1, 1)

            income_sum = await database["income"].aggregate([
                {"$match": {"date": {"$gte": start, "$lt": end}}},
                {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
            ]).to_list(length=1)
            
            expense_sum = await database["expenses"].aggregate([
                {"$match": {"date": {"$gte": start, "$lt": end}}},
                {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
            ]).to_list(length=1)

            income = income_sum[0]["total"] if income_sum else 0
            expense = expense_sum[0]["total"] if expense_sum else 0

            ws.append([start.strftime("%B"), income, expense])

    elif report_type == "monthly":
        if not month:
            return {"error": "Month is required for monthly report"}
        
        start = datetime(year, month, 1)
        next_month = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

        ws.title = f"{start.strftime('%B')} Report"
        ws.append(["Date", "Category", "Amount", "Type"])

        # Expenses
        expenses = await database["expenses"].find({"date": {"$gte": start, "$lt": next_month}}).to_list(None)
        for e in expenses:
            ws.append([e["date"].strftime("%Y-%m-%d"), e.get("category", ""), e["amount"], "Expense"])

        # Income total
        income_sum = await database["income"].aggregate([
            {"$match": {"date": {"$gte": start, "$lt": next_month}}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]).to_list(length=1)
        
        income_total = income_sum[0]["total"] if income_sum else 0

        ws.append([])
        ws.append(["Total Income", income_total])

    # Save Excel to bytes
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"{report_type}_report_{year}_{month or ''}.xlsx"
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": f"attachment; filename={filename}"})