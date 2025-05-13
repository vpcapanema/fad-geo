# app/models/vw_projetos_usuario_comum.py

from pydantic import BaseModel

class ProjetoResumo(BaseModel):
    id_projeto: int
    nome_projeto: str
    interessado: str
    representante: str
    status_geometria: str
    status_conformidade: str
    status_fm: str
    status_fs: str
    status_fi: str
    status_geral: str
