import os

import jwt
from bson import ObjectId
from fastapi import Cookie, Depends, HTTPException, status

import dbConfig


async def is_auth(jwtToken: str | None = Cookie(default=None)) -> str:
    if not jwtToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized , no token")

    try:
        decoded = jwt.decode(jwtToken, os.environ["JWT_SECRET"], algorithms=["HS256"])
        return decoded["userId"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized , token validation failed")


async def require_partner_or_admin(user_id: str = Depends(is_auth)) -> dict:
    user = await dbConfig.db["users"].find_one({"_id": ObjectId(user_id)})
    if not user or user.get("role") not in ("partner", "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied. Partner or Admin role required.")

    user["id"] = str(user.pop("_id"))
    return user
