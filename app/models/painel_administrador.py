from pydantic import BaseModel
from typing import Optional

class UsuarioAprovado(BaseModel):
    id: int
    nome: str
    cpf: str
    email: str
    telefone: Optional[str]
    status: str

class ProjetoRecebido(BaseModel):
    id: int
    nome: str
    municipio: str
    pessoa_juridica: str  # Interessado
    pessoa_fisica: str    # Representante
    usuario: str          # Cadastrante
    status: str
