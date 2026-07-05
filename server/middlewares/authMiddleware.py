import os

import jwt
from fastapi import Cookie, HTTPException, status


async def is_auth(jwtToken: str | None = Cookie(default=None)) -> str:
    if not jwtToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized , no token")

    try:
        decoded = jwt.decode(jwtToken, os.environ["JWT_SECRET"], algorithms=["HS256"])
        return decoded["userId"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized , token validation failed")
