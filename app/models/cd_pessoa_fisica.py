from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base

class PessoaFisica(Base):
    __tablename__ = "pessoa_fisica"
    __table_args__ = {"schema": "Cadastro"}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=True)

    usuarios = relationship(
        "UsuarioSistema",
        back_populates="pessoa_fisica",
        primaryjoin="PessoaFisica.id == UsuarioSistema.pessoa_fisica_id"
    )
