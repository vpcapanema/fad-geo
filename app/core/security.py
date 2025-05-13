# app/security/hashing.py

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha: str) -> str:
    """
    Gera o hash seguro da senha utilizando o algoritmo bcrypt.
    """
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.
    """
    return pwd_context.verify(senha, senha_hash)
