# app/database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base  # ✅ Base declarativa principal da FAD

# 🎯 String de conexão com o banco de dados PostgreSQL hospedado na AWS RDS
SQLALCHEMY_DATABASE_URL = (
    "postgresql://vinicius:Malditas131533*@fad-db.c7cu4eq2gc56.us-east-2.rds.amazonaws.com:5432/fad_db"
)

# 🔌 Cria o mecanismo de conexão com o banco com parâmetros de pool configurados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,       # Tamanho do pool de conexões
    max_overflow=20,    # Número máximo de conexões extras
    pool_timeout=30,    # ✅ vírgula obrigatória aqui
    pool_pre_ping=True  # Verifica se a conexão está ativa antes de usá-la
)


# 🧵 Cria sessões para uso nas rotas/endpoints
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔁 Função de injeção de dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
