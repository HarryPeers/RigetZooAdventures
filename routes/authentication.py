from fastapi import *
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from modules.models.account import account as accountModel

router = APIRouter()


@router.get("/api/login")
async def login(request: Request, email:str, password:str):
    """
    Take the password and email address associated with the account and generate an access token once validated.
    """
    
    # Initalize and retrieve account information
    account = accountModel(request.app, email=email)

    # Generate the appropriate token for the account
    token = account.generateToken(password, overwrite=True)

    # Handle the response
    if not token.valid: raise HTTPException(401, "You could not be authenticated")
    else: return token.json()

@router.post("/api/register")
async def register(request: Request):
    """
    Register an account into the database and return an access token.
    """

    # Parse the request body into json
    json = await request.json()
    
    # Assign attributes
    email = json["email"]
    password = json["password"]
    security_question = json["security-question"]
    security_answer = json["security-answer"]
    
    # Generate the account model object.
    account = accountModel(request.app, email=email)
    
    # Check if account already exists
    if account.id != None: raise HTTPException(403, "Account already exists!")

    # Create the account
    account.createAccount(email, password, security_question, security_answer)

    # Return a generated token.
    return account.generateToken(password, overwrite=True).json()

@router.get("/api/authenticate-token")
async def authenticate(request: Request, token:str):
    """
    Validate the authenticity of an authentication token
    """

    # Initalize and retrieve account information
    account = accountModel(request.app)

    # Validate the account by the provided token.
    account.validateAccountByToken(token)

    # Return response.
    raise HTTPException(200, "Succesfully authenticated")

@router.get("/api/security-question")
async def authenticate(request: Request, email:str):
    """
    Return the security question of an account
    """

    # Initalize and retrieve account information
    account = accountModel(request.app, email=email)

    # Return the security question if the account exists.
    if account.id == None: raise HTTPException(404, "Account could not be found.")
    else: return {"question": account.securityQuestion}


@router.post("/api/security-question")
async def authenticate(request: Request):
    """
    Validate a security question and return an elevated access token
    """

    # Parse the request body to json
    json = await request.json()
    
    # Assign the needed variables.
    email = json["account-email"]
    answer = json["security-answer"]

    # Initalize and retrieve account information
    account = accountModel(request.app, email=email)

    # challenge the security question and retrieve an elevated access token.
    token = account.generateElevatedToken(answer, True)

    # Return response
    if token.valid: return token.json()
    else: raise HTTPException(401, "You were not authenticated")


@router.put("/api/forgotten-password")
async def authenticate(request: Request):
    """
    Change the accounts password through the forgotten password feature
    """

    # Parse the request body to json
    json = await request.json()

    # Assign the needed variables.
    password = json["new-password"]
    token = json["token"]

    # Initalize and retrieve account information
    account = accountModel(request.app)

    # Change the password using the elevated access token
    completed = account.changePassword(token, password)

    # Return response
    if completed: return account.generateToken(password).json()
    else: raise HTTPException(401, "You were not authenticated")