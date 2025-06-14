from sqlalchemy.orm import Session
from app.models.pr_projeto import Projeto
from app.models.pr_relatorio_modulo import RelatorioModulo
from app.models.cd_usuario_sistema import UsuarioSistema
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class StatusProjetoService:
    """Serviço para gerenciar os status dos projetos e suas transições"""
    
    # Status válidos do sistema
    STATUS_VALIDOS = [
        "Em cadastramento",
        "Finalizado", 
        "Enviado",
        "Em análise",
        "Reprovado",
        "Aprovado",
        "Arquivado"
    ]
    
    def __init__(self, db: Session):
        self.db = db

    def alterar_status_projeto(self, projeto_id: int, novo_status: str, 
                              usuario_id: int, observacoes: str = None) -> Dict[str, Any]:
        """
        Altera o status do projeto com validações e logs apropriados
        """
        try:
            if novo_status not in self.STATUS_VALIDOS:
                raise ValueError(f"Status inválido: {novo_status}")
                
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if not projeto:
                raise ValueError(f"Projeto {projeto_id} não encontrado")
                
            usuario = self.db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
            if not usuario:
                raise ValueError(f"Usuário {usuario_id} não encontrado")

            # Validações específicas por status
            self._validar_transicao_status(projeto, novo_status, usuario)
            
            status_anterior = projeto.status
            projeto.status = novo_status
            
            # Atualiza campos específicos baseado no novo status
            self._atualizar_campos_status(projeto, novo_status, usuario_id, observacoes)
            
            self.db.commit()
            
            logger.info(f"Status do projeto {projeto_id} alterado de '{status_anterior}' para '{novo_status}' por usuário {usuario_id}")
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'status_anterior': status_anterior,
                'status_novo': novo_status,
                'alterado_por': usuario.nome_completo,
                'alterado_em': datetime.now()
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao alterar status do projeto {projeto_id}: {str(e)}")
            raise

    def finalizar_projeto(self, projeto_id: int, usuario_id: int) -> Dict[str, Any]:
        """
        Finaliza um projeto após validar que todos os módulos estão completos
        """
        try:
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if not projeto:
                raise ValueError(f"Projeto {projeto_id} não encontrado")
                
            if projeto.status != "Em cadastramento":
                raise ValueError(f"Projeto deve estar 'Em cadastramento' para ser finalizado")
                
            # Verifica se todos os 5 módulos estão validados
            modulos_validados = self.db.query(RelatorioModulo).filter(
                RelatorioModulo.projeto_id == projeto_id,
                RelatorioModulo.status == 'validado'
            ).count()
            
            if modulos_validados < 5:
                raise ValueError(f"Todos os 5 módulos devem estar validados. Atual: {modulos_validados}/5")
            
            projeto.status = "Finalizado"
            projeto.todos_modulos_concluidos = True
            projeto.pronto_para_pdf = True
            
            self.db.commit()
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'status': 'Finalizado',
                'modulos_validados': modulos_validados,
                'pronto_para_envio': True
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao finalizar projeto {projeto_id}: {str(e)}")
            raise

    def enviar_para_analise(self, projeto_id: int, usuario_id: int) -> Dict[str, Any]:
        """
        Envia projeto finalizado para análise da coordenação
        """
        try:
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if not projeto:
                raise ValueError(f"Projeto {projeto_id} não encontrado")
                
            if projeto.status != "Finalizado":
                raise ValueError(f"Projeto deve estar 'Finalizado' para ser enviado")
                
            if projeto.usuario_id != usuario_id:
                raise ValueError(f"Apenas o criador do projeto pode enviá-lo para análise")
                
            projeto.status = "Enviado"
            projeto.enviado_para_analise_em = datetime.now()
            
            self.db.commit()
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'status': 'Enviado',
                'enviado_em': projeto.enviado_para_analise_em
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao enviar projeto {projeto_id} para análise: {str(e)}")
            raise

    def iniciar_analise(self, projeto_id: int, coordenador_id: int) -> Dict[str, Any]:
        """
        Inicia a análise de um projeto enviado por um coordenador
        """
        try:
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if not projeto:
                raise ValueError(f"Projeto {projeto_id} não encontrado")
                
            coordenador = self.db.query(UsuarioSistema).filter(UsuarioSistema.id == coordenador_id).first()
            if not coordenador or coordenador.tipo_usuario != 'coordenador':
                raise ValueError(f"Usuário deve ser coordenador para analisar projetos")
                
            if projeto.status != "Enviado":
                raise ValueError(f"Projeto deve estar 'Enviado' para iniciar análise")
                
            projeto.status = "Em análise"
            projeto.coordenador_id = coordenador_id
            projeto.analise_iniciada_em = datetime.now()
            
            self.db.commit()
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'status': 'Em análise',
                'coordenador': coordenador.nome_completo,
                'analise_iniciada_em': projeto.analise_iniciada_em
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao iniciar análise do projeto {projeto_id}: {str(e)}")
            raise

    def aprovar_projeto(self, projeto_id: int, coordenador_id: int, observacoes: str = None) -> Dict[str, Any]:
        """
        Aprova um projeto em análise
        """
        return self._finalizar_analise(projeto_id, coordenador_id, "Aprovado", observacoes)

    def reprovar_projeto(self, projeto_id: int, coordenador_id: int, motivo: str) -> Dict[str, Any]:
        """
        Reprova um projeto em análise
        """
        if not motivo:
            raise ValueError("Motivo da reprovação é obrigatório")
        return self._finalizar_analise(projeto_id, coordenador_id, "Reprovado", motivo)

    def reverter_projeto(self, projeto_id: int, coordenador_id: int) -> Dict[str, Any]:
        """
        Reverte um projeto enviado de volta para Em cadastramento
        """
        try:
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if not projeto:
                raise ValueError(f"Projeto {projeto_id} não encontrado")
                
            coordenador = self.db.query(UsuarioSistema).filter(UsuarioSistema.id == coordenador_id).first()
            if not coordenador or coordenador.tipo_usuario != 'coordenador':
                raise ValueError(f"Usuário deve ser coordenador para reverter projetos")
                
            if projeto.status != "Enviado":
                raise ValueError(f"Projeto deve estar 'Enviado' para ser revertido")
                
            projeto.status = "Em cadastramento"
            projeto.enviado_para_analise_em = None
            
            self.db.commit()
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'status': 'Em cadastramento',
                'revertido_por': coordenador.nome_completo
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao reverter projeto {projeto_id}: {str(e)}")
            raise

    def arquivar_projeto(self, projeto_id: int, usuario_id: int, motivo: str) -> Dict[str, Any]:
        """
        Arquiva um projeto (apenas masters)
        """
        try:
            usuario = self.db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
            if not usuario or usuario.tipo_usuario != 'master':
                raise ValueError(f"Apenas usuários master podem arquivar projetos")
                
            return self.alterar_status_projeto(projeto_id, "Arquivado", usuario_id, motivo)
            
        except Exception as e:
            logger.error(f"Erro ao arquivar projeto {projeto_id}: {str(e)}")
            raise

    def _validar_transicao_status(self, projeto: Projeto, novo_status: str, usuario: UsuarioSistema):
        """Valida se a transição de status é permitida"""
        
        # Validações por tipo de usuário
        if usuario.tipo_usuario == 'analista':
            if novo_status not in ["Em cadastramento", "Finalizado", "Enviado"]:
                raise ValueError(f"Analista não pode alterar status para '{novo_status}'")
                
        elif usuario.tipo_usuario == 'coordenador':
            if novo_status not in ["Em cadastramento", "Em análise", "Aprovado", "Reprovado"]:
                raise ValueError(f"Coordenador não pode alterar status para '{novo_status}'")
                
        elif usuario.tipo_usuario != 'master':
            raise ValueError(f"Usuário sem permissão para alterar status")

    def _atualizar_campos_status(self, projeto: Projeto, novo_status: str, usuario_id: int, observacoes: str):
        """Atualiza campos específicos baseado no novo status"""
        
        if novo_status == "Enviado":
            projeto.enviado_para_analise_em = datetime.now()
            
        elif novo_status == "Em análise":
            projeto.coordenador_id = usuario_id
            projeto.analise_iniciada_em = datetime.now()
            
        elif novo_status in ["Aprovado", "Reprovado"]:
            projeto.analise_finalizada_em = datetime.now()
            projeto.aprovador_id = usuario_id
            if observacoes:
                if novo_status == "Reprovado":
                    projeto.motivo_reprovacao = observacoes
                else:
                    projeto.observacao = observacoes

    def _finalizar_analise(self, projeto_id: int, coordenador_id: int, status_final: str, observacoes: str) -> Dict[str, Any]:
        """Método auxiliar para aprovar ou reprovar projeto"""
        try:
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if not projeto:
                raise ValueError(f"Projeto {projeto_id} não encontrado")
                
            coordenador = self.db.query(UsuarioSistema).filter(UsuarioSistema.id == coordenador_id).first()
            if not coordenador or coordenador.tipo_usuario != 'coordenador':
                raise ValueError(f"Usuário deve ser coordenador para finalizar análise")
                
            if projeto.status != "Em análise":
                raise ValueError(f"Projeto deve estar 'Em análise' para ser {status_final.lower()}")
                
            if projeto.coordenador_id != coordenador_id:
                raise ValueError(f"Apenas o coordenador responsável pode finalizar a análise")
                
            projeto.status = status_final
            projeto.analise_finalizada_em = datetime.now()
            projeto.aprovador_id = coordenador_id
            
            if status_final == "Reprovado":
                projeto.motivo_reprovacao = observacoes
            else:
                projeto.observacao = observacoes
                projeto.aprovado_em = datetime.now()
            
            self.db.commit()
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'status': status_final,
                'coordenador': coordenador.nome_completo,
                'finalizado_em': projeto.analise_finalizada_em
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao {status_final.lower()} projeto {projeto_id}: {str(e)}")
            raise

    def get_projetos_por_status(self, status: str, usuario_id: int = None) -> list:
        """Retorna lista de projetos filtrados por status"""
        try:
            query = self.db.query(Projeto).filter(Projeto.status == status)
            
            if usuario_id:
                query = query.filter(Projeto.usuario_id == usuario_id)
                
            return query.all()
            
        except Exception as e:
            logger.error(f"Erro ao buscar projetos por status {status}: {str(e)}")
            raise

    def get_status_permitidos_usuario(self, tipo_usuario: str) -> list:
        """Retorna lista de status que o usuário pode visualizar/gerenciar"""
        if tipo_usuario == 'master':
            return self.STATUS_VALIDOS
        elif tipo_usuario == 'coordenador':
            return ["Enviado", "Em análise", "Reprovado", "Aprovado"]
        elif tipo_usuario == 'analista':
            return ["Em cadastramento", "Finalizado", "Enviado", "Reprovado"]
        else:
            return ["Em cadastramento", "Finalizado"]
