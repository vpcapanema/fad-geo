# app/schemas/pr_geometria_upload.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GeometriaUploadBase(BaseModel):
    arquivo_upload: str
    projeto_id: int
    usuario_id: int
    eh_zip: Optional[bool] = False
    tamanho_ok: Optional[bool] = False
    possui_arquivos_obrigatorios: Optional[bool] = False
    possui_geometria: Optional[bool] = False
    cod_preenchido_qtd: Optional[int] = 0
    feicoes_qtd: Optional[int] = 0
    status: Optional[str]
    data_validacao: Optional[datetime]

class GeometriaUploadCreate(GeometriaUploadBase):
    pass

class GeometriaUploadDB(GeometriaUploadBase):
    id: int  # id_geom_up convertido para id

    class Config:
        orm_mode = True
