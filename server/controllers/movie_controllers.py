from bson import ObjectId

import dbConfig
from models.movie_model import Movie


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


async def update_movie(payload: dict):
    try:
        movie_id = payload.pop("movieId")
        await dbConfig.db["movies"].update_one({"_id": ObjectId(movie_id)}, {"$set": payload})
        updated_movie = await dbConfig.db["movies"].find_one({"_id": ObjectId(movie_id)})
        updated_movie["id"] = str(updated_movie.pop("_id"))
        return {
            "success": True,
            "message": "The movie has been updated!",
            "data": updated_movie,
        }
    except Exception:
        return {
            "success": False,
            "message": "Server Error",
        }
