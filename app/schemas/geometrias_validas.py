# app/schemas/pr_geometria_validada.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 🔹 Base com campos comuns
class GeometriaValidadaBase(BaseModel):
    usuario_id: int
    projeto_id: int
    cod: Optional[str]
    nome_arquivo: Optional[str]

# 🔸 Payload de criação
class GeometriaValidadaCreate(GeometriaValidadaBase):
    geometria_wkt: str  # Geometria em WKT no SRID 4674 (LINESTRING)

# 🔸 Retorno da API
class GeometriaValidadaOut(GeometriaValidadaBase):
    id: int
    data_validacao: datetime

    class Config:
        from_attributes = True
