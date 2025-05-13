from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import os

app = FastAPI()

@app.get("/cabecalho-fad", response_class=HTMLResponse)
async def visualizar_cabecalho():
    caminho_html = os.path.join("app", "static", "template_cabecalho_fad.html")
    return FileResponse(caminho_html, media_type="text/html")
