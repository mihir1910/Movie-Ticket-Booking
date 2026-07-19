from bson import ObjectId
from fastapi import APIRouter

import dbConfig
from models.theatre_model import Theatre

router = APIRouter()


@router.post("/add-theatre")
async def add_theatre(theatre: Theatre):
    try:
        result = await dbConfig.db["theatres"].insert_one(theatre.model_dump())
        saved_theatre = await dbConfig.db["theatres"].find_one({"_id": result.inserted_id})
        saved_theatre["id"] = str(saved_theatre.pop("_id"))
        return {
            "success": True,
            "message": "New theatre has been added!",
            "data": saved_theatre,
        }
    except Exception as err:
        return {
            "success": False,
            "message": str(err),
        }


# Get all theatres for Admin route
@router.get("/get-all-theatres")
async def get_all_theatres():
    try:
        all_theatres = await dbConfig.db["theatres"].find().to_list()
        for theatre in all_theatres:
            theatre["id"] = str(theatre.pop("_id"))
        return {
            "success": True,
            "message": "All theatres fetched!",
            "data": all_theatres,
        }
    except Exception as err:
        return {
            "success": False,
            "message": str(err),
        }


@router.post("/get-all-theatres-by-owner")
async def get_all_theatres_by_owner(payload: dict):
    try:
        all_theatres = await dbConfig.db["theatres"].find({"owner": payload.get("owner")}).to_list()
        for theatre in all_theatres:
            theatre["id"] = str(theatre.pop("_id"))
        return {
            "success": True,
            "message": "All theatres fetched successfully!",
            "data": all_theatres,
        }
    except Exception as err:
        return {
            "success": False,
            "message": str(err),
        }


# Update theatre
@router.put("/update-theatre")
async def update_theatre(payload: dict):
    try:
        theatre_id = payload.pop("theatreId")
        await dbConfig.db["theatres"].update_one({"_id": ObjectId(theatre_id)}, {"$set": payload})
        return {
            "success": True,
            "message": "Theatre has been updated!",
        }
    except Exception as err:
        return {
            "success": False,
            "message": str(err),
        }


# Delete theatre
@router.put("/delete-theatre")
async def delete_theatre(payload: dict):
    try:
        theatre_id = payload.get("theatreId")
        await dbConfig.db["theatres"].delete_one({"_id": ObjectId(theatre_id)})
        return {
            "success": True,
            "message": "The theatre has been deleted!",
        }
    except Exception as err:
        return {
            "success": False,
            "message": str(err),
        }
