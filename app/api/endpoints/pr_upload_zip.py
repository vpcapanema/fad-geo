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
    extensoes_permitidas = [".zip", ".rar", ".7z"]
    max_mb = 50
    erros = []

    # 1. Extensão
    if not any(arquivo.filename.lower().endswith(ext) for ext in extensoes_permitidas):
        erros.append("Extensão não permitida. Envie um arquivo .zip, .rar ou .7z.")
    # 2. Tamanho e vazio
    conteudo = await arquivo.read()
    if len(conteudo) == 0:
        erros.append("Arquivo está vazio.")
    if len(conteudo) > max_mb * 1024 * 1024:
        erros.append("Arquivo maior que 50MB.")

    if erros:
        # Aqui você pode gerar o relatório PDF de erro (mock)
        return JSONResponse(status_code=400, content={
            "sucesso": False,
            "mensagem": "Erro no upload.",
            "erros": erros,
            "relatorio": "/static/relatorios/relatorio_erro_upload.pdf"
        })

    # Salvar arquivo e registrar no banco
    nome_base = re.sub(r"[^a-zA-Z0-9_-]", "_", arquivo.filename.replace(".zip", ""))
    temp_dir = Path("temp") / nome_base
    temp_dir.mkdir(parents=True, exist_ok=True)
    zip_path = temp_dir / arquivo.filename
    with open(zip_path, "wb") as f:
        f.write(conteudo)

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

    return JSONResponse(status_code=200, content={
        "sucesso": True,
        "mensagem": "Upload salvo com sucesso. Deseja validar a geometria?",
        "id_upload": novo.id
    })
