from fastapi import APIRouter, HTTPException, status
from app.models.user_model import User, UserLogin
import json
import os

router = APIRouter(tags=["Authentication"])

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

@router.post("/signup")
async def signup(user: User):
    users = load_users()
    
    # Check if user already exists
    if any(u["imr_number"] == user.imr_number for u in users):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this IMR Number already exists."
        )
    
    users.append(user.dict())
    save_users(users)
    return {"message": "Signup successful", "user": user}

@router.post("/login")
async def login(login_data: UserLogin):
    users = load_users()
    
    user = next((u for u in users if u["imr_number"] == login_data.imr_number and u["phone_number"] == login_data.phone_number), None)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid IMR Number or Phone Number."
        )
    
    return {"message": "Login successful", "user": user}
