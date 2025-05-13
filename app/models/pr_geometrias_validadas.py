# app/models/pr_geometrias_validadas.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from geoalchemy2 import Geometry
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.base import Base

class GeometriaValidada(Base):
    __tablename__ = "geometrias_validadas"
    __table_args__ = (
        CheckConstraint(
            "status IN ('validada', 'reprovada', 'aguardando')",
            name="chk_status_geometria_valida"
        ),
        {"schema": "public"},
    )

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id", ondelete="CASCADE"), nullable=False)
    projeto_id = Column(Integer, ForeignKey("public.projeto.id", ondelete="CASCADE"), nullable=False)
    upload_id = Column(Integer, ForeignKey("public.zip_uploads.id"), nullable=False)

    cod = Column(String, nullable=True)
    arquivo = Column(String, nullable=True)
    geom = Column(Geometry(geometry_type="LINESTRING", srid=4674), nullable=False)
    validado_em = Column(DateTime, default=datetime.utcnow)
    status = Column(String(30), nullable=True)

    # Relacionamentos
    usuario = relationship("UsuarioSistema")
    projeto = relationship("Projeto")
    upload = relationship("ZipUpload")
