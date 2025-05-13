from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base

class TrechoEstadualizacao(Base):
    __tablename__ = "trechos_estadualizacao"
    __table_args__ = {"schema": "Elementos_rodoviarios"}

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False, unique=True)
    denominacao = Column(String, nullable=False)
    municipio = Column(String, nullable=False)

    projetos = relationship(
        "Projeto",
        back_populates="trecho",
        primaryjoin="TrechoEstadualizacao.id == Projeto.trecho_id"
    )
