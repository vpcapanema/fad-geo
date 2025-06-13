# app/database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base  # ✅ Base declarativa principal da FAD
import os

# 🎯 Configuração do banco de dados
POSTGRES_URL = (
    "postgresql://vinicius:Malditas131533*@fad-db.c7cu4eq2gc56.us-east-2.rds.amazonaws.com:5432/fad_db"
)

# � Fallback para SQLite local se PostgreSQL não estiver disponível
SQLITE_URL = "sqlite:///./database.db"

# 🔌 Tenta conectar ao PostgreSQL primeiro, senão usa SQLite
try:
    print("Tentando conectar ao PostgreSQL...")
    engine = create_engine(
        POSTGRES_URL,
        pool_size=10,
        max_overflow=20,
        pool_timeout=5,  # Timeout reduzido para falhar rapidamente
        pool_pre_ping=True    )
    # Testa a conexão
    with engine.connect() as conn:
        conn.execute("SELECT 1")
    print("✅ Conectado ao PostgreSQL!")
    SQLALCHEMY_DATABASE_URL = POSTGRES_URL
except Exception as e:
    print(f"❌ Erro ao conectar ao PostgreSQL: {e}")
    print("🔄 Usando SQLite local como fallback...")
    engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False}
    )
    
    # Criar as tabelas no SQLite se não existirem
    print("📊 Criando tabelas no SQLite...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas no SQLite!")
    
    SQLALCHEMY_DATABASE_URL = SQLITE_URL


# 🧵 Cria sessões para uso nas rotas/endpoints
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔁 Função de injeção de dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
