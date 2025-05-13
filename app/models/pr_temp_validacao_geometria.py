# app/models/pr_temp_validacao_geometria.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class TempValidacaoGeometria(Base):
    __tablename__ = "temp_validacao_geometria"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    arquivo = Column(String, nullable=False)
    projeto_id = Column(Integer, ForeignKey("public.projeto.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"), nullable=False)

    arquivos_obrigatorios = Column(Boolean, default=False)
    tem_geometria = Column(Boolean, default=False)
    cod_preenchido = Column(Boolean, default=False)
    epsg_origem = Column(Integer, nullable=True)
    epsg_convertido = Column(Boolean, default=False)
    topologia_valida = Column(Boolean, default=False)
    comprimento_valido = Column(Boolean, default=False)
    sem_sobreposicao = Column(Boolean, default=False)
    dentro_sp = Column(Boolean, default=False)

    status = Column(String, index=True)
    validado_em = Column(DateTime, default=datetime.utcnow)
    geom = Column(Geometry(geometry_type="LINESTRING", srid=4674))

    # Relacionamentos
    projeto = relationship("Projeto")
    usuario = relationship("UsuarioSistema")
