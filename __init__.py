from sys import path as sysPath
import os

sysPath.append("./site-packages")
sysPath.append(f"{os.getcwd()}/site-packages")

from fastapi import *
from modules.config import config
from modules.database import database
from contextlib import asynccontextmanager

import colorama
import uvicorn
import dotenv

from routes.files import router as FileRouter
from routes.authentication import router as AuthenticationRoter
from routes.zooBookings import router as ZooBookingRouter
from routes.accomodationBookings import router as AccomodationBookingRouter
from routes.account import router as AccountRouter

# Initalize the coloured text
colorama.init()


# Initalize the database within the app startup/
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.database = database(app)
    app.database.init()
    yield

# Initalize the API object
app = FastAPI(lifespan=lifespan)

# Assign common variables.
app.config = config()
app.database = None

# Assign the list of active tokens and elevated tokens as empty dicts.
app.activeTokens = {}
app.elevatedAccessTokens = {}

# Import the routers into the API object.
app.include_router(AuthenticationRoter)
app.include_router(ZooBookingRouter)
app.include_router(AccomodationBookingRouter)
app.include_router(FileRouter)
app.include_router(AccountRouter)

# Run the app using connection information provided in the config.env file.
if __name__ == "__main__": uvicorn.run("__init__:app", host=app.config.host, port=int(app.config.port))