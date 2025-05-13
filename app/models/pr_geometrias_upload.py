# app/models/pr_geometrias_upload.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime
from app.database.base import Base

class GeometriaUpload(Base):
    __tablename__ = "geometrias_upload"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    arquivo = Column(String, nullable=False)
    projeto_id = Column(Integer, ForeignKey("public.projeto.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"), nullable=False)

    # Novas colunas compatíveis com o banco
    arquivo_zip = Column(Boolean, nullable=True, default=False)
    arquivo_menor_50 = Column(Boolean, nullable=True, default=False)
    possui_arquivos_obrigatorios = Column(Boolean, nullable=True, default=False)
    possui_geometria = Column(Boolean, nullable=True, default=False)
    n_cod_trecho_preenchido = Column(Integer, nullable=True)
    n_feicoes = Column(Integer, nullable=True)
    status = Column(String, nullable=True)
    data_validacao = Column(DateTime, nullable=True)

    upload_id = Column(Integer, ForeignKey("public.zip_uploads.id"), nullable=True)
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    geom = Column(Geometry(geometry_type="LINESTRING", srid=4674))

    # Relacionamentos
    projeto = relationship("Projeto", back_populates="uploads")
    usuario = relationship("UsuarioSistema")
    upload = relationship("ZipUpload", back_populates="geometrias")
