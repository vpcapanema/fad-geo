from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database.base import Base
from datetime import datetime

class ObraArteEstadualizacao(Base):
    __tablename__ = "obra_arte"
    __table_args__ = {"schema": "Elementos_rodoviarios"}

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False, unique=True)
    denominacao = Column(String, nullable=False)
    tipo = Column(String(100), nullable=False)
    municipio = Column(String, nullable=True)
    extensao_km = Column(Float, nullable=True)
    criado_em = Column(DateTime, nullable=True, default=datetime.utcnow)
