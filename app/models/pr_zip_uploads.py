# app/models/pr_zip_uploads.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class ZipUpload(Base):
    __tablename__ = "zip_uploads"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    arquivo = Column(String, nullable=False)
    tipo_arquivo = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"), nullable=False)
    projeto_id = Column(Integer, ForeignKey("public.projeto.id"), nullable=False)
    status = Column(String, nullable=True, default="recebido") # possíveis 'recebido', 'erro', 'extraído'
    data_upload = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    usuario = relationship("UsuarioSistema")
    projeto = relationship("Projeto")
    geometrias = relationship("GeometriaUpload", back_populates="upload", cascade="all, delete-orphan")
    geometrias_validadas = relationship("GeometriaValidada", back_populates="upload")

