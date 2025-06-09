from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database.base import Base
from datetime import datetime

class RodoviaEstadualizacao(Base):
    __tablename__ = "rodovia_estadualizacao"
    __table_args__ = {"schema": "Elementos_rodoviarios"}

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False, unique=True)
    nome = Column(String, nullable=False)
    uf = Column(String(2), nullable=False)
    extensao_km = Column(Float, nullable=True)
    municipio = Column(String, nullable=True)
    municipio = Column(String, nullable=True)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    tipo = Column(String(100), nullable=True)
