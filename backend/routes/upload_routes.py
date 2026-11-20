from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.constants.index import DATASET_DIR
import shutil
from pathlib import Path
from uuid import uuid4
from services.pdfChat_services import extract_data, reload_faiss



router = APIRouter()

@router.post("/upload")   
async def chat_pdf(file: UploadFile = File(...)):
    if file is None:
        print("file not found")
        return {"message": "file not found", "status": False}
    
    contents = await file.read(5)
    
    # Kiểm tra định dạng file
    if Path(file.filename).suffix.lower() != ".pdf" or contents != b"%PDF-":
        raise HTTPException(
            status_code = 400,
            detail = "Only PDF files are allowed"
        )
        
    # Đưa con trỏ về đầu
    await file.seek(0)
    
    # Lưu file
    try:
        with open(f'{DATASET_DIR}/{uuid4()}.pdf',"wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = f"Could not save file: {str(e)}"
        )
    finally:
        await file.close()
        
    extract_data()
    reload_faiss()
    
    return {
        "message": "File uploaded successfully",
        "data": {
            "filename": file.filename,
        },
        "status": True
    }