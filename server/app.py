from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import dbConfig
from routes.user_routes import router as user_router
from routes.movie_routes import router as movie_router
from routes.theatre_routes import router as theatre_router

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/auth")
app.include_router(movie_router, prefix="/api/movie")
app.include_router(theatre_router, prefix="/api/theatre")


@app.on_event("startup")
async def startup():
    await dbConfig.connect_db()


@app.get("/")
def read_root():
    return "Hello from Server!"


if __name__ == "__main__":

    print("Server is running on port 8005")
    uvicorn.run(app, host="0.0.0.0", port=8005)
