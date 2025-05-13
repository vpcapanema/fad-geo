# app/api/endpoints/pr_salvar_temp_validacao.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.pr_temp_validacao_geometria import TempValidacaoGeometria
from app.models.pr_geometrias_upload import GeometriaUpload

def salvar_resultado_temporario(
    db: Session,
    id_geom_upload: int,
    criterios: dict,
    aprovado: bool
) -> int:
    try:
        origem = db.query(GeometriaUpload).filter(GeometriaUpload.id == id_geom_upload).first()
        if not origem:
            raise HTTPException(status_code=404, detail="Geometria não encontrada.")

        validacao = TempValidacaoGeometria(
            arquivo=origem.arquivo,
            projeto_id=origem.projeto_id,
            usuario_id=origem.usuario_id,
            arquivos_obrigatorios=True,
            tem_geometria=True,
            cod_preenchido=criterios.get("V3", False),
            epsg_origem=4674,
            epsg_convertido=criterios.get("V1", False),
            topologia_valida=criterios.get("V6", False),
            comprimento_valido=criterios.get("V9", False),
            sem_sobreposicao=criterios.get("V8", False),
            dentro_sp=criterios.get("V7", False),
            status="aprovado" if aprovado else "reprovado",
            validado_em=datetime.utcnow(),
            geom=origem.geom
        )

        db.add(validacao)
        db.commit()
        db.refresh(validacao)
        return validacao.id

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar validação: {str(e)}")
