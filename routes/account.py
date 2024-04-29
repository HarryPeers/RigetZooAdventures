from fastapi import *
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from modules.models.bookings import timeSlot
from modules.models.account import account

import os

router = APIRouter()

@router.get("/api/bookings/")
async def createAccomodationBooking(request: Request, expired:bool=True, ordered:bool=True): 
    """
    Get all bookings including zoo and accomodation for the user.
    """

    # Initalize and retrieve account information
    user = account(request.app, headers=request.headers)

    # Get all booings and convert to a json list.
    return [x.json() for x in await user.getAllBookings(expired, ordered)]
