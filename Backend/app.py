from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

# Importing from parent directory
import sys
from pathlib import Path

# Add parent directory to sys.path to access models.py and database.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

from models import User, Base
from database import engine, get_db

# FastAPI app setup
app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
Base.metadata.create_all(bind=engine)

# Password hashing using Passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper functions for password hashing and verification
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to get user by username or email
def get_user(db: Session, username: str = None, email: str = None):
    if username:
        return db.query(User).filter(User.username == username).first()
    if email:
        return db.query(User).filter(User.email == email).first()

# Pydantic models for request validation
class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Endpoints
@app.post("/signup")
def signup(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = get_user(db, username=request.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    existing_email = get_user(db, email=request.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = hash_password(request.password)
    new_user = User(username=request.username, email=request.email, hashed_password=hashed_password)
    try:
        db.add(new_user)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user. Please try again later.",
        )
    return {"message": "User created successfully"}

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = get_user(db, username=request.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )
    return {"message": "Login successful"}

# Weather Prediction Endpoint
with open('./model.pkl', "rb") as f:
    model = pickle.load(f)

@app.post("/predict")
def predict(data: dict):
    humidity = data.get("humidity")
    wind_speed = data.get("wind_speed")
    if humidity is None or wind_speed is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both 'humidity' and 'wind_speed' are required",
        )
    df = pd.DataFrame([[humidity, wind_speed]], columns=["Humidity", "Wind Speed"])
    prediction = model.predict(df)
    return {"temperature": prediction[0]}
