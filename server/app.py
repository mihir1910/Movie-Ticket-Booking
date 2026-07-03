from dotenv import load_dotenv
from fastapi import FastAPI

import dbConfig

load_dotenv()

app = FastAPI()


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
