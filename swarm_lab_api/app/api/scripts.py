from fastapi import APIRouter, HTTPException, UploadFile, File
from app.crud.scripts import upload_script

router = APIRouter()

@router.post("/scripts/upload/")
async def upload_new_script(file: UploadFile = File(...)):
    content = await file.read()
    return upload_script(content.decode())
