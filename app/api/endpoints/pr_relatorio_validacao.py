# app/api/endpoints/relatorio_validacao.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/shape/relatorio-validacao',
    tags=['Relatório de Validação']
)
from pathlib import Path

router = APIRouter()

@router.get("/pdf/{arquivo}")
async def baixar_relatorio_validacao(arquivo: str):
    # Proteção contra path traversal
    if ".." in arquivo or "/" in arquivo or "\\" in arquivo:
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido.")

    # Caminho completo e seguro
    base_path = Path(__file__).resolve().parent.parent.parent / "static" / "relatorios"
    caminho_arquivo = base_path / arquivo

    if not caminho_arquivo.exists():
        raise HTTPException(status_code=404, detail="Relatório não encontrado.")

    return FileResponse(caminho_arquivo, media_type="application/pdf", filename=arquivo)
