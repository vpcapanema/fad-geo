# app/schemas/pr_temp_validacao_geometria.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TempValidacaoGeometriaBase(BaseModel):
    arquivo_upload: str
    projeto_id: int
    usuario_id: int
    arquivos_obrigatorios: Optional[bool] = False
    tem_geometria: Optional[bool] = False
    cod_preenchido: Optional[bool] = False
    epsg_origem: Optional[int]
    epsg_ok: Optional[bool] = False
    topologia_valida: Optional[bool] = False
    comprimento_valido: Optional[bool] = False
    sem_sobreposicao: Optional[bool] = False
    dentro_sp: Optional[bool] = False
    status: Optional[str]
    validado_em: Optional[datetime] = None

class TempValidacaoGeometriaCreate(TempValidacaoGeometriaBase):
    pass

class TempValidacaoGeometriaOut(TempValidacaoGeometriaBase):
    id: int

    class Config:
        from_attributes = True

