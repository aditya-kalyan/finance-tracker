from fastapi import APIRouter, HTTPException,Depends
from typing import List
from app.core.database import database
from app.models.income_model import IncomeCreate, IncomeResponse
from bson import ObjectId
from datetime import datetime
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/create", response_model=IncomeResponse)
async def create_income(
    income: IncomeCreate,
    user_email: str = Depends(get_current_user)
):
    income_dict = income.model_dump(by_alias=True)
    income_dict['date'] = datetime.now()
    income_dict['user_email'] = user_email

    result = await database["income"].insert_one(income_dict)
    income_dict["id"] = str(result.inserted_id)

    return IncomeResponse(**income_dict)

@router.get("/", response_model=List[IncomeResponse])
async def get_all_income(
    user_email: str = Depends(get_current_user)  # 🔐 Require JWT token
):
    """Get all income entries for logged-in user"""
    incomes = await database['income'].find({"user_email": user_email}).to_list(100)

    return [
        IncomeResponse(**{**income, "id": str(income["_id"]), "_id": None})
        for income in incomes
    ]
    
    
    