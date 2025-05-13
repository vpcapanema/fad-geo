from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base

class PessoaJuridica(Base):
    __tablename__ = "pessoa_juridica"
    __table_args__ = {"schema": "Cadastro"}

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String, nullable=False)
    cnpj = Column(String, nullable=False, unique=True)
    nome_fantasia = Column(String, nullable=True)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    rua = Column(String, nullable=True)
    numero = Column(String, nullable=True)
    complemento = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    uf = Column(String, nullable=True)

    projetos = relationship(
        "Projeto",
        back_populates="pessoa_juridica",
        primaryjoin="PessoaJuridica.id == Projeto.pessoa_juridica_id"
    )
