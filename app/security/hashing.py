# app/security/hashing.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha_plana: str) -> str:
    """Gera o hash de uma senha"""
    return pwd_context.hash(senha_plana)

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica se uma senha corresponde ao hash"""
    return pwd_context.verify(senha_plana, senha_hash)
