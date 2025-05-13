# app/api/endpoints/pr_salvar_geometria_validada.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.session import get_db
from app.models.pr_geometrias_validadas import GeometriaValidada
# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/shape/salvar',
    tags=['Salvar Geometria Validada']
)
from app.models.pr_geometrias_upload import GeometriaUpload

router = APIRouter()

@router.post("/geometrias/salvar")
def salvar_geom_definitiva(db: Session = Depends(get_db)):
    geom_upload = db.query(GeometriaUpload).order_by(GeometriaUpload.criado_em.desc()).first()

    if not geom_upload:
        raise HTTPException(status_code=404, detail="Nenhuma geometria disponível.")

    nova = GeometriaValidada(
        projeto_id=geom_upload.projeto_id,
        usuario_id=geom_upload.usuario_id,
        cod=None,
        arquivo=geom_upload.arquivo,
        geom=geom_upload.geom,
        validado_em=datetime.utcnow()
    )

    db.add(nova)
    db.commit()
    return {"sucesso": True}
