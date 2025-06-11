from app.api.endpoints import cd_consultas_auxiliares
from app.api.endpoints import pr_debug_log_projeto
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import json
from pathlib import Path
import os
import threading
import webbrowser
import requests
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.cd_usuario_sistema import UsuarioSistema
from app.models.cd_pessoa_fisica import PessoaFisica
from datetime import datetime, timedelta
from starlette.responses import RedirectResponse

# ================================ 📦 Importações de módulos ================================
from app.api.endpoints.au_autenticacao import router as autenticacao_router
from app.api.endpoints.ca_endpoint import router as conformidade_ambiental_router
from app.api.endpoints.cd_aprovar_usuario import router as aprovar_usuario_router
from app.api.endpoints.cd_cadastro_pessoa_fisica import router as cadastro_pf_router
from app.api.endpoints.cd_cadastro_pessoa_juridica import router as cadastro_pj_router
from app.api.endpoints.cd_cadastro_trechos_estadualizacao import router as cadastro_trechos_router
from app.api.endpoints.cd_cadastro_usuario_sistema import router as cadastro_usuario_router
from app.api.endpoints.cd_cadastro_elementos_rodoviarios import router as cadastro_elementos_rodoviarios_router
# Novos endpoints separados para elementos rodoviários
from app.api.endpoints.cd_cadastro_trecho_rodoviario import router as cadastro_trecho_rodoviario_router
from app.api.endpoints.cd_cadastro_rodovia import router as cadastro_rodovia_router
from app.api.endpoints.cd_cadastro_dispositivo import router as cadastro_dispositivo_router
from app.api.endpoints.cd_cadastro_obra_arte import router as cadastro_obra_arte_router
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
from app.api.endpoints.pr_fluxo_modular import router as fluxo_modular_router
from app.api.endpoints.pr_modulos_pages import router as modulos_pages_router
from app.api.endpoints.au_recuperacao_senha import router as recuperacao_senha_router

# ============================ 🚀 Instância principal da API ============================
app = FastAPI(
    title="FAD - Ferramenta de Análise Dinamizada",
    description="Plataforma para análise técnica e ambiental de dados geoespaciais",
    version="1.0.0"
)

# ============================= 🔐 Middleware de Sessão =============================
app.add_middleware(SessionMiddleware, secret_key="CHAVE_SECRETA_SUPER_FAD_2025")

# ============================= ⏳ Middleware de Timeout de Sessão =============================
# Definição da classe SessionTimeoutMiddleware
class SessionTimeoutMiddleware(BaseHTTPMiddleware):
    TIMEOUT_MINUTES = 15
    def __init__(self, app):
        super().__init__(app)
    async def dispatch(self, request, call_next):
        # Só tenta acessar a sessão se ela existir no escopo
        if 'session' in request.scope:
            session = request.session
            now = datetime.utcnow().timestamp()
            last_active = session.get('last_active')
            if last_active:
                elapsed = now - last_active
                if elapsed > self.TIMEOUT_MINUTES * 60:
                    session.clear()
                    response = RedirectResponse(url="/login")
                    response.delete_cookie('session')
                    return response
            session['last_active'] = now
        response = await call_next(request)
        return response

# Adiciona o middleware de timeout de sessão após a definição da classe
app.add_middleware(SessionTimeoutMiddleware)

# ============================ 🌐 Middleware de CORS ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ============================ 📝 Middleware de Logging ============================
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        method = request.method
        url = str(request.url)
        headers = dict(request.headers)
        try:
            body = await request.body()
            body_str = body.decode('utf-8') if body else ''
        except Exception:
            body_str = '<não foi possível ler o corpo>'
        print(f"\n[REQUISIÇÃO] {method} {url}")
        print(f"Headers: {headers}")
        if body_str:
            print(f"Payload: {body_str}")
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        print(f"[RESPOSTA] Status: {response.status_code} | Tempo: {process_time:.2f}ms")
        try:
            response_body = b''
            async for chunk in response.body_iterator:
                response_body += chunk
            async def new_body_iterator():
                yield response_body
            response.body_iterator = new_body_iterator()
            print(f"Resposta: {response_body.decode('utf-8')}")
        except Exception:
            print("Resposta: <não foi possível ler o corpo>")
        print("-"*60)
        return response

app.add_middleware(LoggingMiddleware)

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

# ✅ Rota para o mapa de rotas
@app.get("/mapa-rotas", response_class=HTMLResponse)
def mapa_rotas(request: Request):
    return templates.TemplateResponse("mapa_rotas_fad_atualizado.html", {"request": request})

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
app.include_router(cadastro_usuario_router, prefix="/api/cd")
app.include_router(cadastro_elementos_rodoviarios_router)
# Novos endpoints separados para elementos rodoviários
app.include_router(cadastro_trecho_rodoviario_router, prefix="/api/cd")
app.include_router(cadastro_rodovia_router, prefix="/api/cd")
app.include_router(cadastro_dispositivo_router, prefix="/api/cd")
app.include_router(cadastro_obra_arte_router, prefix="/api/cd")
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
app.include_router(fluxo_modular_router)
app.include_router(modulos_pages_router)
app.include_router(recuperacao_senha_router)

# ======================== 🌐 Rotas HTML diretas ========================
@app.get("/cadastro-usuario", response_class=HTMLResponse)
def tela_cadastro(request: Request):
    return templates.TemplateResponse("cd_cadastro_usuario.html", {"request": request})

@app.get("/cadastro-projeto", response_class=HTMLResponse)
def tela_projeto(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    timeout = 15 * 60  # 15 minutos em segundos
    now = datetime.utcnow().timestamp()
    last_active = request.session.get('last_active', now)
    tempo_restante = int(timeout - (now - last_active))
    if tempo_restante < 0:
        tempo_restante = 0
    return templates.TemplateResponse("pr_cadastro_projeto.html", {
        "request": request,
        "usuario": usuario,
        "tempo_restante": tempo_restante
    })

@app.get("/importar", response_class=HTMLResponse)
def importar_geometria(request: Request):
    return templates.TemplateResponse("iv_interface.html", {"request": request})

@app.get("/painel-analista", response_class=HTMLResponse)
def painel_comum(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    timeout = 15 * 60  # 15 minutos em segundos
    now = datetime.utcnow().timestamp()
    last_active = request.session.get('last_active', now)
    tempo_restante = int(timeout - (now - last_active))
    if tempo_restante < 0:
        tempo_restante = 0
    return templates.TemplateResponse("pn_painel_usuario_comum.html", {
        "request": request,
        "usuario": usuario,
        "tempo_restante": tempo_restante
    })

@app.get("/painel-coordenador", response_class=HTMLResponse)
def painel_adm(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    timeout = 15 * 60  # 15 minutos em segundos
    now = datetime.utcnow().timestamp()
    last_active = request.session.get('last_active', now)
    tempo_restante = int(timeout - (now - last_active))
    if tempo_restante < 0:
        tempo_restante = 0
    return templates.TemplateResponse("pn_painel_usuario_adm.html", {
        "request": request,
        "usuario": usuario,
        "tempo_restante": tempo_restante
    })

@app.get("/painel-master", response_class=HTMLResponse)
def painel_master(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    # Tempo restante da sessão
    timeout = 15 * 60  # 15 minutos em segundos
    now = datetime.utcnow().timestamp()
    last_active = request.session.get('last_active', now)
    tempo_restante = int(timeout - (now - last_active))
    if tempo_restante < 0:
        tempo_restante = 0
    return templates.TemplateResponse("pn_painel_usuario_master.html", {
        "request": request,
        "usuario": usuario,
        "tempo_restante": tempo_restante,
        "now": datetime.now()
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

@app.get("/boas-vindas", response_class=HTMLResponse)
def boas_vindas(request: Request):
    """Página de boas-vindas da plataforma FAD."""
    return templates.TemplateResponse("boas_vindas.html", {"request": request})

@app.get("/meus-dados", response_class=HTMLResponse)
def meus_dados(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return HTMLResponse(status_code=401, content="Acesso não autorizado. Faça login.")
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        return HTMLResponse(status_code=401, content="Usuário não encontrado. Faça login novamente.")
    # Busca dados pessoais (PessoaFisica) vinculados ao usuário
    usuario_pf = db.query(PessoaFisica).filter(PessoaFisica.id == usuario.pessoa_fisica_id).first()
    timeout = 15 * 60  # 15 minutos em segundos
    now = datetime.utcnow().timestamp()
    last_active = request.session.get('last_active', now)
    tempo_restante = int(timeout - (now - last_active))
    if tempo_restante < 0:
        tempo_restante = 0
    return templates.TemplateResponse("meus_dados.html", {
        "request": request,
        "usuario": usuario,
        "usuario_pf": usuario_pf,
        "tempo_restante": tempo_restante
    })

@app.get("/novo-projeto", response_class=HTMLResponse)
def novo_projeto(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    timeout = 15 * 60  # 15 minutos em segundos
    now = datetime.utcnow().timestamp()
    last_active = request.session.get('last_active', now)
    tempo_restante = int(timeout - (now - last_active))
    if tempo_restante < 0:
        tempo_restante = 0
    return templates.TemplateResponse("pr_cadastro_projeto.html", {
        "request": request,
        "usuario": usuario,
        "tempo_restante": tempo_restante
    })

@app.get("/visualizar-cadastro-ficticio", response_class=HTMLResponse)
def visualizar_cadastro_ficticio(request: Request):
    usuario = {
        'id': 123,
        'nome': 'Maria da Silva',
        'cpf': '123.456.789-00',
        'telefone': '(11) 91234-5678',
        'email': 'maria.silva@email.com',
        'pessoa_fisica_id': 456,
        'instituicao': 'Departamento de Estradas de Rodagem do Estado de São Paulo',
        'lotacao': 'Setor de Engenharia',
        'email_institucional': 'maria.silva@der.sp.gov.br',
        'telefone_institucional': '(11) 3344-5566',
        'ramal': '1234',
        'sede_hierarquia': 'Diretoria Técnica',
        'sede_coordenadoria': 'Coordenação de Projetos',
        'sede_setor': 'Setor de Obras',
        'sede_assistencia': 'Assistência Técnica',
        'regional_nome': 'Regional Campinas',
        'regional_coordenadoria': 'Coord. Regional Campinas',
        'regional_setor': 'Setor Regional',
        'tipo': 'Administrador',
        'status': 'Ativo',
        'ativo': True,
        'criado_em': datetime(2025, 6, 7, 10, 30)
    }
    pessoa_fisica = {
        'rua': 'Rua das Flores',
        'numero': '123',
        'bairro': 'Jardim Primavera',
        'cep': '13000-000',
        'cidade': 'Campinas',
        'uf': 'SP'
    }
    return templates.TemplateResponse(
        "formularios_cadastro_usuarios/cadastro_usuario_template.html",
        {
            "request": request,
            "usuario": usuario,
            "pessoa_fisica": pessoa_fisica,
            "data_geracao": datetime.now()
        }
    )

@app.get("/cadastro-interessado-rodovia", response_class=HTMLResponse)
def cadastro_rodovia(request: Request):
    return templates.TemplateResponse("cd_interessado_rodovia.html", {"request": request})

@app.get("/cadastro-interessado-trecho", response_class=HTMLResponse)
def cadastro_trecho(request: Request):
    return templates.TemplateResponse("cd_interessado_trecho.html", {"request": request})

@app.get("/cadastro-interessado-dispositivo", response_class=HTMLResponse)
def cadastro_dispositivo(request: Request):
    return templates.TemplateResponse("cd_interessado_dispositivo.html", {"request": request})

@app.get("/cadastro-interessado-obra-arte", response_class=HTMLResponse)
def cadastro_obra_arte(request: Request):
    return templates.TemplateResponse("cd_interessado_obra_arte.html", {"request": request})

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import requests

@app.get("/proxy/receitaws/cnpj/{cnpj}", response_class=JSONResponse)
def proxy_receitaws_cnpj(cnpj: str):
    """Proxy para buscar dados de CNPJ na ReceitaWS sem CORS."""
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    try:
        resp = requests.get(url, timeout=10)
        return JSONResponse(status_code=resp.status_code, content=resp.json())
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})
