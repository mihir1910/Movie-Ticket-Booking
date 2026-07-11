from bson import ObjectId
from fastapi import APIRouter

import dbConfig
from controllers.movie_controllers import add_movie, update_movie

router = APIRouter()


# Add a Movie
router.post("/add-movie")(add_movie)

# update movie
router.put("/update-movie/{movie_id}")(update_movie)


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
