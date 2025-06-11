# app/schemas/cd_usuario_sistema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nome: str
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF com ou sem formatação (será limpo no backend)")
    email: EmailStr
    telefone: Optional[str] = None
    senha: str
    tipo: str  # "analista", "coordenador", "master"
    pessoa_fisica_id: Optional[int] = None  # ID da PF associada (se aplicável)
    instituicao: Optional[str] = None
    tipo_lotacao: Optional[str] = None
    email_institucional: Optional[EmailStr] = None
    telefone_institucional: Optional[str] = None
    ramal: Optional[str] = None
    sede_hierarquia: Optional[str] = None
    sede_coordenadoria: Optional[str] = None
    sede_setor: Optional[str] = None
    sede_assistencia: Optional[str] = None
    regional_nome: Optional[str] = None
    regional_coordenadoria: Optional[str] = None
    regional_setor: Optional[str] = None

class UsuarioOut(BaseModel):
    id: int
    nome: str
    cpf: str
    email: EmailStr
    telefone: Optional[str]
    tipo: str
    status: str
    ativo: bool
    instituicao: Optional[str] = None
    tipo_lotacao: Optional[str] = None
    email_institucional: Optional[EmailStr] = None
    telefone_institucional: Optional[str] = None
    ramal: Optional[str] = None
    sede_hierarquia: Optional[str] = None
    sede_coordenadoria: Optional[str] = None
    sede_setor: Optional[str] = None
    sede_assistencia: Optional[str] = None
    regional_nome: Optional[str] = None
    regional_coordenadoria: Optional[str] = None
    regional_setor: Optional[str] = None

    class Config:
        from_attributes = True

class UsuarioDB(UsuarioOut):
    pessoa_fisica_id: Optional[int]
    criado_em: Optional[datetime]
    aprovado_em: Optional[datetime]
    aprovador_id: Optional[int]
