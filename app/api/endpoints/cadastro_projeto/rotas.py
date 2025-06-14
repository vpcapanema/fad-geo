# Mapa de rotas para o fluxo de cadastro de projeto
from fastapi import APIRouter
from .upload import router as upload_router
from .validacao import router as validacao_router
from .croqui import router as croqui_router
from .gravar import router as gravar_router

router = APIRouter()

# Inclui as rotas de cada etapa
router.include_router(upload_router)
router.include_router(validacao_router)
router.include_router(croqui_router)
router.include_router(gravar_router)
