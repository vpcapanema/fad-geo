# app/api/endpoints/delete_upload.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from sqlalchemy import text
# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/shape/limpeza',
    tags=['Limpeza de Geometrias']
)
from app.api.dependencies import get_current_user

router = APIRouter()

# ===============================
# 🗑️ Deletar arquivos de upload não processados
# ===============================
@router.delete("/delete-uploaded-file")
def delete_uploaded_file(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        db.execute(text('DELETE FROM "public".geometrias_upload WHERE status = :status'), {"status": "pendente"})
        db.commit()
        return {"sucesso": True, "mensagem": "Arquivos pendentes excluídos com sucesso."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao excluir uploads: {str(e)}")
