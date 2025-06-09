from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.models.pr_projeto import Projeto
from app.models.pr_modulo_configuracao import ModuloConfiguracao
from app.services.fluxo_modular_service import FluxoModularService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/modulo", tags=["Páginas de Módulos"])

# Configuração dos templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/{projeto_id}/{modulo_numero}", response_class=HTMLResponse)
async def pagina_modulo(
    request: Request,
    projeto_id: int,
    modulo_numero: int,
    db: Session = Depends(get_db)
):
    """
    Renderiza a página do módulo específico baseado no projeto e número do módulo.
    Verifica permissões e redireciona para o template apropriado.
    """
    try:
        # Validação básica
        if modulo_numero < 1 or modulo_numero > 5:
            raise HTTPException(status_code=400, detail="Número do módulo deve estar entre 1 e 5")
        
        # Busca informações do projeto
        projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()
        if not projeto:
            raise HTTPException(status_code=404, detail="Projeto não encontrado")
        
        # Busca configuração do módulo
        modulo_config = db.query(ModuloConfiguracao).filter(
            ModuloConfiguracao.numero == modulo_numero,
            ModuloConfiguracao.ativo == True
        ).first()
        
        if not modulo_config:
            raise HTTPException(status_code=404, detail="Módulo não encontrado")
        
        # Verifica permissões usando o serviço de fluxo
        service = FluxoModularService(db)
        status_projeto = service.get_status_projeto(projeto_id)
        
        # Encontra status do módulo específico
        modulo_status = next(
            (m for m in status_projeto['modulos'] if m['numero'] == modulo_numero),
            None
        )
        
        if not modulo_status:
            raise HTTPException(status_code=404, detail="Status do módulo não encontrado")
        
        # Verifica se pode acessar o módulo
        if not modulo_status['pode_executar'] and modulo_status['status'] not in ['concluido', 'validado']:
            raise HTTPException(
                status_code=403, 
                detail=f"Acesso negado. Módulo {modulo_numero} não pode ser executado. Complete os módulos anteriores primeiro."
            )
        
        # Determina o template baseado no módulo
        template_map = {
            1: "pr_cadastro_projeto.html",
            2: "pr_conformidade_ambiental.html", 
            3: "pr_favorabilidade_multicriterio.html",
            4: "pr_favorabilidade_socioeconomica.html",
            5: "pr_favorabilidade_infraestrutural.html"
        }
        
        template_name = template_map.get(modulo_numero)
        if not template_name:
            raise HTTPException(status_code=404, detail="Template do módulo não encontrado")
        
        # Contexto para o template
        context = {
            "request": request,
            "projeto": projeto,
            "modulo": {
                "numero": modulo_numero,
                "nome": modulo_config.nome,
                "descricao": modulo_config.descricao,
                "status": modulo_status['status'],
                "pode_executar": modulo_status['pode_executar']
            },
            "status_projeto": status_projeto
        }
        
        return templates.TemplateResponse(template_name, context)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao carregar página do módulo {modulo_numero} do projeto {projeto_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/{projeto_id}", response_class=HTMLResponse)
async def dashboard_projeto(
    request: Request,
    projeto_id: int,
    db: Session = Depends(get_db)
):
    """
    Dashboard do projeto mostrando todos os módulos e seu status.
    Página inicial quando se acessa um projeto.
    """
    try:
        # Busca informações do projeto
        projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()
        if not projeto:
            raise HTTPException(status_code=404, detail="Projeto não encontrado")
        
        # Busca status completo do projeto
        service = FluxoModularService(db)
        status_projeto = service.get_status_projeto(projeto_id)
        
        # Inicializa fluxo se necessário (projeto novo)
        if not status_projeto['modulos']:
            service.inicializar_fluxo_projeto(projeto_id)
            status_projeto = service.get_status_projeto(projeto_id)
        
        context = {
            "request": request,
            "projeto": projeto,
            "status_projeto": status_projeto,
            "modulos_configuracao": db.query(ModuloConfiguracao).order_by(ModuloConfiguracao.ordem_execucao).all()
        }
        
        return templates.TemplateResponse("pr_dashboard_projeto.html", context)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao carregar dashboard do projeto {projeto_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/{projeto_id}/navegacao", response_class=HTMLResponse) 
async def apenas_navegacao(
    request: Request,
    projeto_id: int,
    db: Session = Depends(get_db)
):
    """
    Renderiza apenas o componente de navegação modular.
    Útil para inclusão via AJAX em outras páginas.
    """
    try:
        projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()
        if not projeto:
            raise HTTPException(status_code=404, detail="Projeto não encontrado")
        
        service = FluxoModularService(db)
        status_projeto = service.get_status_projeto(projeto_id)
        
        context = {
            "request": request,
            "projeto": projeto,
            "status_projeto": status_projeto
        }
        
        return templates.TemplateResponse("componentes/navegacao_modular.html", context)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao carregar navegação do projeto {projeto_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
