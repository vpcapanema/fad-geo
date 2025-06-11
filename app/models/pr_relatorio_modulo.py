from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, CheckConstraint, UniqueConstraint, Interval
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database.base import Base
from datetime import datetime

class RelatorioModulo(Base):
    __tablename__ = "relatorio_modulo"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    projeto_id = Column(Integer, ForeignKey("public.projeto.id", ondelete="CASCADE"), nullable=False)
    modulo_numero = Column(Integer, nullable=False)
    modulo_nome = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="pendente")
    
    # Metadados do relatório
    criado_em = Column(DateTime, default=datetime.now)
    criado_por = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"))
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Dados do relatório HTML
    html_conteudo = Column(Text)
    html_arquivo = Column(String(255))
    
    # Validação pelo coordenador
    validado_em = Column(DateTime)
    validado_por = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"))
    observacoes_validacao = Column(Text)
    
    # PDF gerado para processo judicial
    pdf_arquivo = Column(String(255))
    pdf_gerado_em = Column(DateTime)
    
    # Controle de sequência
    pode_executar = Column(Boolean, default=False)
    dependencias_ok = Column(Boolean, default=False)
    
    # Metadados adicionais
    dados_extras = Column(JSONB)
    duracao_execucao = Column(Interval)
    tamanho_dados = Column(Integer)

    # Constraints
    __table_args__ = (
        CheckConstraint('modulo_numero BETWEEN 1 AND 5', name='check_modulo_numero'),
        UniqueConstraint('projeto_id', 'modulo_numero', name='uq_projeto_modulo'),
        {"schema": "public"}
    )

    # Relacionamentos
    projeto = relationship("Projeto", back_populates="relatorios_modulos")
    criador = relationship("UsuarioSistema", foreign_keys=[criado_por])
    validador = relationship("UsuarioSistema", foreign_keys=[validado_por])

    def __repr__(self):
        return f"<RelatorioModulo(projeto_id={self.projeto_id}, modulo={self.modulo_numero}, status='{self.status}')>"

    @property
    def status_display(self):
        status_map = {
            'pendente': 'Pendente',
            'em_execucao': 'Em Execução',
            'concluido': 'Concluído',
            'validado': 'Validado',
            'rejeitado': 'Rejeitado'
        }
        return status_map.get(self.status, self.status.title())

    @property
    def pode_validar(self):
        """Verifica se o relatório pode ser validado pelo coordenador"""
        return self.status == 'concluido' and self.html_conteudo is not None

    @property
    def proximo_modulo_numero(self):
        """Retorna o número do próximo módulo na sequência"""
        return self.modulo_numero + 1 if self.modulo_numero < 5 else None
