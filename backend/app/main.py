from fastapi import FastAPI
from app.routes import  expenses,income,reports,auth

app = FastAPI()

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(income.router, prefix="/income", tags=["Income"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
# app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Budget Tracker API"}
