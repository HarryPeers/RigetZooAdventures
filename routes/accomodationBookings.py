from fastapi import *
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from modules.models.bookings import timeSlot
from modules.models.account import account

import os

router = APIRouter()

@router.post("/api/bookings/accomodation/create")
async def createAccomodationBooking(request: Request, start:str, end:str, type:str="Accomodation", number:int=0): 
    """
    Create the booking attached to a user account.
    """

    # Initalize timeslot object
    slot = timeSlot(start, end)

    # Initalize and retrieve account information
    user = account(request.app, headers=request.headers)

    # Create the booking
    booking = await user.createAccomodationBooking(slot, type, number)

    # Return the booking information in a json format
    return booking.json()

@router.get("/api/bookings/accomodation/")
async def getAllAccomodationBookings(request: Request, expired:bool=True): 
    """
    Retrieve all bookings related to accomodation
    """

    # Initalize and retrieve account information
    user = account(request.app, headers=request.headers)
    
    # Get all bookings for the user and convert it to a json list.
    return [x.json() for x in await user.getAllAccomodationBookings(expired)]