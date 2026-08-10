from bson import ObjectId
from fastapi import APIRouter, Depends

import dbConfig
from middlewares.authMiddleware import require_partner_or_admin
from models.show_model import Show

router = APIRouter()


# create a show (Partner or Admin)
@router.post("/add-show")
async def add_show(show: Show, user: dict = Depends(require_partner_or_admin)):
    try:
        # Security: Partners can only add shows to their own theatres
        if user["role"] == "partner":
            theatre = await dbConfig.db["theatres"].find_one({"_id": ObjectId(show.theatre)})
            if theatre and str(theatre.get("owner")) != user["id"]:
                return {
                    "success": False,
                    "message": "Access denied. You can only add shows to your own theatres.",
                }

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


# Delete Show (Partner or Admin)
@router.post("/delete-show")
async def delete_show(payload: dict, user: dict = Depends(require_partner_or_admin)):
    try:
        show = await dbConfig.db["shows"].find_one({"_id": ObjectId(payload.get("showId"))})
        if not show:
            return {
                "success": False,
                "message": "Show not found",
            }

        theatre = await dbConfig.db["theatres"].find_one({"_id": ObjectId(show["theatre"])})

        # Security: Partners can only delete shows from their own theatres
        if user["role"] == "partner" and theatre and str(theatre.get("owner")) != user["id"]:
            return {
                "success": False,
                "message": "Access denied. You can only delete shows from your own theatres.",
            }

        await dbConfig.db["shows"].delete_one({"_id": ObjectId(payload.get("showId"))})
        return {
            "success": True,
            "message": "The show has been deleted!",
        }
    except Exception as err:
        return {
            "success": False,
            "message": str(err),
        }


# Update show (Partner or Admin)
@router.put("/update-show")
async def update_show(payload: dict, user: dict = Depends(require_partner_or_admin)):
    try:
        show_id = payload.get("showId")
        show = await dbConfig.db["shows"].find_one({"_id": ObjectId(show_id)})
        if not show:
            return {
                "success": False,
                "message": "Show not found",
            }

        theatre = await dbConfig.db["theatres"].find_one({"_id": ObjectId(show["theatre"])})

        # Security: Partners can only update shows from their own theatres
        if user["role"] == "partner" and theatre and str(theatre.get("owner")) != user["id"]:
            return {
                "success": False,
                "message": "Access denied. You can only update shows from your own theatres.",
            }

        update_data = {k: v for k, v in payload.items() if k != "showId"}
        await dbConfig.db["shows"].update_one({"_id": ObjectId(show_id)}, {"$set": update_data})
        return {
            "success": True,
            "message": "The show has been updated!",
        }
    except Exception as err:
        return {
            "success": False,
            "message": str(err),
        }


# Get all theatres by movie (Public route - users need to see available shows)
@router.post("/get-all-theatres-by-movie")
async def get_all_theatres_by_movie(payload: dict):
    try:
        movie = payload.get("movie")
        date = payload.get("date")
        shows = await dbConfig.db["shows"].aggregate([
            {"$match": {"movie": ObjectId(movie), "date": date}},
            {
                "$lookup": {
                    "from": "theatres",
                    "localField": "theatre",
                    "foreignField": "_id",
                    "as": "theatre",
                }
            },
            {"$unwind": "$theatre"},
        ]).to_list()

        for show in shows:
            show["id"] = str(show.pop("_id"))
            show["theatre"]["id"] = str(show["theatre"]["_id"])

        # we need to map the shows with unique theatres

        unique_theatres = []
        for show in shows:
            is_theatre = next(
                (t for t in unique_theatres if t["id"] == show["theatre"]["id"]), None
            )
            if not is_theatre:
                shows_of_this_theatre = [
                    s for s in shows if s["theatre"]["id"] == show["theatre"]["id"]
                ]
                unique_theatres.append({
                    **show["theatre"],
                    "shows": shows_of_this_theatre,
                })

        return {
            "success": True,
            "message": "Shows Fetched",
            "shows": unique_theatres,
        }
    except Exception:
        return {
            "success": False,
            "message": "Shows not Fetched",
        }


# get-show-by-id (Public route - anyone can view show details)
@router.post("/get-show-by-id")
async def get_show_by_id(payload: dict):
    try:
        shows = await dbConfig.db["shows"].aggregate([
            {"$match": {"_id": ObjectId(payload.get("showId"))}},
            {
                "$lookup": {
                    "from": "movies",
                    "localField": "movie",
                    "foreignField": "_id",
                    "as": "movie",
                }
            },
            {"$unwind": "$movie"},
            {
                "$lookup": {
                    "from": "theatres",
                    "localField": "theatre",
                    "foreignField": "_id",
                    "as": "theatre",
                }
            },
            {"$unwind": "$theatre"},
        ]).to_list()

        show = shows[0] if shows else None
        if show:
            show["id"] = str(show.pop("_id"))
            show["movie"]["id"] = str(show["movie"].pop("_id"))
            show["theatre"]["id"] = str(show["theatre"].pop("_id"))

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


@router.post("/get-all-shows")
async def get_all_shows(payload: dict, user: dict = Depends(require_partner_or_admin)):
    try:
        theatre_id = payload.get("thearteId")

        # Security: Partners can only see shows from their own theatres
        if user["role"] == "partner" and theatre_id:
            theatre = await dbConfig.db["theatres"].find_one({"_id": ObjectId(theatre_id)})
            if theatre and str(theatre.get("owner")) != user["id"]:
                return {
                    "success": False,
                    "message": "Access denied. You can only view shows from your own theatres.",
                }

        all_shows = await dbConfig.db["shows"].aggregate([
            {"$match": {"theatre": ObjectId(theatre_id)}},
            {
                "$lookup": {
                    "from": "movies",
                    "localField": "movie",
                    "foreignField": "_id",
                    "as": "movie",
                }
            },
            {"$unwind": "$movie"},
            {
                "$lookup": {
                    "from": "theatres",
                    "localField": "theatre",
                    "foreignField": "_id",
                    "as": "theatre",
                }
            },
            {"$unwind": "$theatre"},
        ]).to_list()

        for show in all_shows:
            show["id"] = str(show.pop("_id"))
            show["movie"]["id"] = str(show["movie"].pop("_id"))
            show["theatre"]["id"] = str(show["theatre"].pop("_id"))

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
