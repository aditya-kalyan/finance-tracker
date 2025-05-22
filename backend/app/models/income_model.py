from pydantic import BaseModel
from typing import Optional
from datetime import datetime
    
class IncomeCreate(BaseModel):
    amount: int
    source: Optional [str]=None
    # date: datetime 
    
class IncomeResponse(IncomeCreate):
    id : str
    date: datetime