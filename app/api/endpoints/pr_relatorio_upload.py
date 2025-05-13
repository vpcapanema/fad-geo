# app/api/endpoints/relatorio_upload.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/shape/relatorio-upload',
    tags=['Relatório de Upload']
)
from pathlib import Path

router = APIRouter()

@router.get("/relatorios/{nome_arquivo}")
async def baixar_relatorio_upload(nome_arquivo: str):
    # Segurança: evitar leitura de arquivos fora da pasta
    if ".." in nome_arquivo or "/" in nome_arquivo or "\\" in nome_arquivo:
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido.")

    # Caminho completo do arquivo
    base_path = Path(__file__).resolve().parent.parent.parent / "static" / "relatorios"
    caminho_arquivo = base_path / nome_arquivo

    if not caminho_arquivo.exists():
        raise HTTPException(status_code=404, detail="Relatório não encontrado.")

    return FileResponse(caminho_arquivo, media_type="application/pdf", filename=nome_arquivo)
