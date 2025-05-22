from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None

class ExpenseResponse(ExpenseCreate):
    id: str 
    date: datetime
