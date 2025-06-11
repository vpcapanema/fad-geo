from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class TrechoEstadualizacao(Base):
    __tablename__ = "trecho_rodoviario"
    __table_args__ = {"schema": "Elementos_rodoviarios"}

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False, unique=True)
    denominacao = Column(String, nullable=False)
    tipo = Column(String(100), nullable=True)
    municipio = Column(String, nullable=True)
    extensao_km = Column(Float, nullable=True)
    criado_em = Column(DateTime, nullable=True)

    projetos = relationship(
        "Projeto",
        back_populates="trecho",
        primaryjoin="TrechoEstadualizacao.id == Projeto.trecho_id"
    )
