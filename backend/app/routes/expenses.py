from fastapi import APIRouter, HTTPException,Depends
from typing import List
from app.core.database import database
from app.models.expense_model import ExpenseCreate, ExpenseResponse
from bson import ObjectId
from datetime import datetime
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/create", response_model=ExpenseResponse)
async def create_expense(expense: ExpenseCreate, user_email: str = Depends(get_current_user)):
    """Create a new expense entry"""
    expense_dict = expense.model_dump(by_alias=True)
    expense_dict['date'] = datetime.now()
    expense_dict['user_email'] = user_email

    result = await database["expenses"].insert_one(expense_dict)

    expense_dict["id"] = str(result.inserted_id)
    return ExpenseResponse(**expense_dict)

@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: str,
    user_email: str = Depends(get_current_user)
):
    """Retrieve an expense by ID (only if belongs to the user)"""
    try:
        expense = await database["expenses"].find_one({
            "_id": ObjectId(expense_id),
            "user_email": user_email
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense ID format")

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense["id"] = str(expense["_id"])
    expense.pop("_id", None)
    return ExpenseResponse(**expense)

@router.get("/", response_model=List[ExpenseResponse])
async def get_all_expenses(user_email: str = Depends(get_current_user)):
    """Retrieve all expenses of the authenticated user"""
    expenses = await database["expenses"].find({"user_email": user_email}).to_list(100)

    return [
        ExpenseResponse(**{**expense, "id": str(expense["_id"])})
        for expense in expenses
    ]

@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: str,
    expense: ExpenseCreate,
    user_email: str = Depends(get_current_user)
):
    """Update an existing expense (only if belongs to the user)"""
    try:
        obj_id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense ID format")

    expense_dict = expense.model_dump(by_alias=True)
    result = await database["expenses"].update_one(
        {"_id": obj_id, "user_email": user_email},  # Check user owns this
        {"$set": expense_dict}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found or not yours")

    expense_dict["id"] = expense_id
    return ExpenseResponse(**expense_dict)


@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: str,
    user_email: str = Depends(get_current_user)
):
    """Delete an expense by ID (only if belongs to the user)"""
    try:
        obj_id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense ID format")

    result = await database["expenses"].delete_one({
        "_id": obj_id,
        "user_email": user_email  # Make sure it’s user's expense
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found or not yours")

    return {"message": "Expense deleted"}