from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.fluxo_modular_service import FluxoModularService
from app.models.pr_projeto import Projeto
from app.models.pr_relatorio_modulo import RelatorioModulo
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pr/fluxo", tags=["Fluxo Modular"])

@router.post("/inicializar/{projeto_id}")
async def inicializar_fluxo_projeto(
    projeto_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Inicializa o fluxo modular para um projeto.
    Cria registros para todos os 5 módulos da FAD-GEO.
    """
    try:
        service = FluxoModularService(db)
        resultado = service.inicializar_fluxo_projeto(projeto_id)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao inicializar fluxo: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/status/{projeto_id}")
async def get_status_projeto(
    projeto_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retorna o status completo do fluxo modular de um projeto.
    """
    try:
        service = FluxoModularService(db)
        status = service.get_status_projeto(projeto_id)
        return status
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao buscar status: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.post("/modulo/{projeto_id}/{modulo_numero}/iniciar")
async def iniciar_modulo(
    projeto_id: int,
    modulo_numero: int,
    usuario_id: int = Query(..., description="ID do usuário que está iniciando o módulo"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Inicia a execução de um módulo específico.
    """
    try:
        if modulo_numero < 1 or modulo_numero > 5:
            raise HTTPException(status_code=400, detail="Número do módulo deve estar entre 1 e 5")
        
        service = FluxoModularService(db)
        resultado = service.iniciar_execucao_modulo(projeto_id, modulo_numero, usuario_id)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao iniciar módulo: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.post("/modulo/{projeto_id}/{modulo_numero}/concluir")
async def concluir_modulo(
    projeto_id: int,
    modulo_numero: int,
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Conclui um módulo salvando o relatório HTML gerado.
    
    Payload esperado:
    {
        "html_conteudo": "string - Conteúdo HTML do relatório",
        "html_arquivo": "string - Caminho para arquivo HTML (opcional)",
        "dados_extras": {} - Dados específicos do módulo (opcional)
    }
    """
    try:
        if modulo_numero < 1 or modulo_numero > 5:
            raise HTTPException(status_code=400, detail="Número do módulo deve estar entre 1 e 5")
        
        html_conteudo = payload.get('html_conteudo')
        if not html_conteudo:
            raise HTTPException(status_code=400, detail="Conteúdo HTML é obrigatório")
        
        service = FluxoModularService(db)
        resultado = service.concluir_modulo(
            projeto_id=projeto_id,
            modulo_numero=modulo_numero,
            html_conteudo=html_conteudo,
            html_arquivo=payload.get('html_arquivo'),
            dados_extras=payload.get('dados_extras')
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao concluir módulo: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.post("/modulo/{projeto_id}/{modulo_numero}/validar")
async def validar_modulo(
    projeto_id: int,
    modulo_numero: int,
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Valida ou rejeita um módulo concluído (ação do coordenador).
    
    Payload esperado:
    {
        "validador_id": int - ID do usuário coordenador,
        "aprovado": bool - True para aprovar, False para rejeitar,
        "observacoes": "string - Observações da validação (opcional)"
    }
    """
    try:
        if modulo_numero < 1 or modulo_numero > 5:
            raise HTTPException(status_code=400, detail="Número do módulo deve estar entre 1 e 5")
        
        validador_id = payload.get('validador_id')
        aprovado = payload.get('aprovado')
        
        if validador_id is None:
            raise HTTPException(status_code=400, detail="ID do validador é obrigatório")
        if aprovado is None:
            raise HTTPException(status_code=400, detail="Campo 'aprovado' é obrigatório")
        
        service = FluxoModularService(db)
        resultado = service.validar_modulo(
            projeto_id=projeto_id,
            modulo_numero=modulo_numero,
            validador_id=validador_id,
            aprovado=aprovado,
            observacoes=payload.get('observacoes')
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao validar módulo: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.post("/atualizar-permissoes/{projeto_id}")
async def atualizar_permissoes(
    projeto_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Atualiza as permissões de execução dos módulos baseado no status atual.
    """
    try:
        service = FluxoModularService(db)
        resultado = service.atualizar_permissoes_modulos(projeto_id)
        return resultado
    except Exception as e:
        logger.error(f"Erro ao atualizar permissões: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/modulo/{projeto_id}/{modulo_numero}/relatorio")
async def get_relatorio_modulo(
    projeto_id: int,
    modulo_numero: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retorna o relatório HTML de um módulo específico.
    """
    try:
        if modulo_numero < 1 or modulo_numero > 5:
            raise HTTPException(status_code=400, detail="Número do módulo deve estar entre 1 e 5")
        
        relatorio = db.query(RelatorioModulo).filter(
            RelatorioModulo.projeto_id == projeto_id,
            RelatorioModulo.modulo_numero == modulo_numero
        ).first()
        
        if not relatorio:
            raise HTTPException(status_code=404, detail="Relatório não encontrado")
        
        return {
            'projeto_id': projeto_id,
            'modulo_numero': modulo_numero,
            'modulo_nome': relatorio.modulo_nome,
            'status': relatorio.status,
            'html_conteudo': relatorio.html_conteudo,
            'html_arquivo': relatorio.html_arquivo,
            'criado_em': relatorio.criado_em.isoformat() if relatorio.criado_em else None,
            'atualizado_em': relatorio.atualizado_em.isoformat() if relatorio.atualizado_em else None,
            'validado_em': relatorio.validado_em.isoformat() if relatorio.validado_em else None,
            'observacoes_validacao': relatorio.observacoes_validacao,
            'dados_extras': relatorio.dados_extras
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar relatório: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/navegacao/{projeto_id}")
async def get_navegacao_modulos(
    projeto_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retorna informações de navegação entre os módulos para um projeto.
    Útil para gerar menus de navegação e controle de acesso.
    """
    try:
        service = FluxoModularService(db)
        status = service.get_status_projeto(projeto_id)
        
        # Monta informações de navegação
        navegacao = []
        for modulo in status['modulos']:
            navegacao.append({
                'numero': modulo['numero'],
                'nome': modulo['nome'],
                'status': modulo['status'],
                'pode_acessar': modulo['pode_executar'] or modulo['status'] in ['concluido', 'validado'],
                'url': f"/modulo/{projeto_id}/{modulo['numero']}",
                'icone_status': {
                    'pendente': 'fa-clock',
                    'em_execucao': 'fa-spinner fa-spin',
                    'concluido': 'fa-check-circle text-warning',
                    'validado': 'fa-check-circle text-success',
                    'rejeitado': 'fa-times-circle text-danger'
                }.get(modulo['status'], 'fa-question-circle')
            })
        
        return {
            'projeto_id': projeto_id,
            'modulo_atual': status['modulo_atual'],
            'progresso_percentual': status['progresso_percentual'],
            'todos_concluidos': status['todos_modulos_concluidos'],
            'navegacao': navegacao
        }
    except Exception as e:
        logger.error(f"Erro ao buscar navegação: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
