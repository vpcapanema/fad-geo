from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from app.database.session import get_db
from app.models.pr_geometrias_upload import GeometriaUpload
from app.models.pr_geometrias_validadas import GeometriaValidada
from app.api.endpoints.pr_salvar_temp_validacao import salvar_resultado_temporario
from app.utils.utils_gerar_relatorio_validacao import gerar_relatorio_validacao
# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/shape/validacao',
    tags=['Validação de Geometria']
)

router = APIRouter()

@router.get("/validar")
def validar_geometria(db: Session = Depends(get_db)):
    try:
        geom_upload = (
            db.query(GeometriaUpload)
            .filter(GeometriaUpload.arquivo != None)
            .order_by(GeometriaUpload.criado_em.desc())
            .first()
        )

        if not geom_upload:
            return JSONResponse(status_code=404, content={"validado": False, "erro": "Nenhuma geometria para validar."})

        id_geom = geom_upload.id

        def checar(query: str) -> bool:
            resultado = db.execute(text(query)).scalar()
            return bool(resultado)

        criterios = {
            "V1": checar(f"SELECT ST_SRID(geom) = 4674 FROM geometrias_upload WHERE id = {id_geom}"),
            "V2": checar(f"SELECT GeometryType(geom) = 'LINESTRING' FROM geometrias_upload WHERE id = {id_geom}"),
            "V3": checar(f"SELECT EXISTS (SELECT 1 FROM geometrias_upload WHERE id = {id_geom} AND cod IS NOT NULL AND cod != '')"),
            "V4": checar(f"SELECT COUNT(*) > 0 FROM geometrias_upload WHERE id = {id_geom}"),
            "V5": checar(f"SELECT NOT ST_IsEmpty(geom) FROM geometrias_upload WHERE id = {id_geom}"),
            "V6": checar(f"SELECT ST_IsValid(geom) FROM geometrias_upload WHERE id = {id_geom}"),
            "V7": checar(f'''
                SELECT ST_Within(
                    geom,
                    (SELECT geom FROM "DataGEO".limite_estadual WHERE uf = 'SP' LIMIT 1)
                )
                FROM geometrias_upload WHERE id = {id_geom}
            '''),
            "V8": checar(f'''
                SELECT NOT EXISTS (
                    SELECT 1
                    FROM geometrias_upload AS a, geometrias_upload AS b
                    WHERE a.id != b.id AND ST_Overlaps(a.geom, b.geom)
                )
            '''),
            "V9": checar(f"SELECT ST_Length(geom::geography) > 10 FROM geometrias_upload WHERE id = {id_geom}")
        }

        aprovado = all(criterios.values())

        id_validacao = salvar_resultado_temporario(
            db=db,
            id_geom_upload=id_geom,
            criterios=criterios,
            aprovado=aprovado
        )

        nome_pdf = f"validacao_{id_validacao}.pdf"
        gerar_relatorio_validacao(
            usuario=geom_upload,
            resultados_dict=criterios,
            erros=[] if aprovado else ["Critérios não atendidos"],
            aprovado=aprovado,
            nome_pdf=nome_pdf
        )

        if aprovado:
            geom_validada = GeometriaValidada(
                projeto_id=geom_upload.projeto_id,
                usuario_id=geom_upload.usuario_id,
                cod=None,
                arquivo=geom_upload.arquivo,
                geom=geom_upload.geom,
                validado_em=datetime.utcnow()
            )
            db.add(geom_validada)
            db.commit()

        return JSONResponse(content={"validado": aprovado})

    except Exception as e:
        return JSONResponse(status_code=500, content={"validado": False, "erro": str(e)})
