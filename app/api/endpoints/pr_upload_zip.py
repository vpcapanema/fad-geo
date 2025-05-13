# app/api/endpoints/pr_upload_zip.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pathlib import Path
import zipfile, os, re, shutil
from app.database.session import get_db
# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/shape/upload',
    tags=['Upload de Shape']
)
from app.models.pr_zip_uploads import ZipUpload
from datetime import datetime

router = APIRouter()

@router.post("/")
async def upload_zip(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not arquivo.filename.lower().endswith(".zip"):
        return JSONResponse(status_code=400, content={"sucesso": False, "erros": ["Arquivo deve ser .zip."]})

    nome_base = re.sub(r"[^a-zA-Z0-9_-]", "_", arquivo.filename.replace(".zip", ""))
    temp_dir = Path("temp") / nome_base
    temp_dir.mkdir(parents=True, exist_ok=True)

    zip_path = temp_dir / arquivo.filename
    with open(zip_path, "wb") as f:
        f.write(await arquivo.read())

    # Registro do upload (padrão: usuário 1, projeto 1 - alterar para pegar da sessão)
    novo = ZipUpload(
        arquivo=arquivo.filename,
        tipo_arquivo=arquivo.content_type,
        status="recebido",
        usuario_id=1,
        projeto_id=1,
        data_upload=datetime.utcnow()
    )

    db.add(novo)
    db.commit()

    return {"sucesso": True, "mensagem": "Upload salvo com sucesso."}
