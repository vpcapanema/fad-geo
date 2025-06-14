from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.status_projeto_service import StatusProjetoService
from app.models.cd_usuario_sistema import UsuarioSistema
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/projetos/status", tags=["Status de Projetos"])

# Modelos Pydantic para requests
class AlterarStatusRequest(BaseModel):
    projeto_id: int
    novo_status: str
    observacoes: Optional[str] = None

class AnaliseRequest(BaseModel):
    projeto_id: int
    observacoes: Optional[str] = None

class ReprovacaoRequest(BaseModel):
    projeto_id: int
    motivo: str

@router.post("/finalizar")
async def finalizar_projeto(request: Request, projeto_id: int, db: Session = Depends(get_db)):
    """
    Finaliza um projeto após validar que todos os módulos estão completos
    Só pode ser usado por analistas que criaram o projeto
    """
    try:
        # TODO: Implementar autenticação e pegar usuario_id da sessão
        usuario_id = 1  # Temporário - deve vir da sessão
        
        service = StatusProjetoService(db)
        resultado = service.finalizar_projeto(projeto_id, usuario_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Projeto finalizado com sucesso",
                "data": resultado
            }
        )
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao finalizar projeto: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.post("/enviar")
async def enviar_para_analise(request: Request, projeto_id: int, db: Session = Depends(get_db)):
    """
    Envia projeto finalizado para análise da coordenação
    Só pode ser usado pelo analista que criou o projeto
    """
    try:
        # TODO: Implementar autenticação e pegar usuario_id da sessão
        usuario_id = 1  # Temporário - deve vir da sessão
        
        service = StatusProjetoService(db)
        resultado = service.enviar_para_analise(projeto_id, usuario_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Projeto enviado para análise com sucesso",
                "data": resultado
            }
        )
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao enviar projeto para análise: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.post("/reverter")
async def reverter_projeto(request: Request, projeto_id: int, db: Session = Depends(get_db)):
    """
    Reverte um projeto enviado de volta para Em cadastramento
    Só pode ser usado por coordenadores
    """
    try:
        # TODO: Implementar autenticação e pegar coordenador_id da sessão
        coordenador_id = 2  # Temporário - deve vir da sessão
        
        service = StatusProjetoService(db)
        resultado = service.reverter_projeto(projeto_id, coordenador_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Projeto revertido com sucesso",
                "data": resultado
            }
        )
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao reverter projeto: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.post("/iniciar-analise")
async def iniciar_analise(request: Request, projeto_id: int, db: Session = Depends(get_db)):
    """
    Inicia a análise de um projeto enviado
    Só pode ser usado por coordenadores
    """
    try:
        # TODO: Implementar autenticação e pegar coordenador_id da sessão
        coordenador_id = 2  # Temporário - deve vir da sessão
        
        service = StatusProjetoService(db)
        resultado = service.iniciar_analise(projeto_id, coordenador_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Análise iniciada com sucesso",
                "data": resultado
            }
        )
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao iniciar análise: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.post("/aprovar")
async def aprovar_projeto(dados: AnaliseRequest, db: Session = Depends(get_db)):
    """
    Aprova um projeto em análise
    Só pode ser usado pelo coordenador responsável
    """
    try:
        # TODO: Implementar autenticação e pegar coordenador_id da sessão
        coordenador_id = 2  # Temporário - deve vir da sessão
        
        service = StatusProjetoService(db)
        resultado = service.aprovar_projeto(dados.projeto_id, coordenador_id, dados.observacoes)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Projeto aprovado com sucesso",
                "data": resultado
            }
        )
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao aprovar projeto: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.post("/reprovar")
async def reprovar_projeto(dados: ReprovacaoRequest, db: Session = Depends(get_db)):
    """
    Reprova um projeto em análise
    Só pode ser usado pelo coordenador responsável
    """
    try:
        # TODO: Implementar autenticação e pegar coordenador_id da sessão
        coordenador_id = 2  # Temporário - deve vir da sessão
        
        service = StatusProjetoService(db)
        resultado = service.reprovar_projeto(dados.projeto_id, coordenador_id, dados.motivo)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Projeto reprovado",
                "data": resultado
            }
        )
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao reprovar projeto: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.post("/arquivar")
async def arquivar_projeto(request: Request, projeto_id: int, motivo: str, db: Session = Depends(get_db)):
    """
    Arquiva um projeto (apenas masters)
    """
    try:
        # TODO: Implementar autenticação e pegar usuario_id da sessão
        usuario_id = 3  # Temporário - deve vir da sessão (master)
        
        service = StatusProjetoService(db)
        resultado = service.arquivar_projeto(projeto_id, usuario_id, motivo)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Projeto arquivado com sucesso",
                "data": resultado
            }
        )
        
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Erro ao arquivar projeto: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.get("/listar/{status}")
async def listar_projetos_por_status(status: str, db: Session = Depends(get_db)):
    """
    Lista projetos filtrados por status
    """
    try:
        # TODO: Implementar autenticação e pegar usuario_id da sessão
        usuario_id = None  # Para coordenadores/masters ver todos
        
        service = StatusProjetoService(db)
        projetos = service.get_projetos_por_status(status, usuario_id)
        
        projetos_data = []
        for projeto in projetos:
            projetos_data.append({
                "id": projeto.id,
                "nome": projeto.nome,
                "status": projeto.status,
                "criado_em": projeto.enviado_em,
                "usuario_id": projeto.usuario_id,
                "coordenador_id": projeto.coordenador_id,
                "progresso": projeto.progresso_percentual
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "status": status,
                "total": len(projetos_data),
                "projetos": projetos_data
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao listar projetos por status: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )

@router.get("/status-permitidos/{tipo_usuario}")
async def get_status_permitidos(tipo_usuario: str, db: Session = Depends(get_db)):
    """
    Retorna lista de status que o usuário pode visualizar/gerenciar
    """
    try:
        service = StatusProjetoService(db)
        status_permitidos = service.get_status_permitidos_usuario(tipo_usuario)
        
        return JSONResponse(
            status_code=200,
            content={
                "tipo_usuario": tipo_usuario,
                "status_permitidos": status_permitidos
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao buscar status permitidos: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Erro interno do servidor"}
        )
