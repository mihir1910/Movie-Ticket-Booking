from bson import ObjectId
from fastapi import APIRouter

import dbConfig
from models.show_model import Show

router = APIRouter()


# create a show
@router.post("/add-show")
async def add_show(show: Show):
    try:
        show_data = show.model_dump()
        show_data["movie"] = ObjectId(show_data["movie"])
        show_data["theatre"] = ObjectId(show_data["theatre"])
        await dbConfig.db["shows"].insert_one(show_data)
        return {
            "success": True,
            "message": "New show has been added!",
        }
    except Exception as error:
        return {
            "status": False,
            "message": str(error),
        }


# Delete Show
@router.post("/delete-show")
async def delete_show(payload: dict):
    try:
        await dbConfig.db["shows"].delete_one({"_id": ObjectId(payload.get("showId"))})
        return {
            "success": True,
            "message": "The show has been deleted!",
        }
    except Exception as err:
        return {
            "status": False,
            "message": str(err),
        }


# Update show
@router.put("/update-show")
async def update_show(payload: dict):
    try:
        show_id = payload.pop("showId")
        await dbConfig.db["shows"].update_one({"_id": ObjectId(show_id)}, {"$set": payload})
        return {
            "success": True,
            "message": "The show has been updated!",
        }
    except Exception as err:
        return {
            "success": False,
            "message": str(err),
        }


# get all shows and theatres for a movie
@router.get("/get-all-theatres-by-movie")
async def get_all_theatres_by_movie(payload: dict):
    try:
        movie = payload.get("movie")
        date = payload.get("date")
        shows = await dbConfig.db["shows"].find({"movie": movie, "date": date}).to_list()

        # we need to map the shows with theatres

        return {
            "success": True,
            "message": "Shows Fetched",
            "shows": shows,
        }
    except Exception:
        return {
            "success": False,
            "message": "Shows not Fetched",
        }


# get-show-by-id
@router.get("/get-show-by-id")
async def get_show_by_id(payload: dict):
    try:
        show = dbConfig.db["shows"].find_one({"_id": ObjectId(payload.get("showId"))})
        return {
            "success": True,
            "message": "Show fetched!",
            "data": show,
        }
    except Exception as error:
        return {
            "success": False,
            "message": str(error),
        }


@router.get("/get-all-shows")
async def get_all_shows():
    try:
        all_shows = await dbConfig.db["shows"].aggregate([
            {
                "$lookup": {
                    "from": "movies",
                    "localField": "movie",
                    "foreignField": "_id",
                    "as": "movie",
                }
            },
            {"$unwind": "$movie"},
        ]).to_list()
        for show in all_shows:
            show["id"] = str(show.pop("_id"))
            show["theatre"] = str(show["theatre"])
            show["movie"]["id"] = str(show["movie"].pop("_id"))
        return {
            "success": True,
            "message": "All Shows Fetched",
            "data": all_shows,
        }
    except Exception as error:
        return {
            "success": False,
            "message": f"Not able to fetch Shows {error}",
        }
