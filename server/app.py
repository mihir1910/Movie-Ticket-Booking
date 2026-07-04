from dotenv import load_dotenv
from fastapi import FastAPI

import dbConfig
from routes.user_routes import router as user_router

load_dotenv()

app = FastAPI()
app.include_router(user_router, prefix="/api/auth")


@app.on_event("startup")
async def startup():
    await dbConfig.connect_db()


@app.get("/")
def read_root():
    return "Hello from Server!"


if __name__ == "__main__":
    import uvicorn

    print("Server is running on port 8005")
    uvicorn.run(app, host="0.0.0.0", port=8005)
