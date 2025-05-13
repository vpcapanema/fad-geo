from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.session import get_db
from app.models.pr_projeto import Projeto

router = APIRouter(
    prefix="/projeto",
    tags=["Gravação de Projeto - Etapa Final"]
)

@router.post("/salvar-final")
def salvar_etapa_final(
    projeto_id: int = Form(...),
    geometria_id: int = Form(...),
    modulos: str = Form(...),
    db: Session = Depends(get_db)
):
    projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()

    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")

    projeto.geometria_id = geometria_id
    projeto.status = "finalizado"
    projeto.enviado_em = datetime.now()
    # futuros campos: projeto.modulos = modulos.split(",")

    db.commit()
    return {"sucesso": True, "mensagem": "Projeto finalizado com sucesso."}
