# Endpoint para renderizar o mapa de rotas visual (HTML)
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../../templates'))

router = APIRouter()

@router.get("/mapa-rotas-fad", response_class=HTMLResponse)
def renderizar_mapa_rotas(request: Request):
    return templates.TemplateResponse("mapa_rotas_fad_atualizado.html", {"request": request})
