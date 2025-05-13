from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.session import get_db
from app.core.jinja import templates
from app.models.cd_usuario_sistema import UsuarioSistema
from app.models.cd_pessoa_fisica import PessoaFisica
from passlib.hash import bcrypt
import re
# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/usuario',
    tags=['Cadastro de Usuário']
)

router = APIRouter()

# ===============================
# Formulário de Cadastro de Usuário
# ===============================
@router.get("/cadastrar-usuario", response_class=HTMLResponse)
def form_cadastro_usuario(request: Request, db: Session = Depends(get_db)):
    pfs = db.query(PessoaFisica).order_by(PessoaFisica.nome).all()
    return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
        "request": request,
        "pfs": pfs
    })

# ===============================
# Cadastro de novo usuário
# ===============================
@router.post("/cadastrar-usuario", response_class=HTMLResponse)
def cadastrar_usuario(
    request: Request,
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    tipo: str = Form(...),
    pessoa_fisica_id: int = Form(...),
    db: Session = Depends(get_db)
):
    pfs = db.query(PessoaFisica).order_by(PessoaFisica.nome).all()

    # Verifica se o tipo de usuário é 'master', caso seja, não permitir o cadastro via interface
    if tipo == "master":
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ O tipo de usuário 'master' só pode ser criado diretamente pela equipe técnica da FAD."
        })

    # Verifica se as senhas são iguais
    if senha != confirmar_senha:
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ As senhas não coincidem."
        })

    # Normaliza o CPF, removendo caracteres não numéricos
    cpf_limpo = re.sub(r"\D", "", cpf)

    # Verifica se já existe um usuário com a mesma combinação de CPF e tipo
    usuario_existente = db.query(UsuarioSistema).filter(
        UsuarioSistema.cpf == cpf_limpo,
        UsuarioSistema.tipo == tipo
    ).first()

    if usuario_existente:
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ Usuário já cadastrado com este CPF para este tipo."
        })

    # Verifica se o CPF já está associado a outros tipos de usuário
    usuario_com_outra_categoria = db.query(UsuarioSistema).filter(UsuarioSistema.cpf == cpf_limpo).all()
    if len(usuario_com_outra_categoria) >= 3:
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ Este CPF já está cadastrado para os três tipos de usuários."
        })
        

    # Criação do novo usuário
    novo_usuario = UsuarioSistema(
        nome=nome,
        cpf=cpf_limpo,
        email=email,
        telefone=telefone,
        senha_hash=bcrypt.hash(senha),
        tipo=tipo,
        pessoa_fisica_id=pessoa_fisica_id,
        status="aguardando_aprovacao",
        ativo=False
    )
    db.add(novo_usuario)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ Erro ao cadastrar: já existe um usuário com este CPF e tipo."
        })

    return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
        "request": request,
        "pfs": pfs,
        "mensagem_sucesso": "✅ Usuário cadastrado com sucesso. Aguardando aprovação.",
        "mostrar_botao_voltar": True
    })


