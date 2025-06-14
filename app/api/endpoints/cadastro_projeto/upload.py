# Endpoint de upload e recebimento do ZIP/shapefile do projeto
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/api/projeto/upload-geometria")
def upload_geometria(projeto_id: int = Form(...), arquivo_zip: UploadFile = File(...)):
    # Aqui você processa o arquivo, salva temporariamente e retorna status
    # (Lógica real no backend principal)
    return JSONResponse({
        "status": "recebido",
        "upload_id": 123  # ID fictício para exemplo
    })
