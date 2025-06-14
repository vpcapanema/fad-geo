# Endpoint de geração do croqui de localização
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/api/projeto/gerar-croqui")
def gerar_croqui(geometria_id: int):
    # Aqui você chama a lógica de geração do croqui
    # (Lógica real no backend principal)
    return JSONResponse({
        "status": "croqui_gerado",
        "caminho_croqui": "/media/croquis/croqui_789.png"
    })
