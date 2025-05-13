from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.cd_pessoa_fisica import PessoaFisica
from app.models.cd_pessoa_juridica import PessoaJuridica
from app.models.cd_usuario_sistema import UsuarioSistema

class Projeto(Base):
    __tablename__ = "projeto"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)

    pessoa_juridica_id = Column(Integer, ForeignKey("Cadastro.pessoa_juridica.id"))
    pessoa_fisica_id = Column(Integer, ForeignKey("Cadastro.pessoa_fisica.id"))
    trecho_id = Column(Integer, ForeignKey("Elementos_rodoviarios.trechos_estadualizacao.id"))
    geometria_id = Column(Integer)

    enviado_em = Column(DateTime)
    usuario_id = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"))
    aprovado_em = Column(DateTime)
    aprovador_id = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"))
    observacao = Column(Text)
    status = Column(String, default="em cadastramento")

    # Relacionamentos
    pessoa_juridica = relationship(
        "PessoaJuridica",
        back_populates="projetos",
        primaryjoin="Projeto.pessoa_juridica_id == PessoaJuridica.id"
    )
    
    trecho = relationship(
        "TrechoEstadualizacao",
        back_populates="projetos",
        primaryjoin="Projeto.trecho_id == TrechoEstadualizacao.id"
    )

    aprovador = relationship("UsuarioSistema", foreign_keys=[aprovador_id])
    uploads = relationship("GeometriaUpload", back_populates="projeto")

