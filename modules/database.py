from fastapi import FastAPI
from modules.models.account import account
import sqlite3

class database:
    def __init__(self, app:FastAPI):
        """
        Initalize the database using provided information and self assign attributes.
        """
        self.app = app

        self.connection = sqlite3.connect(".db")
        self.cursor = self.connection.cursor()

    def init(self): 
        """
        Check that all tables exist and if not create them
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        savedTables = self.cursor.fetchall()

        if savedTables is None or ("accounts",) not in savedTables: self.createAccountDatabase()
        if savedTables is None or ("zooBookings",) not in savedTables: self.createZooBookingsDatabase()
        if savedTables is None or ("accomodationBookings",) not in savedTables: self.createAccomodationBookingsDatabase()

        self.connection.commit()

    def createAccountDatabase(self):
        print("Creating account table and administrator account")
        
        self.cursor.execute("CREATE TABLE accounts (ID varchar(36), Email varchar(255), Password varchar(255), SecurityQuestion varchar(255), SecurityAnswer varchar(255), Administrator BIT)")
        
        adminstrator = account(self.app)
        adminstrator.createAccount(self.app.config.admin[0], self.app.config.admin[1], None, None, True)

    def createZooBookingsDatabase(self):
        print("Creating zoo bookings database")

        self.cursor.execute("CREATE TABLE zooBookings (ID varchar(36), User varchar(36), Date varchar(27), Registration varchar(10))")

    def createAccomodationBookingsDatabase(self):
        print("Creating accomodation bookings database")

        self.cursor.execute("CREATE TABLE accomodationBookings (ID varchar(36), User varchar(36), Start varchar(27), End varchar(27), Room int, Type varchar(256))")