from fastapi import APIRouter

import dbConfig
from models.movie_model import Movie

router = APIRouter()


# Add a Movie
@router.post("/add-movie")
async def add_movie(movie: Movie):
    try:
        await dbConfig.db["movies"].insert_one(movie.model_dump())
        return {
            "success": True,
            "message": "New movie has been added!",
        }
    except Exception:
        return {
            "success": False,
            "message": "Movie Could not be added",
        }
