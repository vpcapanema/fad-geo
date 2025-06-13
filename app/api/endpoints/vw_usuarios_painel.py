from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.session import get_db

router = APIRouter()

@router.get("/painel-analista/usuarios")
def listar_usuarios_comuns(db: Session = Depends(get_db)):
    try:        
        query = text("""
            SELECT id, nome, cpf, email, telefone, status, tipo as tipo_usuario,
                   criado_em, aprovado_em, aprovador_id, ativo, pessoa_fisica_id,
                   instituicao, tipo_lotacao, email_institucional, telefone_institucional, ramal,
                   sede_hierarquia, sede_coordenadoria, sede_assistencia,
                   regional_nome, regional_coordenadoria, regional_setor
            FROM "Cadastro".usuario_sistema
            WHERE tipo = 'analista'
            ORDER BY nome
        """)
        resultados = db.execute(query).mappings().all()
        return list(resultados)
    except Exception as e:
        return {"erro": str(e)}

@router.get("/painel-coordenador/usuarios")
def listar_usuarios_coordenadores(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT id, nome, cpf, email, telefone, status, tipo as tipo_usuario,
                   criado_em, aprovado_em, aprovador_id, ativo, pessoa_fisica_id,
                   instituicao, tipo_lotacao, email_institucional, telefone_institucional, ramal,
                   sede_hierarquia, sede_coordenadoria, sede_assistencia,
                   regional_nome, regional_coordenadoria, regional_setor
            FROM "Cadastro".usuario_sistema
            WHERE tipo = 'coordenador'
            ORDER BY nome
        """)
        resultados = db.execute(query).mappings().all()
        return list(resultados)
    except Exception as e:
        return {"erro": str(e)}
