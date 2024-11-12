from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.accommodations import AccommodationService

accommodations_router = APIRouter()
accommodation_service = AccommodationService("accommodations.json")


@accommodations_router.get("/accommodation/{id}", tags=["Accommodations"])
async def get_accommodation(id: int):
    try:
        accommodation = accommodation_service.get_accommodation(id)

        if accommodation:
            return JSONResponse(
                status_code=200,
                content={"message": "Accommodation found", "data": accommodation},
            )
        else:
            return JSONResponse(
                status_code=404, content={"message": "Accommodation not found"}
            )

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": f"Internal Server Error: {e}"}
        )
