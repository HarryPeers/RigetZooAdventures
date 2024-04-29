from datetime import datetime, timedelta
from random import choice
from fastapi import FastAPI
from uuid import uuid4
from fastapi.exceptions import HTTPException
from .bookings import zooBooking, timeSlot, accomodationBooking

import bcrypt

global alphabet
alphabet = "abcdefghijklmnopqurstvwxyz"
alphabet += alphabet.upper()

global specialChars
specialChars = "1234567890!£$%^*()-_="

global charSet 
charSet = list(alphabet) + list(specialChars)

def generateTokenString(length:int=255) -> str: return "".join([choice(charSet) for x in range(length)])

class elevatedAccessToken:
    def __init__(self, account:object, token:str=None, securityAnswer:str=None, load:bool=True, overwrite:bool=False):
        """
        Initalize the object and self assign variables.
        """
        self.account = account
        self.providedSecurityAnswer = securityAnswer
        self.overwrite = overwrite

        self.valid = False
        self.token = token
        self.expires = None

        # Attempt to either overwrite or load the token from the app memory
        if overwrite: self.generate(overwrite)
        if load: self.load()

    def generate(self, overwrite:bool=False):
        """
        Generate the token
        """

        # If overwrite, delete any current tokens linked to the given account and generate a new one.
        if overwrite and self.account != None: 
            for token in list(self.account.app.elevatedAccessTokens.values()): 
                if token.account.id == self.account.id: token.revoke()

        # Validate the security answer.
        if not self.account.validateAccountSecurityQuestion(self.providedSecurityAnswer): return

        # Self assign variables.
        self.valid = True
        self.token = generateTokenString(255)

        # Set expiry.
        self.expires = datetime.now() + timedelta(0, 1800) # 48 hours in seconds.

        # Save token in memory.
        self.account.app.elevatedAccessTokens[self.token] = self
    
    def locate(self, inherit:bool=False) -> bool:
        """
        Attempt to find the token in the apps memory by searching for token string.
        """
        if self.token in list(self.account.app.elevatedAccessTokens.keys()):
            if inherit: self.inherit(self.account.app.elevatedAccessTokens[self.token])
            return True
        return False
    
    def inherit(self, token):
        """
        Inherit the attributes from another token object.
        """
        self.account = token.account
        self.valid = token.valid
        self.token = token.token
        self.expires = token.expires

    def load(self, generate:bool=True):
        """
        Attempt to load the existing token or create a new token.
        """
        if self.token != None and self.locate(inherit=True): return
        elif generate: self.generate()

    def json(self) -> dict:
        """
        Return the token object as a JSON parsable dict.
        """
        return {
            "expiry": self.expires.isoformat(),
            "token": self.token,
            "elevated": True
        }
    
    def revoke(self):
        """
        Delete the token
        """
        self.valid = False
        self.expires = datetime.now()
        
        # Remove the token from memory.
        if self.locate(False): del self.account.app.elevatedAccessTokens[self.token]
   
class accessToken:
    def __init__(self, account:object, token:str=None, password:str=None, load:bool=True, overwrite:bool=False):
        """
        Initalize the object and self assign variables.
        """
        self.account = account
        self.providedPassword = password
        self.overwrite = overwrite

        self.valid = False
        self.token = token
        self.expires = None

        # Attempt to either overwrite or load the token from the app memory
        if overwrite: self.generate(overwrite)
        if load: self.load()

    def generate(self, overwrite:bool=False):
        """
        Generate the token
        """

        # If overwrite, delete any current tokens linked to the given account and generate a new one.
        if overwrite and self.account != None: 
            for token in list(self.account.app.activeTokens.values()): 
                if token.account.id == self.account.id: token.revoke()

        # Validate the password.
        if not self.account.validateAccount(self.providedPassword): return

        # Self assign variables.
        self.valid = True
        self.token = generateTokenString(255)

        # Set expiry.
        self.expires = datetime.now() + timedelta(0, 172800) # 48 hours in seconds.

        # Save token in memory.
        self.account.app.activeTokens[self.token] = self
    
    def locate(self, inherit:bool=False) -> bool:
        """
        Attempt to find the token in the apps memory by searching for token string.
        """
        if self.token in list(self.account.app.activeTokens.keys()):
            if inherit: self.inherit(self.account.app.activeTokens[self.token])
            return True
        return False
    
    def inherit(self, token):
        """
        Inherit the attributes of another token object
        """
        self.account = token.account
        self.valid = token.valid
        self.token = token.token
        self.expires = token.expires

    def load(self, generate:bool=True):
        """
        Attempt to load the existing token or create a new token.
        """
        if self.token != None and self.locate(inherit=True): return
        elif generate: self.generate()

    def json(self) -> dict:
        """
        Return the token object as a JSON parsable dict.
        """
        return {
            "expiry": self.expires.isoformat(),
            "token": self.token,
            "elevated": False
        }
    
    def revoke(self):
        """
        Delete the token
        """
        self.valid = False
        self.expires = datetime.now()
        
        # Remove the token from memory.
        if self.locate(False): del self.account.app.activeTokens[self.token]
    
class account:
    def __init__(self, app:FastAPI, id:str=None, email:str=None, token:accessToken=None, elevatedToken:elevatedAccessToken=None, load:bool=True, headers:dict=None):
        """
        Initalize the user object and self assign variables.
        """
        self.app = app
        self.headers = headers

        self.id = id
        self.email = email

        self.token = token
        self.elevatedToken = elevatedToken

        self.password = None
        self.securityQuestion = None
        self.securityAnswer = None
        self.administrator = None

        # If headers are provided attempt to load from token in header.
        if self.headers != None and "authorization" in list(self.headers.keys()): self.validateAccountByToken(self.headers["authorization"])

        # Load the user record.
        if load: self.loadRecord()

    @property
    def dbCursor(self): return self.app.database.cursor

    @property
    def dbConnection(self): return self.app.database.connection

    def createAccount(self, email:str, password:str, securityQuestion:str, securityAnswer:str, administrator:bool=False): 
        """
        Insert the account into the database
        """

        # Return if account already exists
        if self.id != None: return
        
        # Generate a new user GUID
        self.id = str(uuid4())

        # Self assign variables
        self.email = email
        self.password = bcrypt.hashpw(password.strip().encode("utf-8"), bcrypt.gensalt())
        self.securityQuestion = securityQuestion
        self.securityAnswer = None if securityAnswer is None else bcrypt.hashpw(securityAnswer.strip().upper().encode("utf-8"), bcrypt.gensalt())
        self.administrator = administrator

        # Execute command into database.
        self.dbCursor.execute(f"INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)", (self.id, self.email, self.password, self.securityQuestion, self.securityAnswer, self.administrator,))
        self.dbConnection.commit()

    def changePassword(self, eaToken:str, password:str) -> bool:
        """
        Change the password of an account once the elevated access token has been authenticated.
        """

        # Authenticate elevated token.
        authenticated = self.validateAccountByEAToken(eaToken)
        
        # Return if not authenticated
        if not authenticated: return False

        # Revoke the provided token.
        self.elevatedToken.revoke()

        # Hash the new password
        newPassword = bcrypt.hashpw(password.strip().encode("utf-8"), bcrypt.gensalt())

        # Apply changes to the database
        self.dbCursor.execute(f"UPDATE accounts SET Password=? WHERE Id=?;", (newPassword, self.id,))
        self.password = newPassword

        # Save changes
        self.dbConnection.commit()

        return True

    def validateAccount(self, password:str) -> bool: 
        """
        Check to see that the password provided matches the stored password.
        """

        # Validate the provided password against the stored password.
        if password is None or self.id is None: return False
        return bcrypt.checkpw(password.strip().encode("utf-8"), self.password)

    def validateAccountByToken(self, token:str, raiseException:bool=True) -> bool:
        """
        Validate the account through an access token
        """

        # Retrieve the token from app memory.
        self.token = accessToken(self, token, load=True)

        # Inherit the provided user details, and handle non-authentication errors.
        if self.token.valid: self.inherit(self.token.account)
        elif raiseException: raise HTTPException(401, "You could not be authorized!")
        else: return False

        return True
    
    def validateAccountByEAToken(self, token:str, raiseException:bool=True) -> bool:
        """
        Validate the account through an access token
        """

        # Retrieve the token from app memory.
        self.elevatedToken = elevatedAccessToken(self, token, load=True)

        # Inherit the provided user details, and handle non-authentication errors.
        if self.elevatedToken.valid: self.inherit(self.elevatedToken.account)
        elif raiseException: raise HTTPException(401, "You could not be authorized!")
        else: return False

        return True

    def validateAccountSecurityQuestion(self, answer:str) -> bool:
        """
        Check that the provided security question answer is correct.
        """
        
        # Validate the provided answer against the stored answer.
        if answer is None or self.id is None: return False
        return bcrypt.checkpw(answer.strip().upper().encode("utf-8"), self.securityAnswer)

    def generateToken(self, password:str, overwrite:bool=False) -> accessToken: 
        """
        Generate a new access token once password has been validated.
        """

        # Generate a token
        self.token = accessToken(self, self.token, password, True, overwrite)

        return self.token

    def generateElevatedToken(self, securityAnswer:str, overwrite:bool=False) -> elevatedAccessToken:
        """
        Generate a new elevated access token
        """

        # Generate an elevated access token
        self.elevatedToken = elevatedAccessToken(self, None, securityAnswer, True, overwrite)

        return self.elevatedToken
        
    def inherit(self, account:object):
        """
        Inherit attributes from other account object
        """
        self.email = account.email
        self.id = account.id

        self.password = account.password
        self.securityQuestion = account.securityQuestion
        self.securityAnswer = account.securityAnswer
        self.administrator = account.administrator
    

    def loadRecord(self):
        query = None

        # Build a query with provided information
        if self.id != None and self.email != None: query = ("SELECT * FROM accounts WHERE Id=? AND Email=?;", (self.id, self.email,))
        elif self.id != None: query = ("SELECT * FROM accounts WHERE Id=?", (self.id,))
        elif self.email != None: query = ("SELECT * FROM accounts WHERE Email=?", (self.email,))

        # If no query could be determined, return
        if query is None: return

        # Execute the query
        self.dbCursor.execute(query[0], query[1])
        result = self.dbCursor.fetchone()

        # Return if no record found.
        if result is None or len(result) == 0: return

        # Self assign attributes.
        self.id = result[0]
        self.email = result[1]
        self.password = result[2]
        self.securityQuestion = result[3]
        self.securityAnswer = result[4]
        self.administrator = result[5]

    """
    Zoo bookings
    """

    async def createZooBooking(self, timeSlot, registration) -> zooBooking:
        """
        Create a zoo booking
        """

        # Create booking object.
        booking = zooBooking(self.app, timeSlot, self)

        # Generate booking
        booking.createBooking(registration)

        return booking

    async def getAllZooBookings(self, expired=True) -> list[zooBooking]: 
        """
        Return all zoo booking information
        """
        
        # Query database
        self.dbCursor.execute("SELECT * FROM zooBookings WHERE User=?;", (self.id,))
        result = self.dbCursor.fetchall()

        # build list of zoo booking objects from records.
        return [zooBooking(self.app, timeSlot(record[2]), self, self.id, record[0], record[3], False) for record in result]

    """
    Accomodation bookings
    """

    async def createAccomodationBooking(self, timeSlot, type, number) -> zooBooking:
        """
        Create a zoo booking
        """

        # Create accomodation object.
        booking = accomodationBooking(self.app, timeSlot, self)

        # Generate booking
        booking.createBooking(type, number)

        return booking
    
    async def getAllAccomodationBookings(self, expired=True) -> list[zooBooking]: 
        """
        Return all zoo booking information
        """
        
        #Query database
        self.dbCursor.execute("SELECT * FROM accomodationBookings WHERE User=?;", (self.id,))
        result = self.dbCursor.fetchall()

        # Build list of accomodation booking objects from records.
        return [accomodationBooking(self.app, timeSlot(record[2], record[3]), self, self.id, record[0], record[5], record[4], False) for record in result]

    """
    All bookings
    """

    async def getAllBookings(self, expired=True, ordered=True):
        #Fetch each list individually and merge.
        bookings = await self.getAllZooBookings(expired) + await self.getAllAccomodationBookings(expired)

        if not ordered: return bookings

        # Order the bookings by the start date.        
        return sorted(bookings, key=lambda x: x.timeslot.startToDate())