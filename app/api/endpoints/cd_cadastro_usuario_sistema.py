from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.session import get_db
from app.core.jinja import templates
from app.models.cd_usuario_sistema import UsuarioSistema
from app.models.cd_pessoa_fisica import PessoaFisica
from app.schemas.usuario import UsuarioCreate
from passlib.hash import bcrypt
import re
from fastapi import Request
import logging

# Configuração básica de logging para debug detalhado
logging.basicConfig(level=logging.INFO, format='[FAD DEBUG] %(asctime)s %(levelname)s %(message)s')

def log_requisicao(request: Request, etapa: str, info_extra: str = ""):
    logging.info(f"{etapa} | {request.method} {request.url.path} | IP: {request.client.host} | {info_extra}")

# ✅ Padrão de roteador aplicado
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
    instituicao: str = Form(None),
    tipo_lotacao: str = Form(None),
    email_institucional: str = Form(None),
    telefone_institucional: str = Form(None),
    ramal: str = Form(None),
    sede_hierarquia: str = Form(None),
    sede_coordenadoria: str = Form(None),
    sede_setor: str = Form(None),
    sede_assistencia: str = Form(None),
    regional_nome: str = Form(None),
    regional_coordenadoria: str = Form(None),
    regional_setor: str = Form(None),
    db: Session = Depends(get_db)
):
    pfs = db.query(PessoaFisica).order_by(PessoaFisica.nome).all()

    log_requisicao(request, "INÍCIO", "Dados recebidos para cadastro")

    # Verifica se o tipo de usuário é 'master', caso seja, não permitir o cadastro via interface
    if tipo == "master":
        log_requisicao(request, "FIM", "Tentativa de cadastro com tipo 'master'")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ O tipo de usuário 'master' só pode ser criado diretamente pela equipe técnica da FAD."
        })

    # Verifica se as senhas são iguais
    if senha != confirmar_senha:
        log_requisicao(request, "FIM", "Senhas não coincidem")
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
        log_requisicao(request, "FIM", "Usuário já cadastrado com este CPF e tipo")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ Usuário já cadastrado com este CPF para este tipo."
        })

    # Verifica se o CPF já está associado a outros tipos de usuário
    usuario_com_outra_categoria = db.query(UsuarioSistema).filter(UsuarioSistema.cpf == cpf_limpo).all()
    if len(usuario_com_outra_categoria) >= 3:
        log_requisicao(request, "FIM", "CPF já cadastrado para os três tipos de usuários")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ Este CPF já está cadastrado para os três tipos de usuários."
        })
        
    # Validações adicionais de formato e obrigatoriedade
    obrigatorios = [nome, cpf, email, telefone, senha, confirmar_senha, tipo, pessoa_fisica_id, instituicao, tipo_lotacao, email_institucional, telefone_institucional, ramal, sede_hierarquia, sede_coordenadoria, sede_setor, sede_assistencia, regional_nome, regional_coordenadoria, regional_setor]
    if any(x is None or str(x).strip() == '' for x in obrigatorios):
        log_requisicao(request, "FIM", "Campos obrigatórios não preenchidos")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ Todos os campos são obrigatórios. Preencha todos corretamente."
        })
    email_regex = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    telefone_regex = r"^\(\d{2}\) \d{4,5}-\d{4}$"
    cpf_regex = r"^\d{11}$"
    ramal_regex = r"^\d{4,10}$"
    if not re.match(email_regex, email):
        log_requisicao(request, "FIM", "E-mail pessoal inválido")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ E-mail pessoal inválido."
        })
    if not re.match(email_regex, email_institucional):
        log_requisicao(request, "FIM", "E-mail institucional inválido")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ E-mail institucional inválido."
        })
    if not re.match(telefone_regex, telefone):
        log_requisicao(request, "FIM", "Telefone pessoal inválido")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ Telefone pessoal inválido. Use o formato (XX) XXXXX-XXXX."
        })
    if not re.match(telefone_regex, telefone_institucional):
        log_requisicao(request, "FIM", "Telefone institucional inválido")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ Telefone institucional inválido. Use o formato (XX) XXXXX-XXXX."
        })
    if not re.match(cpf_regex, re.sub(r"\D", "", cpf)):
        log_requisicao(request, "FIM", "CPF inválido")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ CPF inválido."
        })
    if not re.match(ramal_regex, ramal):
        log_requisicao(request, "FIM", "Ramal inválido")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ Ramal inválido. Deve conter ao menos 4 dígitos."
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
        ativo=False,
        instituicao=instituicao,
        tipo_lotacao=tipo_lotacao,
        email_institucional=email_institucional,
        telefone_institucional=telefone_institucional,
        ramal=ramal,
        sede_hierarquia=sede_hierarquia,
        sede_coordenadoria=sede_coordenadoria,
        sede_setor=sede_setor,
        sede_assistencia=sede_assistencia,
        regional_nome=regional_nome,
        regional_coordenadoria=regional_coordenadoria,
        regional_setor=regional_setor
    )
    db.add(novo_usuario)

    try:
        db.commit()
        log_requisicao(request, "FIM", "Usuário cadastrado com sucesso")
        db.refresh(novo_usuario)

        # Buscar dados completos do usuário e pessoa física
        usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == novo_usuario.id).first()
        pessoa_fisica = db.query(PessoaFisica).filter(PessoaFisica.id == usuario.pessoa_fisica_id).first()

        # Renderizar template HTML
        from datetime import datetime
        from app.core.jinja import templates as jinja_templates
        html_content = jinja_templates.get_template("formularios_cadastro_usuarios/cadastro_usuario_template.html").render(
            usuario=usuario,
            pessoa_fisica=pessoa_fisica,
            data_geracao=datetime.now(),
            request=request
        )

        # Salvar HTML
        import os
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "formularios_cadastro")
        os.makedirs(base_dir, exist_ok=True)
        pasta_usuario = f"usuario_{usuario.id:04d}_{datetime.now().strftime('%Y%m%d')}"
        caminho_pasta = os.path.join(base_dir, pasta_usuario)
        os.makedirs(caminho_pasta, exist_ok=True)
        nome_arquivo_html = f"cadastro_usuario_{usuario.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_v1.html"
        caminho_html = os.path.join(caminho_pasta, nome_arquivo_html)
        with open(caminho_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Converter HTML para PDF
        import pdfkit
        nome_arquivo_pdf = nome_arquivo_html.replace('.html', '.pdf')
        caminho_pdf = os.path.join(caminho_pasta, nome_arquivo_pdf)
        pdfkit.from_file(caminho_html, caminho_pdf)

        # Enviar e-mail com PDF em anexo
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'fadgeoteste@gmail.com'
        smtp_pass = 'Malditas131533*'
        destinatario = usuario.email
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = destinatario
        msg['Subject'] = 'Cadastro realizado com sucesso - FAD'
        corpo = f"Olá, {usuario.nome}!\n\nSeu cadastro foi realizado com sucesso no sistema FAD. Em anexo está seu comprovante de cadastro.\n\nAtenciosamente,\nEquipe FAD."
        msg.attach(MIMEText(corpo, 'plain'))
        with open(caminho_pdf, "rb") as f:
            part = MIMEApplication(f.read(), Name=nome_arquivo_pdf)
            part['Content-Disposition'] = f'attachment; filename="{nome_arquivo_pdf}"'
            msg.attach(part)
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        data_envio_email = datetime.now()

        # Registrar na tabela de controle
        db.execute(
            """
            INSERT INTO formularios_usuario (usuario_id, arquivo_nome, caminho_completo, data_geracao, versao, ativo, tamanho_arquivo, status, data_envio_email)
            VALUES (:usuario_id, :arquivo_nome, :caminho_completo, :data_geracao, :versao, :ativo, :tamanho_arquivo, :status, :data_envio_email)
            """,
            {
                'usuario_id': usuario.id,
                'arquivo_nome': nome_arquivo_pdf,
                'caminho_completo': caminho_pdf,
                'data_geracao': datetime.now(),
                'versao': 1,
                'ativo': True,
                'tamanho_arquivo': os.path.getsize(caminho_pdf),
                'status': 'ativo',
                'data_envio_email': data_envio_email
            }
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        log_requisicao(request, "FIM", "Erro ao cadastrar usuário: CPF/tipo duplicado")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": "❌ Erro ao cadastrar: já existe um usuário com este CPF e tipo."
        })
    except Exception as e:
        db.rollback()
        log_requisicao(request, "FIM", f"Erro geral: {e}")
        return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
            "request": request,
            "pfs": pfs,
            "mensagem_erro": f"❌ Erro ao gerar comprovante: {e}"
        })

    return templates.TemplateResponse("cd_cadastro_usuario_sistema.html", {
        "request": request,
        "pfs": pfs,
        "mensagem_sucesso": "✅ Usuário cadastrado com sucesso. Comprovante enviado por e-mail.",
        "mostrar_botao_voltar": True
    })

# ===============================
# Edição de Usuário
# ===============================
@router.put("/{usuario_id}", response_class=JSONResponse)
def editar_usuario(
    usuario_id: int,
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        return JSONResponse(status_code=404, content={"detail": "Usuário não encontrado."})

    # Atualiza todos os campos recebidos
    usuario.nome = dados.nome
    usuario.cpf = re.sub(r"\D", "", dados.cpf)
    usuario.email = dados.email
    usuario.telefone = dados.telefone
    usuario.tipo = dados.tipo
    usuario.pessoa_fisica_id = dados.pessoa_fisica_id
    usuario.instituicao = dados.instituicao
    usuario.tipo_lotacao = dados.tipo_lotacao
    usuario.email_institucional = dados.email_institucional
    usuario.telefone_institucional = dados.telefone_institucional
    usuario.ramal = dados.ramal
    usuario.sede_hierarquia = dados.sede_hierarquia
    usuario.sede_coordenadoria = dados.sede_coordenadoria
    usuario.sede_setor = dados.sede_setor
    usuario.sede_assistencia = dados.sede_assistencia
    usuario.regional_nome = dados.regional_nome
    usuario.regional_coordenadoria = dados.regional_coordenadoria
    usuario.regional_setor = dados.regional_setor
    # Atualiza senha se enviada
    if dados.senha:
        usuario.senha_hash = bcrypt.hash(dados.senha)
    try:
        db.commit()
        db.refresh(usuario)
    except IntegrityError:
        db.rollback()
        return JSONResponse(status_code=400, content={"detail": "Erro de integridade ao atualizar usuário (CPF/tipo duplicado?)"})
    return {"msg": "Usuário atualizado com sucesso", "id": usuario.id}

# ===============================
# Verificação de Duplicidade de Perfil
# ===============================
@router.get("/verificar-duplicidade")
def verificar_duplicidade_perfil(cpf: str, tipo: str, db: Session = Depends(get_db)):
    cpf_limpo = re.sub(r"\D", "", cpf)
    existe = db.query(UsuarioSistema).filter(
        UsuarioSistema.cpf == cpf_limpo,
        UsuarioSistema.tipo == tipo
    ).first()
    return {"duplicado": bool(existe)}


