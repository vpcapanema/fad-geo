from app.api.endpoints import cd_consultas_auxiliares
from app.api.endpoints import pr_debug_log_projeto
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
import os

# ================================ 📦 Importações de módulos ================================
from app.api.endpoints.au_autenticacao import router as autenticacao_router
from app.api.endpoints.ca_endpoint import router as conformidade_ambiental_router
from app.api.endpoints.cd_aprovar_usuario import router as aprovar_usuario_router
from app.api.endpoints.cd_cadastro_pessoa_fisica import router as cadastro_pf_router
from app.api.endpoints.cd_cadastro_pessoa_juridica import router as cadastro_pj_router
from app.api.endpoints.cd_cadastro_trechos_estadualizacao import router as cadastro_trechos_router
from app.api.endpoints.cd_cadastro_usuario_sistema import router as cadastro_usuario_router
from app.api.endpoints.pn_menu_navegacao import router as menu_navegacao_router
from app.api.endpoints.pn_painel_usuario_administrador import router as painel_administrador_router
from app.api.endpoints.pn_painel_usuario_comum import router as painel_usuario_comum_router
from app.api.endpoints.pn_painel_usuario_master import router as painel_master_router
from app.api.endpoints.pr_gravar_projeto import router as cadastrar_projeto_router
from app.api.endpoints.pr_relatorio_upload import router as relatorio_upload_router
from app.api.endpoints.pr_relatorio_validacao import router as relatorio_validacao_router
from app.api.endpoints.pr_salvar_geometria_validada import router as salvar_geometria_router
from app.api.endpoints.pr_salvar_projeto import router as salvar_projeto_router
from app.api.endpoints.pr_status_projeto import router as status_projeto_router
from app.api.endpoints.pr_upload_zip import router as upload_router
from app.api.endpoints.pr_validacao_geometria import router as validacao_geometria_router
from app.api.endpoints.vw_painel_administrador import router as vw_painel_administrador_router
from app.api.endpoints.vw_projetos_usuario_comum import router as vw_projetos_usuario_comum_router

# ============================ 🚀 Instância principal da API ============================
app = FastAPI(
    title="FAD - Ferramenta de Análise Dinamizada",
    description="Plataforma para análise técnica e ambiental de dados geoespaciais",
    version="1.0.0"
)

# ============================= 🔐 Middleware de Sessão =============================
app.add_middleware(SessionMiddleware, secret_key="CHAVE_SECRETA_SUPER_FAD_2025")

# ============================ 🌐 Middleware de CORS ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ======================== 📁 Diretórios do Projeto ========================
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)

os.makedirs(STATIC_DIR / "images", exist_ok=True)
os.makedirs(STATIC_DIR / "relatorios", exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# =================== 🏠 Página Inicial ===================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "static_url": "/static/images"
    })

# ✅ Nova rota limpa para exibir o login
@app.get("/login", response_class=HTMLResponse)
def tela_login(request: Request):
    return templates.TemplateResponse("au_login.html", {"request": request})

# =============== 🐞 Rota Debug ===============
@app.get("/debug", response_class=JSONResponse)
async def debug_info(request: Request):
    return {
        "status": "online",
        "base_url": str(request.base_url),
        "static_files_path": str(STATIC_DIR),
        "available_images": os.listdir(STATIC_DIR / "images") if os.path.exists(STATIC_DIR / "images") else []
    }

# =============== 🖼️ Favicon ===============
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    path = STATIC_DIR / "images/favicon.ico"
    if path.exists():
        return FileResponse(path)
    return JSONResponse(status_code=404, content={"detail": "Favicon não encontrado."})

# ==================== 🔌 Inclusão de Rotas API ====================
app.include_router(autenticacao_router)
app.include_router(conformidade_ambiental_router)
app.include_router(aprovar_usuario_router)
app.include_router(cadastro_pf_router)
app.include_router(cadastro_pj_router)
app.include_router(cadastro_trechos_router)
app.include_router(cadastro_usuario_router)
app.include_router(menu_navegacao_router)
app.include_router(painel_administrador_router)
app.include_router(painel_usuario_comum_router)
app.include_router(painel_master_router)
app.include_router(cadastrar_projeto_router)
app.include_router(relatorio_upload_router)
app.include_router(relatorio_validacao_router)
app.include_router(salvar_geometria_router)
app.include_router(salvar_projeto_router)
app.include_router(status_projeto_router)
app.include_router(upload_router)
app.include_router(validacao_geometria_router)
app.include_router(vw_painel_administrador_router)
app.include_router(vw_projetos_usuario_comum_router)

# ======================== 🌐 Rotas HTML diretas ========================
@app.get("/cadastro-usuario", response_class=HTMLResponse)
def tela_cadastro(request: Request):
    return templates.TemplateResponse("cd_cadastro_usuario.html", {"request": request})

@app.get("/cadastro-projeto", response_class=HTMLResponse)
def tela_projeto(request: Request):
    return templates.TemplateResponse("pr_cadastro_projeto.html", {"request": request})

@app.get("/importar", response_class=HTMLResponse)
def importar_geometria(request: Request):
    return templates.TemplateResponse("iv_interface.html", {"request": request})

@app.get("/painel-analista", response_class=HTMLResponse)
def painel_comum(request: Request):
    usuario = request.session.get("usuario")
    return templates.TemplateResponse("pn_painel_usuario_comum.html", {
        "request": request,
        "usuario": usuario
    })

@app.get("/painel-coordenador", response_class=HTMLResponse)
def painel_adm(request: Request):
    usuario = request.session.get("usuario")
    return templates.TemplateResponse("pn_painel_usuario_adm.html", {
        "request": request,
        "usuario": usuario
    })

@app.get("/painel-master", response_class=HTMLResponse)
def painel_master(request: Request):
    usuario = request.session.get("usuario")
    return templates.TemplateResponse("pn_painel_usuario_master.html", {
        "request": request,
        "usuario": usuario
    })

# ======================== 🌐 Rota de visualização do Cabeçalho FAD ========================
@app.get("/cabecalho-fad", response_class=HTMLResponse)
def visualizar_cabecalho_fad():
    caminho = STATIC_DIR / "template_cabecalho_fad.html"
    if not caminho.exists():
        raise HTTPException(status_code=404, detail="Template do cabeçalho não encontrado.")
    return FileResponse(caminho, media_type="text/html")


from app.api.endpoints.vw_painel_analista_projetos import router as painel_analista_projetos_router
from app.api.endpoints.vw_painel_coordenador_projetos import router as painel_coordenador_projetos_router
from app.api.endpoints.vw_painel_master_projetos import router as painel_master_projetos_router
from app.api.endpoints.vw_usuarios_painel import router as usuarios_painel_router
app.include_router(painel_analista_projetos_router)
app.include_router(painel_coordenador_projetos_router)
app.include_router(painel_master_projetos_router)
app.include_router(usuarios_painel_router)
