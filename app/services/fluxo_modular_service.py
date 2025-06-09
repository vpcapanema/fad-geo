from sqlalchemy.orm import Session
from app.models.pr_projeto import Projeto
from app.models.pr_relatorio_modulo import RelatorioModulo
from app.models.pr_modulo_configuracao import ModuloConfiguracao
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FluxoModularService:
    """Serviço para gerenciar o fluxo sequencial dos módulos da FAD-GEO"""
    
    def __init__(self, db: Session):
        self.db = db

    def inicializar_fluxo_projeto(self, projeto_id: int) -> Dict[str, Any]:
        """
        Inicializa o fluxo modular para um projeto recém-criado.
        Cria registros para todos os 5 módulos com status e permissões apropriadas.
        """
        try:
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if not projeto:
                raise ValueError(f"Projeto {projeto_id} não encontrado")

            # Busca configuração dos módulos
            modulos = self.db.query(ModuloConfiguracao).order_by(ModuloConfiguracao.ordem_execucao).all()
            
            relatorios_criados = []
            
            for modulo in modulos:
                # Verifica se já existe relatório para este módulo
                relatorio_existente = self.db.query(RelatorioModulo).filter(
                    RelatorioModulo.projeto_id == projeto_id,
                    RelatorioModulo.modulo_numero == modulo.numero
                ).first()
                
                if not relatorio_existente:
                    # Primeiro módulo sempre pode ser executado
                    pode_executar = modulo.is_primeiro_modulo
                    
                    relatorio = RelatorioModulo(
                        projeto_id=projeto_id,
                        modulo_numero=modulo.numero,
                        modulo_nome=modulo.nome,
                        status='pendente',
                        pode_executar=pode_executar,
                        dependencias_ok=pode_executar,
                        criado_em=datetime.now()
                    )
                    
                    self.db.add(relatorio)
                    relatorios_criados.append({
                        'modulo': modulo.numero,
                        'nome': modulo.nome,
                        'pode_executar': pode_executar
                    })

            # Atualiza status do projeto
            projeto.status_fluxo = 'iniciado'
            projeto.modulo_atual = 1
            
            self.db.commit()
            
            logger.info(f"Fluxo modular inicializado para projeto {projeto_id}")
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'relatorios_criados': relatorios_criados,
                'modulo_atual': 1,
                'status_fluxo': 'iniciado'
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao inicializar fluxo do projeto {projeto_id}: {str(e)}")
            raise

    def atualizar_permissoes_modulos(self, projeto_id: int) -> Dict[str, Any]:
        """
        Atualiza as permissões de execução dos módulos baseado no status atual.
        Chama a função PostgreSQL para garantir consistência.
        """
        try:
            # Executa função PostgreSQL para atualizar permissões
            self.db.execute("SELECT atualizar_permissoes_modulos(:projeto_id)", {"projeto_id": projeto_id})
            self.db.commit()
            
            # Busca status atualizado
            relatorios = self.db.query(RelatorioModulo).filter(
                RelatorioModulo.projeto_id == projeto_id
            ).order_by(RelatorioModulo.modulo_numero).all()
            
            status_modulos = []
            for rel in relatorios:
                status_modulos.append({
                    'modulo': rel.modulo_numero,
                    'nome': rel.modulo_nome,
                    'status': rel.status,
                    'pode_executar': rel.pode_executar,
                    'dependencias_ok': rel.dependencias_ok
                })
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'modulos': status_modulos
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao atualizar permissões do projeto {projeto_id}: {str(e)}")
            raise

    def iniciar_execucao_modulo(self, projeto_id: int, modulo_numero: int, usuario_id: int) -> Dict[str, Any]:
        """
        Inicia a execução de um módulo específico.
        Verifica permissões e atualiza status.
        """
        try:
            relatorio = self.db.query(RelatorioModulo).filter(
                RelatorioModulo.projeto_id == projeto_id,
                RelatorioModulo.modulo_numero == modulo_numero
            ).first()
            
            if not relatorio:
                raise ValueError(f"Módulo {modulo_numero} não encontrado para projeto {projeto_id}")
            
            if not relatorio.pode_executar:
                raise ValueError(f"Módulo {modulo_numero} não pode ser executado. Dependências não atendidas.")
            
            if relatorio.status in ['em_execucao', 'concluido', 'validado']:
                raise ValueError(f"Módulo {modulo_numero} já foi iniciado ou concluído")
            
            # Atualiza status para execução
            relatorio.status = 'em_execucao'
            relatorio.criado_por = usuario_id
            relatorio.atualizado_em = datetime.now()
            
            # Atualiza módulo atual do projeto
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if projeto and projeto.modulo_atual < modulo_numero:
                projeto.modulo_atual = modulo_numero
            
            self.db.commit()
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'modulo_numero': modulo_numero,
                'status': 'em_execucao',
                'iniciado_por': usuario_id
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao iniciar módulo {modulo_numero} do projeto {projeto_id}: {str(e)}")
            raise

    def concluir_modulo(self, projeto_id: int, modulo_numero: int, html_conteudo: str, 
                       html_arquivo: str = None, dados_extras: Dict = None) -> Dict[str, Any]:
        """
        Conclui um módulo salvando o relatório HTML gerado.
        """
        try:
            relatorio = self.db.query(RelatorioModulo).filter(
                RelatorioModulo.projeto_id == projeto_id,
                RelatorioModulo.modulo_numero == modulo_numero
            ).first()
            
            if not relatorio:
                raise ValueError(f"Módulo {modulo_numero} não encontrado para projeto {projeto_id}")
            
            if relatorio.status != 'em_execucao':
                raise ValueError(f"Módulo {modulo_numero} não está em execução")
            
            # Salva dados do relatório
            relatorio.status = 'concluido'
            relatorio.html_conteudo = html_conteudo
            relatorio.html_arquivo = html_arquivo
            relatorio.dados_extras = dados_extras
            relatorio.atualizado_em = datetime.now()
            
            self.db.commit()
            
            # Atualiza permissões dos próximos módulos
            self.atualizar_permissoes_modulos(projeto_id)
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'modulo_numero': modulo_numero,
                'status': 'concluido',
                'aguardando_validacao': True
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao concluir módulo {modulo_numero} do projeto {projeto_id}: {str(e)}")
            raise

    def validar_modulo(self, projeto_id: int, modulo_numero: int, validador_id: int, 
                      aprovado: bool, observacoes: str = None) -> Dict[str, Any]:
        """
        Valida ou rejeita um módulo concluído (ação do coordenador).
        """
        try:
            relatorio = self.db.query(RelatorioModulo).filter(
                RelatorioModulo.projeto_id == projeto_id,
                RelatorioModulo.modulo_numero == modulo_numero
            ).first()
            
            if not relatorio:
                raise ValueError(f"Módulo {modulo_numero} não encontrado para projeto {projeto_id}")
            
            if relatorio.status != 'concluido':
                raise ValueError(f"Módulo {modulo_numero} não está pronto para validação")
            
            # Atualiza status baseado na validação
            relatorio.status = 'validado' if aprovado else 'rejeitado'
            relatorio.validado_em = datetime.now()
            relatorio.validado_por = validador_id
            relatorio.observacoes_validacao = observacoes
            relatorio.atualizado_em = datetime.now()
            
            # Se rejeitado, permite nova execução
            if not aprovado:
                relatorio.pode_executar = True
                relatorio.status = 'pendente'  # Volta para pendente para nova execução
            
            self.db.commit()
            
            # Se validado, atualiza permissões dos próximos módulos
            if aprovado:
                self.atualizar_permissoes_modulos(projeto_id)
                
                # Verifica se todos os módulos foram validados
                self._verificar_conclusao_projeto(projeto_id)
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'modulo_numero': modulo_numero,
                'validacao': 'aprovado' if aprovado else 'rejeitado',
                'validado_por': validador_id,
                'observacoes': observacoes
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao validar módulo {modulo_numero} do projeto {projeto_id}: {str(e)}")
            raise

    def _verificar_conclusao_projeto(self, projeto_id: int):
        """
        Verifica se todos os módulos foram validados e atualiza status do projeto.
        """
        relatorios_validados = self.db.query(RelatorioModulo).filter(
            RelatorioModulo.projeto_id == projeto_id,
            RelatorioModulo.status == 'validado'
        ).count()
        
        if relatorios_validados == 5:  # Todos os 5 módulos validados
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if projeto:
                projeto.todos_modulos_concluidos = True
                projeto.status_fluxo = 'concluido'
                projeto.pronto_para_pdf = True
                self.db.commit()

    def get_status_projeto(self, projeto_id: int) -> Dict[str, Any]:
        """
        Retorna o status completo do fluxo modular de um projeto.
        """
        projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
        if not projeto:
            raise ValueError(f"Projeto {projeto_id} não encontrado")
        
        relatorios = self.db.query(RelatorioModulo).filter(
            RelatorioModulo.projeto_id == projeto_id
        ).order_by(RelatorioModulo.modulo_numero).all()
        
        modulos_status = []
        for rel in relatorios:
            modulos_status.append({
                'numero': rel.modulo_numero,
                'nome': rel.modulo_nome,
                'status': rel.status,
                'status_display': rel.status_display,
                'pode_executar': rel.pode_executar,
                'dependencias_ok': rel.dependencias_ok,
                'criado_em': rel.criado_em.isoformat() if rel.criado_em else None,
                'atualizado_em': rel.atualizado_em.isoformat() if rel.atualizado_em else None,
                'validado_em': rel.validado_em.isoformat() if rel.validado_em else None,
                'tem_relatorio': bool(rel.html_conteudo),
                'observacoes_validacao': rel.observacoes_validacao
            })
        
        return {
            'projeto_id': projeto_id,
            'nome_projeto': projeto.nome,
            'modulo_atual': projeto.modulo_atual,
            'modulo_atual_nome': projeto.modulo_atual_nome,
            'status_fluxo': projeto.status_fluxo,
            'progresso_percentual': projeto.progresso_percentual,
            'todos_modulos_concluidos': projeto.todos_modulos_concluidos,
            'pronto_para_pdf': projeto.pronto_para_pdf,
            'modulos': modulos_status
        }
