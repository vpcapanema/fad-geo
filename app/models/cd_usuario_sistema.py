from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class UsuarioSistema(Base):
    __tablename__ = "usuario_sistema"
    __table_args__ = (
        UniqueConstraint('cpf', 'tipo', name='uix_cpf_tipo'),
        CheckConstraint(
            "tipo IN ('comum', 'administrador', 'master')",
            name="check_tipo_usuario_valido"
        ),
        {"schema": "Cadastro"}  # ← precisa ser o último item
    )

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False)  # unique removido para permitir a restrição composta
    email = Column(String, nullable=False)
    telefone = Column(String)
    senha_hash = Column(String, nullable=False)
    tipo = Column(String, nullable=False, default="comum")

    pessoa_fisica_id = Column(Integer, ForeignKey("Cadastro.pessoa_fisica.id"), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    aprovado_em = Column(DateTime, nullable=True)
    aprovador_id = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"), nullable=True)
    status = Column(String, default="aguardando aprovacao")
    ativo = Column(Boolean, default=True)

    pessoa_fisica = relationship(
        "PessoaFisica",
        back_populates="usuarios",
        primaryjoin="UsuarioSistema.pessoa_fisica_id == PessoaFisica.id"
    )

    aprovador = relationship(
        "UsuarioSistema",
        remote_side=[id],
        primaryjoin="UsuarioSistema.aprovador_id == UsuarioSistema.id"
    )

