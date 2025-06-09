from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class ModuloConfiguracao(Base):
    __tablename__ = "modulo_configuracao"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False, unique=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    
    # Controle de sequência
    modulo_anterior = Column(Integer, ForeignKey("modulo_configuracao.numero"))
    obrigatorio = Column(Boolean, default=True)
    
    # Configurações de template
    template_html = Column(String(255))
    endpoint_base = Column(String(100))
    
    # Metadados
    ativo = Column(Boolean, default=True)
    ordem_execucao = Column(Integer)
    
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relacionamentos
    modulo_pai = relationship("ModuloConfiguracao", remote_side=[numero])

    def __repr__(self):
        return f"<ModuloConfiguracao(numero={self.numero}, nome='{self.nome}')>"

    @property
    def is_primeiro_modulo(self):
        """Verifica se é o primeiro módulo da sequência"""
        return self.modulo_anterior is None

    @property
    def endpoint_completo(self):
        """Retorna o endpoint completo do módulo"""
        return f"{self.endpoint_base}/{self.numero}"

    @classmethod
    def get_modulo_por_numero(cls, session, numero):
        """Busca um módulo específico pelo número"""
        return session.query(cls).filter(cls.numero == numero, cls.ativo == True).first()

    @classmethod
    def get_sequencia_modulos(cls, session):
        """Retorna todos os módulos na ordem de execução"""
        return session.query(cls).filter(cls.ativo == True).order_by(cls.ordem_execucao).all()
