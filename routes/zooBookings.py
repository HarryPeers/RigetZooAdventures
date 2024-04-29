from fastapi import *
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from modules.models.bookings import timeSlot
from modules.models.account import account

import os

router = APIRouter()

@router.post("/api/bookings/zoo/create")
async def createZooBooking(request: Request, start:str, registration:str=""): 
    """
    Create the booking attached to a user account.
    """

    # Initiate the timeslot object
    slot = timeSlot(start)

    # Initalize and retrieve account information
    user = account(request.app, headers=request.headers)

    # Create the zoo booking with the provided information.
    booking = await user.createZooBooking(slot, registration)

    # Return the booking as json
    return booking.json()

@router.get("/api/bookings/zoo/")
async def getAllZooBookings(request: Request, expired:bool=True): 
    """
    Get all zoo bookings of a user
    """

    # Initalize and retrieve account information
    user = account(request.app, headers=request.headers)

    # Get all user bookings and return in a json list
    return [x.json() for x in await user.getAllZooBookings(expired)]