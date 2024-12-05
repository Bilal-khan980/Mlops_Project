from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User, Base
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

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

# Helper function to hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to get user by username or email
def get_user(db: Session, username: str = None, email: str = None):
    if username:
        return db.query(User).filter(User.username == username).first()
    if email:
        return db.query(User).filter(User.email == email).first()

# Pydantic model for register request
class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

# Signup Endpoint
@app.post("/signup")
def signup(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if the username already exists
    existing_user = get_user(db, username=request.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Check if the email already exists
    existing_email = get_user(db, email=request.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = hash_password(request.password)
    
    # Create new user
    new_user = User(username=request.username, email=request.email, hashed_password=hashed_password)
    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user. Please try again later."
        )
    
    return {"message": "User created successfully"}

# Pydantic model for login request
class LoginRequest(BaseModel):
    username: str
    password: str

# Login Endpoint
@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Check if the user exists
    user = get_user(db, username=request.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify the password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    return {"message": "Login successful"}

# Weather Prediction Endpoint
# Load the model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.post("/predict")
def predict(data: dict):
    humidity = data["humidity"]
    wind_speed = data["wind_speed"]
    df = pd.DataFrame([[humidity, wind_speed]], columns=["Humidity", "Wind Speed"])
    prediction = model.predict(df)
    return {"temperature": prediction[0]}
