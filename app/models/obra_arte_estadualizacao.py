from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database.base import Base
from datetime import datetime

class ObraArteEstadualizacao(Base):
    __tablename__ = "obra_arte_estadualizacao"
    __table_args__ = {"schema": "Elementos_rodoviarios"}

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False, unique=True)
    denominacao = Column(String, nullable=False)
    tipo = Column(String(100), nullable=False)
    extensao_m = Column(Float, nullable=False)
    localizacao = Column(String, nullable=False)
    municipio = Column(String, nullable=False)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
