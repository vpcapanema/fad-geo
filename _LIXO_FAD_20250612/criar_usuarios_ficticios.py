from app.database.session import SessionLocal
from app.models.cd_pessoa_fisica import PessoaFisica
from app.models.cd_usuario_sistema import UsuarioSistema
from datetime import datetime
from sqlalchemy.exc import IntegrityError

def criar_usuarios_ficticios():
    db = SessionLocal()
    pessoas = db.query(PessoaFisica).all()
    for i, pf in enumerate(pessoas):
        tipo = 'coordenador' if i % 2 == 0 else 'analista'
        usuario = UsuarioSistema(
            nome=pf.nome + ' (usuário)',
            cpf=pf.cpf,
            email=pf.email,
            telefone=pf.telefone,
            senha_hash='123456',
            tipo=tipo,
            pessoa_fisica_id=pf.id,
            criado_em=datetime.now(),
            status='ativo',
            ativo=True,
            instituicao='Instituição Exemplo',
            tipo_lotacao='Efetivo',
            email_institucional=pf.email.replace('@','_inst@'),
            telefone_institucional=pf.telefone,
            ramal='1234',
            sede_hierarquia='Sede',
            sede_coordenadoria='Coord',
            sede_setor='Setor',
            sede_assistencia='Assistência',
            regional_nome='Regional',
            regional_coordenadoria='Coord Regional',
            regional_setor='Setor Regional'
        )
        db.add(usuario)
        try:
            db.commit()
            print(f'Usuário criado para {pf.nome} ({tipo})')
        except IntegrityError:
            db.rollback()
            print(f'Usuário já existe para {pf.cpf}')
    db.close()

if __name__ == "__main__":
    criar_usuarios_ficticios()
