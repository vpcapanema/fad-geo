from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime, timedelta
import uuid

class RecuperacaoSenha(Base):
    __tablename__ = "au_recuperacao_senha"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    
    # Controle de tempo
    criado_em = Column(DateTime, default=datetime.utcnow)
    expira_em = Column(DateTime, nullable=False)
    usado = Column(Boolean, default=False)
    usado_em = Column(DateTime, nullable=True)
    
    # Dados de segurança
    ip_solicitacao = Column(String(45))
    user_agent = Column(Text)

    # Relacionamento
    usuario = relationship("UsuarioSistema", back_populates="recuperacoes_senha")    def __init__(self, usuario_id, ip_solicitacao=None, user_agent=None):
        self.usuario_id = usuario_id
        self.token = str(uuid.uuid4())
        self.criado_em = datetime.utcnow()
        self.expira_em = datetime.utcnow() + timedelta(minutes=15)  # 15 minutos
        self.ip_solicitacao = ip_solicitacao
        self.user_agent = user_agent

    @property
    def is_expired(self):
        """Verifica se o token expirou"""
        return datetime.utcnow() > self.expira_em

    @property
    def is_used(self):
        """Verifica se o token já foi usado"""
        return self.usado_em is not None

    @property
    def is_valid(self):
        """Verifica se o token é válido (não expirou e não foi usado)"""
        return self.ativo and not self.is_expired and not self.is_used

    def marcar_como_usado(self):
        """Marca o token como usado"""
        self.usado_em = datetime.utcnow()
        self.ativo = False

    def __repr__(self):
        return f"<RecuperacaoSenha(id={self.id}, usuario_id={self.usuario_id}, token='{self.token[:8]}...', expirado={self.is_expired})>"
