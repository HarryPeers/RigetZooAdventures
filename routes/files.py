from fastapi import *
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.exceptions import HTTPException

import os

router = APIRouter()

async def FileResponseHandler(path):
    if os.path.exists(path): return FileResponse(path)
    else: raise HTTPException(404, "File not found")

@router.get("/scripts/components/{file:str}")
async def fileUnderGroup(request:Request, file:str): 
    path = f"./www/scripts/components/{file}"
    if not os.path.exists(path): raise HTTPException(404, "File not found")

    with open(path, "r") as file: content = file.read()
    for p in request.query_params.keys(): content = f"{p} = {request.query_params[p]}\n" + content

    return HTMLResponse(content, 200)

@router.get("/")
async def index(): return await FileResponseHandler(f"./www/pages/index.html")

@router.get("/{file:str}")
async def file(file:str): return await FileResponseHandler(f"./www/pages/{file}.html")

@router.get("/{group:str}/{file:str}")
async def fileUnderGroup(group:str, file:str): return await FileResponseHandler(f"./www/{group}/{file}")

@router.get("/{group:str}/{subgroup:str}/{file:str}")
async def fileUnderGroup(group:str, subgroup:str, file:str): return await FileResponseHandler(f"./www/{group}/{subgroup}/{file}")
