import bcrypt
from fastapi import APIRouter
from fastapi.responses import JSONResponse

import dbConfig
from models.user_model import LoginRequest, User

router = APIRouter()


# Signup route
@router.post("/register")
async def register(user: User):
    try:
        user_exists = await dbConfig.db["users"].find_one({"email": user.email})
        if user_exists:
            return {
                "success": False,
                "message": "User Already Exists with the Email",
            }

        # hash the password
        salt = bcrypt.gensalt(10)
        user.password = bcrypt.hashpw(user.password.encode(), salt).decode()

        result = await dbConfig.db["users"].insert_one(user.model_dump())
        new_user = await dbConfig.db["users"].find_one({"_id": result.inserted_id})
        new_user["id"] = str(new_user.pop("_id"))

        return {
            "success": True,
            "message": "User Registered Successfully",
            "user": new_user,
        }
    except Exception as error:
        return JSONResponse(status_code=500, content={"message": str(error)})
    
@router.post("/login")
async def login(credentials: LoginRequest):
    try:
        user_data = await dbConfig.db["users"].find_one({"email": credentials.email})
        if not user_data:
            return {
                "success": False,
                "message": "User not Registered, Register yourself first",
            }

        if not bcrypt.checkpw(credentials.password.encode(), user_data["password"].encode()):
            return {
                "success": False,
                "message": "Invalid password, Please try again",
            }

        user_data["id"] = str(user_data.pop("_id"))

        return {
            "success": True,
            "message": "User Logged In Successfully",
            "user": user_data,
        }
    except Exception as error:
        return JSONResponse(status_code=500, content={"message": str(error)})