from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.cd_trecho import TrechoEstadualizacao
from app.models.rodovia_estadualizacao import RodoviaEstadualizacao
from app.models.dispositivo_estadualizacao import DispositivoEstadualizacao
from app.models.obra_arte_estadualizacao import ObraArteEstadualizacao
from datetime import datetime
import re

router = APIRouter()

# --- Trecho Estadualizacao ---
@router.post("/elementos/trecho", status_code=201)
def criar_trecho(dados: dict = Body(...), db: Session = Depends(get_db)):
    campos = ['codigo', 'denominacao', 'municipio']
    for campo in campos:
        if not dados.get(campo):
            raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {campo}")
    
    # Validação do código do elemento rodoviário
    regex_codigo = r'^[A-Z]{2,}-\d{3,}$'
    if not re.match(regex_codigo, dados['codigo']):
        raise HTTPException(status_code=400, detail="O código deve ter no mínimo duas letras maiúsculas, hífen e três números. Ex: AB-123")
    
    trecho = TrechoEstadualizacao(
        codigo=dados['codigo'],
        denominacao=dados['denominacao'],
        municipio=dados['municipio'],
        criado_em=datetime.utcnow(),
        extensao=dados.get('extensao'),
        tipo=dados.get('tipo')
    )
    db.add(trecho)
    db.commit()
    db.refresh(trecho)
    return {"msg": "Trecho cadastrado com sucesso", "id": trecho.id}

# --- Rodovia Estadualizacao ---
@router.post("/elementos/rodovia", status_code=201)
def criar_rodovia(dados: dict = Body(...), db: Session = Depends(get_db)):
    campos = ['codigo', 'nome', 'uf', 'municipio']
    for campo in campos:
        if not dados.get(campo):
            raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {campo}")
    
    # Validação do código do elemento rodoviário
    regex_codigo = r'^[A-Z]{2,}-\d{3,}$'
    if not re.match(regex_codigo, dados['codigo']):
        raise HTTPException(status_code=400, detail="O código deve ter no mínimo duas letras maiúsculas, hífen e três números. Ex: AB-123")
    
    rodovia = RodoviaEstadualizacao(
        codigo=dados['codigo'],
        nome=dados['nome'],
        uf=dados['uf'],
        extensao_km=dados.get('extensao_km'),
        municipio=dados.get('municipio'),
        criado_em=datetime.utcnow(),
        tipo=dados.get('tipo')
    )
    db.add(rodovia)
    db.commit()
    db.refresh(rodovia)
    return {"msg": "Rodovia cadastrada com sucesso", "id": rodovia.id}

# --- Dispositivo Estadualizacao ---
@router.post("/elementos/dispositivo", status_code=201)
def criar_dispositivo(dados: dict = Body(...), db: Session = Depends(get_db)):
    campos = ['codigo', 'denominacao', 'tipo', 'municipio', 'localizacao']
    for campo in campos:
        if not dados.get(campo):
            raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {campo}")
    
    # Validação do código do elemento rodoviário
    regex_codigo = r'^[A-Z]{2,}-\d{3,}$'
    if not re.match(regex_codigo, dados['codigo']):
        raise HTTPException(status_code=400, detail="O código deve ter no mínimo duas letras maiúsculas, hífen e três números. Ex: AB-123")
    
    # Padronização de campos antes de gravar
    def capitalizar_nome(s):
        if not s: return s
        preps = {"da","de","do","das","dos","e"}
        return ' '.join([w if w in preps else w.capitalize() for w in s.lower().split()])
    dados['denominacao'] = capitalizar_nome(dados.get('denominacao', ''))
    dados['municipio'] = capitalizar_nome(dados.get('municipio', ''))
    dados['localizacao'] = capitalizar_nome(dados.get('localizacao', ''))
    
    dispositivo = DispositivoEstadualizacao(
        codigo=dados['codigo'],
        denominacao=dados['denominacao'],
        tipo=dados['tipo'],
        localizacao=dados['localizacao'],
        municipio=dados['municipio'],
        criado_em=datetime.utcnow()
    )
    db.add(dispositivo)
    db.commit()
    db.refresh(dispositivo)
    return {"msg": "Dispositivo cadastrado com sucesso", "id": dispositivo.id}

# --- Obra de Arte Estadualizacao ---
@router.post("/elementos/obra-arte", status_code=201)
def criar_obra_arte(dados: dict = Body(...), db: Session = Depends(get_db)):
    campos = ['codigo', 'denominacao', 'tipo', 'municipio', 'extensao_m', 'localizacao']
    for campo in campos:
        if not dados.get(campo):
            raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {campo}")
    
    # Validação do código do elemento rodoviário
    regex_codigo = r'^[A-Z]{2,}-\d{3,}$'
    if not re.match(regex_codigo, dados['codigo']):
        raise HTTPException(status_code=400, detail="O código deve ter no mínimo duas letras maiúsculas, hífen e três números. Ex: AB-123")
    
    # Padronização de campos antes de gravar
    def capitalizar_nome(s):
        if not s: return s
        preps = {"da","de","do","das","dos","e"}
        return ' '.join([w if w in preps else w.capitalize() for w in s.lower().split()])
    dados['denominacao'] = capitalizar_nome(dados.get('denominacao', ''))
    dados['municipio'] = capitalizar_nome(dados.get('municipio', ''))
    dados['localizacao'] = capitalizar_nome(dados.get('localizacao', ''))
    
    obra = ObraArteEstadualizacao(
        codigo=dados['codigo'],
        denominacao=dados['denominacao'],
        tipo=dados['tipo'],
        extensao_m=dados['extensao_m'],
        localizacao=dados['localizacao'],
        municipio=dados['municipio'],
        criado_em=datetime.utcnow()
    )
    db.add(obra)
    db.commit()
    db.refresh(obra)
    return {"msg": "Obra de arte cadastrada com sucesso", "id": obra.id}
