from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
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
    trecho_id = Column(Integer, ForeignKey("Elementos_rodoviarios.trecho_rodoviario.id"))
    geometria_id = Column(Integer)

    enviado_em = Column(DateTime)
    usuario_id = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"))
    aprovado_em = Column(DateTime)
    aprovador_id = Column(Integer, ForeignKey("Cadastro.usuario_sistema.id"))
    observacao = Column(Text)
    status = Column(String, default="em cadastramento")
    
    # Colunas de controle de fluxo modular
    modulo_atual = Column(Integer, default=1)
    status_fluxo = Column(String(50), default="iniciado")
    todos_modulos_concluidos = Column(Boolean, default=False)
    pronto_para_pdf = Column(Boolean, default=False)    # Relacionamentos
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
    relatorios_modulos = relationship("RelatorioModulo", back_populates="projeto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Projeto(id={self.id}, nome='{self.nome}', status='{self.status}')>"

    @property
    def modulo_atual_nome(self):
        """Retorna o nome do módulo atual baseado no número"""
        modulos = {
            1: "Cadastro",
            2: "Conformidade Ambiental", 
            3: "Favorabilidade Multicritério",
            4: "Favorabilidade Socioeconômica",
            5: "Favorabilidade Infraestrutural"
        }
        return modulos.get(self.modulo_atual, "Desconhecido")

    @property
    def progresso_percentual(self):
        """Calcula o progresso em percentual baseado nos módulos validados"""
        if not self.relatorios_modulos:
            return 0
        validados = sum(1 for r in self.relatorios_modulos if r.status == 'validado')
        return int((validados / 5) * 100)

    def pode_avancar_modulo(self):
        """Verifica se pode avançar para o próximo módulo"""
        if self.modulo_atual >= 5:
            return False
        
        # Verifica se o módulo atual está validado
        modulo_atual_rel = next((r for r in self.relatorios_modulos if r.modulo_numero == self.modulo_atual), None)
        return modulo_atual_rel and modulo_atual_rel.status == 'validado'

    def get_status_modulo(self, numero_modulo):
        """Retorna o status de um módulo específico"""
        modulo = next((r for r in self.relatorios_modulos if r.modulo_numero == numero_modulo), None)
        return modulo.status if modulo else 'pendente'

