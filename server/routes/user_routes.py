import bcrypt
from fastapi import APIRouter
from fastapi.responses import JSONResponse

import dbConfig
from models.user_model import User

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
        new_user["_id"] = str(new_user["_id"])

        return {
            "success": True,
            "message": "User Registered Successfully",
            "user": new_user,
        }
    except Exception as error:
        return JSONResponse(status_code=500, content={"message": str(error)})
