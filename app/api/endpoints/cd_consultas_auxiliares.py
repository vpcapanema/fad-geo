from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.cd_pessoa_fisica import PessoaFisica
from app.models.cd_pessoa_juridica import PessoaJuridica
from app.models.cd_trecho_estadualizacao import TrechoEstadualizacao

router = APIRouter(
    prefix="/cadastro",
    tags=["Listas JSON"]
)

@router.get("/pfs/json")
def listar_pfs(db: Session = Depends(get_db)):
    return db.query(PessoaFisica).all()

@router.get("/pjs/json")
def listar_pjs(db: Session = Depends(get_db)):
    return db.query(PessoaJuridica).all()

@router.get("/trechos/json")
def listar_trechos(db: Session = Depends(get_db)):
    return db.query(TrechoEstadualizacao).all()
