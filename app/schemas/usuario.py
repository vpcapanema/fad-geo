# app/schemas/cd_usuario_sistema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nome: str
    cpf: str = Field(..., pattern=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
    email: EmailStr
    telefone: Optional[str] = None
    senha: str
    tipo: str  # "comum", "administrador", "master"
    pessoa_fisica_id: Optional[int] = None  # ID da PF associada (se aplicável)

class UsuarioOut(BaseModel):
    id: int
    nome: str
    cpf: str
    email: EmailStr
    telefone: Optional[str]
    tipo: str
    status: str
    ativo: bool

    class Config:
        orm_mode = True

class UsuarioDB(UsuarioOut):
    pessoa_fisica_id: Optional[int]
    criado_em: Optional[datetime]
    aprovado_em: Optional[datetime]
    aprovador_id: Optional[int]
