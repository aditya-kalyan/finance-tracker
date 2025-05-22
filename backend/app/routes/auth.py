from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.core.security import hash_password, verify_password, create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.database import database
from app.models.user_model import UserCreate,UserInDB,UserLogin

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate):
    # Check if user already exists
    existing_user = await database["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password
    hashed_pw = hash_password(user.password)

    # Insert user into the database
    user_data = {"email": user.email, "hashed_password": hashed_pw}
    await database["users"].insert_one(user_data)

    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    # Fetch user by email (username field holds email here)
    db_user = await database["users"].find_one({"email": form_data.username})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Check password
    if not verify_password(form_data.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create JWT token
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user["email"]}, expires_delta=token_expires)

    return {"access_token": access_token, "token_type": "bearer"}