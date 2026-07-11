from bson import ObjectId
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


# update movie
@router.put("/update-movie/{movie_id}")
async def update_movie(movie_id: str, movie: dict):
    try:
        await dbConfig.db["movies"].update_one({"_id": ObjectId(movie_id)}, {"$set": movie})
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


# Delete Movie
@router.delete("/delete-movie/{movie_id}")
async def delete_movie(movie_id: str):
    try:
        movie = await dbConfig.db["movies"].find_one_and_delete({"_id": ObjectId(movie_id)})
        movie["id"] = str(movie.pop("_id"))
        return {
            "success": True,
            "message": "The movie has been updated!",
            "data": movie,
        }
    except Exception:
        return {
            "success": False,
            "message": "Server Error",
        }


# get all Movies
@router.get("/all-movies")
async def all_movies():
    try:
        all_movies = await dbConfig.db["movies"].find().to_list()
        for movie in all_movies:
            movie["id"] = str(movie.pop("_id"))
        return {
            "success": True,
            "message": "All movies have been fetched!",
            "data": all_movies,
        }
    except Exception as error:
        return {
            "success": False,
            "message": str(error),
        }


# get a specific Movie
@router.get("/{movie_id}")
async def get_movie(movie_id: str):
    try:
        movie = await dbConfig.db["movies"].find_one({"_id": ObjectId(movie_id)})
        movie["id"] = str(movie.pop("_id"))
        return {
            "success": True,
            "message": "Movie fetched successfully!",
            "data": movie,
        }
    except Exception as error:
        return {
            "success": False,
            "message": str(error),
        }
