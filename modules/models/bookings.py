from fastapi import FastAPI
from uuid import uuid4
from datetime import datetime

class timeSlot:
    def __init__(self, start=None, end=None, hour=None, minute=None):
        """
        Initalize and self assign the attributes
        """
        self.start = start
        self.end = end
        self.hour = hour
        self.minute = minute

    def json(self) -> dict:
        """
        Return the information as a json parsable object.
        """
        return {
            "start": self.start,
            "end": self.end,
            "hour": self.hour,
            "minute": self.minute
        }
    
    # Convert the dates to datetime objects.
    def startToDate(self) -> datetime: return datetime.fromisoformat(self.start)
    def endToDate(self)-> datetime: return datetime.fromisoformat(self.end)

class zooBooking:
    def __init__(self, app:FastAPI, timeslot:timeSlot=None, user:object=None, userId=None, id=None, registration:str=None, load:bool=True):
        """
        Initalize and self assign the attributes
        """

        self.app = app

        self.timeslot = timeslot
        self.user = user
        self.userId = user.id if user != None else userId

        self.id = id
        self.registration = registration

        # Attempt to load the details from the database
        if load: self.loadRecord()

    @property
    def dbCursor(self): return self.app.database.cursor

    @property
    def dbConnection(self): return self.app.database.connection

    def loadRecord(self):
        """
        Load the record from the database and assign the values to self.
        """
        query = None

        # Build a query if self.id is given.
        if self.id != None: query = ("SELECT * FROM zooBookings WHERE Id=?;", (self.id,))

        # If no query can be determined return.
        if query is None: return

        # Execute the query and return the result.
        self.dbCursor.execute(query[0], query[1])
        result = self.dbCursor.fetchone()

        # If record not found return
        if result is None or len(result) == 0: return

        # Self assign the values.
        self.id = result[0]
        self.userId = result[1]
        self.timeslot = timeSlot(result[2], None)
        self.registration = result[3]

    def inherit(self, booking:object):
        """
        Inherit attributes from other zoo booking object
        """
        self.id = booking.id
        self.timeslot = booking.timeslot

        self.user = booking.user
        self.userId = booking.userId

        self.registration = booking.registration

    def createBooking(self, registration): 
        """
        Insert the booking into the database
        """

        if self.id != None: return
        
        # Generate the ID and self assign registration.
        self.id = str(uuid4())
        self.registration = registration

        # Execute the command into the database and commit the changes.
        self.dbCursor.execute(f"INSERT INTO zooBookings VALUES (?, ?, ?, ?)", (self.id, self.userId, self.timeslot.start, self.registration,))
        self.dbConnection.commit()


    def json(self) -> dict:
        """
        Return the object as a json parsable dict.
        """
        return {
            "id": self.id,
            "valid": self.id != None,
            "expired": None,
            "registration": self.registration,
            "time": self.timeslot.json(),
            "type": "Safari Adventure"
        }
    
class accomodationBooking:
    def __init__(self, app:FastAPI, timeslot:timeSlot=None, user:object=None, userId=None, id=None, type:str=None, number:int=None, load:bool=True):
        """
        Initalize and self assign the attributes
        """
        self.app = app

        self.timeslot = timeslot
        self.user = user
        self.userId = user.id if user != None else userId

        self.id = id
        self.type = type
        self.number = number

        # Attempt to load the record from the database.
        if load: self.loadRecord()

    @property
    def dbCursor(self): return self.app.database.cursor

    @property
    def dbConnection(self): return self.app.database.connection

    def loadRecord(self):
        query = None

        # Build a query if self.id is given.
        if self.id != None: query = ("SELECT * FROM accomodationBookings WHERE Id=?;", (self.id,))

        # If no query can be determined return.
        if query is None: return

        # Execute the query and return the result.
        self.dbCursor.execute(query[0], query[1])
        result = self.dbCursor.fetchone()

        # If record not found return
        if result is None or len(result) == 0: return

        # Self assign the values.
        self.id = result[0]
        self.userId = result[1]
        self.timeslot = timeSlot(result[2], result[3])
        self.type = result[5]
        self.number = result[4]

    def inherit(self, booking:object):
        """
        Inherit attributes from other zoo booking object
        """
        self.id = booking.id
        self.timeslot = booking.timeslot

        self.user = booking.user
        self.userId = booking.userId

        self.type = booking.type
        self.number = booking.number

    def createBooking(self, type, number): 
        """
        Insert the booking into the database
        """

        if self.id != None: return
        
        # Generate an ID and self assign variables.
        self.id = str(uuid4())
        self.type = type
        self.number = number

        # Execute the command and save changes.
        self.dbCursor.execute(f"INSERT INTO accomodationBookings VALUES (?, ?, ?, ?, ?, ?)", (self.id, self.userId, self.timeslot.start, self.timeslot.end, self.number, self.type,))
        self.dbConnection.commit()

    def json(self) -> dict:
        """
        Return the object as a json parsable dict.
        """
        return {
            "id": self.id,
            "valid": self.id != None,
            "expired": None,
            "type": self.type,
            "number": self.number,
            "time": self.timeslot.json()
        }