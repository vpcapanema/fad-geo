from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.modulos_projeto_service import ModulosProjetoService
from app.services.status_projeto_service import StatusProjetoService
from pydantic import BaseModel
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/projetos/modulos", tags=["Módulos de Projetos"])

# Modelos Pydantic
class SalvarModuloRequest(BaseModel):
    projeto_id: int
    modulo_numero: int
    dados_formulario: Dict[str, Any]

class ValidarModuloRequest(BaseModel):
    projeto_id: int
    modulo_numero: int

@router.post("/inicializar")
async def inicializar_modulos(projeto_id: int, db: Session = Depends(get_db)):
    """
    Inicializa todos os 5 módulos para um projeto novo
    """
    try:
        service = ModulosProjetoService(db)
        resultado = service.inicializar_modulos_projeto(projeto_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Módulos inicializados com sucesso",
                "data": resultado
            }
        )
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao inicializar módulos: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.post("/salvar")
async def salvar_dados_modulo(dados: SalvarModuloRequest, db: Session = Depends(get_db)):
    """
    Salva os dados de um módulo específico
    """
    try:
        # TODO: Implementar autenticação e pegar usuario_id da sessão
        usuario_id = 1  # Temporário
        
        service = ModulosProjetoService(db)
        resultado = service.salvar_dados_modulo(
            dados.projeto_id,
            dados.modulo_numero,
            dados.dados_formulario,
            usuario_id
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Dados do módulo salvos com sucesso",
                "data": resultado
            }
        )
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao salvar dados do módulo: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.post("/validar")
async def validar_modulo(dados: ValidarModuloRequest, db: Session = Depends(get_db)):
    """
    Valida um módulo e libera o próximo para preenchimento
    """
    try:
        # TODO: Implementar autenticação e pegar usuario_id da sessão
        usuario_id = 1  # Temporário
        
        service = ModulosProjetoService(db)
        resultado = service.validar_modulo(
            dados.projeto_id,
            dados.modulo_numero,
            usuario_id
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Módulo validado com sucesso",
                "data": resultado
            }
        )
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao validar módulo: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.get("/status/{projeto_id}")
async def get_status_modulos(projeto_id: int, db: Session = Depends(get_db)):
    """
    Retorna o status completo de todos os módulos de um projeto
    """
    try:
        service = ModulosProjetoService(db)
        status = service.get_status_modulos_projeto(projeto_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Status dos módulos recuperado com sucesso",
                "data": status
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao buscar status dos módulos: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.get("/formulario/{projeto_id}/{modulo_numero}")
async def get_formulario_modulo(projeto_id: int, modulo_numero: int, db: Session = Depends(get_db)):
    """
    Retorna os dados do formulário de um módulo específico
    """
    try:
        from app.models.pr_relatorio_modulo import RelatorioModulo
        
        relatorio = db.query(RelatorioModulo).filter(
            RelatorioModulo.projeto_id == projeto_id,
            RelatorioModulo.modulo_numero == modulo_numero
        ).first()
        
        if not relatorio:
            return JSONResponse(
                status_code=404,
                content={"error": "Módulo não encontrado"}
            )
        
        dados_formulario = relatorio.dados_extras.get("dados_formulario", {}) if relatorio.dados_extras else {}
        
        return JSONResponse(
            status_code=200,
            content={
                "projeto_id": projeto_id,
                "modulo_numero": modulo_numero,
                "modulo_nome": relatorio.modulo_nome,
                "status": relatorio.status,
                "pode_editar": relatorio.pode_executar and relatorio.status in ['pendente', 'em_preenchimento'],
                "dados_formulario": dados_formulario
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao buscar formulário do módulo: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.get("/html/{projeto_id}/{modulo_numero}", response_class=HTMLResponse)
async def gerar_html_modulo(projeto_id: int, modulo_numero: int, db: Session = Depends(get_db)):
    """
    Gera e retorna HTML completo do módulo para visualização/PDF
    """
    try:
        service = ModulosProjetoService(db)
        html_content = service.gerar_html_modulo(projeto_id, modulo_numero)
        
        return HTMLResponse(content=html_content, status_code=200)
        
    except ValueError as e:
        return HTMLResponse(
            content=f"<html><body><h1>Erro</h1><p>{str(e)}</p></body></html>",
            status_code=404
        )
    except Exception as e:
        logger.error(f"Erro ao gerar HTML do módulo: {str(e)}")
        return HTMLResponse(
            content=f"<html><body><h1>Erro interno</h1><p>Não foi possível gerar o HTML</p></body></html>",
            status_code=500
        )

# Endpoints específicos para cada módulo (podem ser expandidos)

@router.get("/cadastro/{projeto_id}")
async def get_modulo_cadastro(projeto_id: int, db: Session = Depends(get_db)):
    """Endpoint específico para módulo de cadastro"""
    return await get_formulario_modulo(projeto_id, 1, db)

@router.get("/ambiental/{projeto_id}")
async def get_modulo_ambiental(projeto_id: int, db: Session = Depends(get_db)):
    """Endpoint específico para módulo de conformidade ambiental"""
    return await get_formulario_modulo(projeto_id, 2, db)

@router.get("/multicriterio/{projeto_id}")
async def get_modulo_multicriterio(projeto_id: int, db: Session = Depends(get_db)):
    """Endpoint específico para módulo de favorabilidade multicritério"""
    return await get_formulario_modulo(projeto_id, 3, db)

@router.get("/socioeconomico/{projeto_id}")
async def get_modulo_socioeconomico(projeto_id: int, db: Session = Depends(get_db)):
    """Endpoint específico para módulo de favorabilidade socioeconômica"""
    return await get_formulario_modulo(projeto_id, 4, db)

@router.get("/infraestrutura/{projeto_id}")
async def get_modulo_infraestrutura(projeto_id: int, db: Session = Depends(get_db)):
    """Endpoint específico para módulo de favorabilidade infraestrutural"""
    return await get_formulario_modulo(projeto_id, 5, db)

# Endpoint para autocompletar projeto quando todos os módulos estão validados
@router.post("/autocompletar/{projeto_id}")
async def autocompletar_projeto(projeto_id: int, db: Session = Depends(get_db)):
    """
    Verifica se todos os módulos estão validados e automatically finaliza o projeto
    """
    try:
        # TODO: Implementar autenticação
        usuario_id = 1  # Temporário
        
        modulos_service = ModulosProjetoService(db)
        status_service = StatusProjetoService(db)
        
        # Verifica status dos módulos
        status_modulos = modulos_service.get_status_modulos_projeto(projeto_id)
        
        if status_modulos['todos_concluidos']:
            # Todos os módulos estão validados, pode finalizar o projeto
            resultado = status_service.finalizar_projeto(projeto_id, usuario_id)
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Projeto finalizado automaticamente - todos os módulos validados",
                    "data": resultado
                }
            )
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "error": f"Nem todos os módulos estão validados. Progresso: {status_modulos['modulos_validados']}/5"
                }
            )
        
    except Exception as e:
        logger.error(f"Erro ao autocompletar projeto: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )
