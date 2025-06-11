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
    tags=['Cadastro de Usuário']
)

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
            f.write(html_content)        # Converter HTML para PDF
        # Tenta primeiro com pdfkit (se wkhtmltopdf estiver instalado)
        # Senão, usa reportlab como alternativa
        import pdfkit
        nome_arquivo_pdf = nome_arquivo_html.replace('.html', '.pdf')
        caminho_pdf = os.path.join(caminho_pasta, nome_arquivo_pdf)
        
        pdf_gerado = False
        
        try:
            # Tenta gerar PDF com pdfkit/wkhtmltopdf
            pdfkit.from_file(caminho_html, caminho_pdf)
            pdf_gerado = True
            print(f"✅ PDF gerado com wkhtmltopdf: {caminho_pdf}")
        except Exception as e:
            print(f"⚠️  wkhtmltopdf falhou: {e}")
            print("🔄 Tentando com reportlab...")
            
            # Fallback: usa reportlab
            from app.services.email_service import gerar_comprovante_cadastro_pdf_reportlab
            
            dados_para_pdf = {
                'nome': usuario.nome,
                'cpf': usuario.cpf,
                'tipo': usuario.tipo,
                'email': usuario.email,
                'email_institucional': usuario.email_institucional,
                'telefone': usuario.telefone,
                'telefone_institucional': usuario.telefone_institucional,
                'instituicao': usuario.instituicao,
                'ramal': usuario.ramal,
                'tipo_lotacao': usuario.tipo_lotacao,
                'status': 'Cadastrado - Aguardando Aprovação'
            }
            
            # Adiciona dados específicos de sede/regional conforme o tipo
            if usuario.tipo_lotacao == 'sede' and hasattr(usuario, 'sede_hierarquia'):
                dados_para_pdf.update({
                    'sede_hierarquia': usuario.sede_hierarquia,
                    'sede_coordenadoria': usuario.sede_coordenadoria,
                    'sede_setor': usuario.sede_setor
                })
            elif usuario.tipo_lotacao == 'regional' and hasattr(usuario, 'regional_nome'):
                dados_para_pdf.update({
                    'regional_nome': usuario.regional_nome,
                    'regional_coordenadoria': usuario.regional_coordenadoria,
                    'regional_setor': usuario.regional_setor
                })
            
            pdf_gerado = gerar_comprovante_cadastro_pdf_reportlab(dados_para_pdf, caminho_pdf)
            
            if pdf_gerado:
                print(f"✅ PDF gerado com reportlab: {caminho_pdf}")
            else:
                print("❌ Falha ao gerar PDF com reportlab")
        
        # Só continua se o PDF foi gerado com sucesso
        if not pdf_gerado:
            raise HTTPException(
                status_code=500, 
                detail="Erro ao gerar comprovante PDF. Entre em contato com o suporte."
            )# Enviar e-mail com PDF em anexo usando o serviço configurado
        from app.services.email_service import email_service
        
        # Prepara o email de confirmação
        email_enviado = email_service.enviar_email_confirmacao_cadastro(
            destinatario_email=usuario.email_institucional,
            destinatario_nome=usuario.nome,
            comprovante_pdf_path=caminho_pdf,
            dados_cadastro={
                'nome': usuario.nome,
                'cpf': usuario.cpf,
                'tipo': usuario.tipo,
                'email_institucional': usuario.email_institucional,
                'instituicao': usuario.instituicao,
                'status': 'Cadastrado - Aguardando Aprovação'
            },
            ip_origem=request.client.host,
            user_agent=request.headers.get("user-agent", "Desconhecido")
        )
          # Define data de envio baseada no sucesso
        if email_enviado:
            data_envio_email = datetime.now()
        else:
            data_envio_email = None
            logging.warning("Falha no envio do email de confirmação de cadastro")

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

# ===============================
# Endpoint JSON para cadastro via JavaScript
# ===============================
@router.post("/cadastro-usuario-sistema")
async def cadastrar_usuario_json(request: Request, usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Endpoint para cadastro de usuário via JSON (usado pelo JavaScript do frontend)
    """
    from datetime import datetime
    import os
    
    log_requisicao(request, "INÍCIO", f"Cadastro JSON para: {usuario_data.nome}")
    
    try:
        # Verifica se o tipo de usuário é 'master'
        if usuario_data.tipo == "master":
            raise HTTPException(
                status_code=400,
                detail="O tipo de usuário 'master' só pode ser criado pela equipe técnica da FAD."
            )
        
        # Normaliza o CPF
        cpf_limpo = re.sub(r"\D", "", usuario_data.cpf)
        
        # Verifica duplicidade
        usuario_existente = db.query(UsuarioSistema).filter(
            UsuarioSistema.cpf == cpf_limpo,
            UsuarioSistema.tipo == usuario_data.tipo
        ).first()
        
        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail=f"Já existe um usuário {usuario_data.tipo} cadastrado com este CPF."
            )
        
        # Validações de formato
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        telefone_regex = r"^\(\d{2}\) \d{4,5}-\d{4}$"
        cpf_regex = r"^\d{11}$"
        ramal_regex = r"^\d{4,}$"
        
        if not re.match(email_regex, usuario_data.email):
            raise HTTPException(status_code=400, detail="E-mail pessoal inválido.")
        
        if not re.match(email_regex, usuario_data.email_institucional):
            raise HTTPException(status_code=400, detail="E-mail institucional inválido.")
            
        if not re.match(telefone_regex, usuario_data.telefone):
            raise HTTPException(status_code=400, detail="Telefone pessoal inválido.")
            
        if not re.match(telefone_regex, usuario_data.telefone_institucional):
            raise HTTPException(status_code=400, detail="Telefone institucional inválido.")
            
        if not re.match(cpf_regex, cpf_limpo):
            raise HTTPException(status_code=400, detail="CPF inválido.")
            
        if not re.match(ramal_regex, usuario_data.ramal):
            raise HTTPException(status_code=400, detail="Ramal inválido.")
        
        # Criação do novo usuário
        novo_usuario = UsuarioSistema(
            nome=usuario_data.nome,
            cpf=cpf_limpo,
            email=usuario_data.email,
            telefone=usuario_data.telefone,
            senha_hash=bcrypt.hash(usuario_data.senha),
            tipo=usuario_data.tipo,
            pessoa_fisica_id=getattr(usuario_data, 'pessoa_fisica_id', None),
            status="aguardando_aprovacao",
            ativo=False,
            instituicao=usuario_data.instituicao,
            tipo_lotacao=usuario_data.tipo_lotacao,
            email_institucional=usuario_data.email_institucional,
            telefone_institucional=usuario_data.telefone_institucional,
            ramal=usuario_data.ramal,
            sede_hierarquia=getattr(usuario_data, 'sede_hierarquia', None),
            sede_coordenadoria=getattr(usuario_data, 'sede_coordenadoria', None),
            sede_setor=getattr(usuario_data, 'sede_setor', None),
            sede_assistencia=getattr(usuario_data, 'sede_assistencia', None),
            regional_nome=getattr(usuario_data, 'regional_nome', None),
            regional_coordenadoria=getattr(usuario_data, 'regional_coordenadoria', None),
            regional_setor=getattr(usuario_data, 'regional_setor', None)
        )
        
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        
        # Geração do comprovante HTML
        pessoa_fisica = db.query(PessoaFisica).filter(PessoaFisica.id == novo_usuario.pessoa_fisica_id).first() if novo_usuario.pessoa_fisica_id else None
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Comprovante de Cadastro</title></head>
        <body>
            <h1>FAD - Comprovante de Cadastro</h1>
            <h2>Dados do Usuário</h2>
            <p><strong>Nome:</strong> {novo_usuario.nome}</p>
            <p><strong>CPF:</strong> {novo_usuario.cpf}</p>
            <p><strong>Tipo:</strong> {novo_usuario.tipo}</p>
            <p><strong>Email:</strong> {novo_usuario.email}</p>
            <p><strong>Email Institucional:</strong> {novo_usuario.email_institucional}</p>
            <p><strong>Telefone:</strong> {novo_usuario.telefone}</p>
            <p><strong>Instituição:</strong> {novo_usuario.instituicao}</p>
            <p><strong>Status:</strong> Aguardando Aprovação</p>
            <p><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </body>
        </html>
        """
        
        # Criação de diretórios
        base_dir = os.path.join("downloads", "usuarios", "comprovantes_cadastro")
        os.makedirs(base_dir, exist_ok=True)
        pasta_usuario = f"usuario_{novo_usuario.id:04d}_{datetime.now().strftime('%Y%m%d')}"
        caminho_pasta = os.path.join(base_dir, pasta_usuario)
        os.makedirs(caminho_pasta, exist_ok=True)
        
        # Gera HTML temporário
        nome_arquivo_html = f"cadastro_usuario_{novo_usuario.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_v1.html"
        caminho_html = os.path.join(caminho_pasta, nome_arquivo_html)
        with open(caminho_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Gera PDF
        nome_arquivo_pdf = nome_arquivo_html.replace('.html', '.pdf')
        caminho_pdf = os.path.join(caminho_pasta, nome_arquivo_pdf)
        
        pdf_gerado = False
        
        try:
            # Tenta gerar PDF com pdfkit/wkhtmltopdf
            import pdfkit
            pdfkit.from_file(caminho_html, caminho_pdf)
            pdf_gerado = True
            print(f"✅ PDF gerado com wkhtmltopdf: {caminho_pdf}")
        except Exception as e:
            print(f"⚠️  wkhtmltopdf falhou: {e}")
            print("🔄 Tentando com reportlab...")
            
            # Fallback: usa reportlab
            from app.services.email_service import gerar_comprovante_cadastro_pdf_reportlab
            
            dados_para_pdf = {
                'nome': novo_usuario.nome,
                'cpf': novo_usuario.cpf,
                'tipo': novo_usuario.tipo,
                'email': novo_usuario.email,
                'email_institucional': novo_usuario.email_institucional,
                'telefone': novo_usuario.telefone,
                'telefone_institucional': novo_usuario.telefone_institucional,
                'instituicao': novo_usuario.instituicao,
                'ramal': novo_usuario.ramal,
                'tipo_lotacao': novo_usuario.tipo_lotacao,
                'status': 'Cadastrado - Aguardando Aprovação'
            }
            
            # Adiciona dados específicos conforme o tipo de lotação
            if novo_usuario.tipo_lotacao == 'sede':
                dados_para_pdf.update({
                    'sede_hierarquia': novo_usuario.sede_hierarquia,
                    'sede_coordenadoria': novo_usuario.sede_coordenadoria,
                    'sede_setor': novo_usuario.sede_setor
                })
            elif novo_usuario.tipo_lotacao == 'regional':
                dados_para_pdf.update({
                    'regional_nome': novo_usuario.regional_nome,
                    'regional_coordenadoria': novo_usuario.regional_coordenadoria,
                    'regional_setor': novo_usuario.regional_setor
                })
            
            pdf_gerado = gerar_comprovante_cadastro_pdf_reportlab(dados_para_pdf, caminho_pdf)
            
            if pdf_gerado:
                print(f"✅ PDF gerado com reportlab: {caminho_pdf}")
            else:
                print("❌ Falha ao gerar PDF com reportlab")
        
        if not pdf_gerado:
            raise HTTPException(
                status_code=500, 
                detail="Erro ao gerar comprovante PDF. Entre em contato com o suporte."
            )
        
        # Envio de email
        from app.services.email_service import email_service
        
        email_enviado = email_service.enviar_email_confirmacao_cadastro(
            destinatario_email=novo_usuario.email_institucional,
            destinatario_nome=novo_usuario.nome,
            comprovante_pdf_path=caminho_pdf,
            dados_cadastro={
                'nome': novo_usuario.nome,
                'cpf': novo_usuario.cpf,
                'tipo': novo_usuario.tipo,
                'email_institucional': novo_usuario.email_institucional,
                'instituicao': novo_usuario.instituicao,
                'status': 'Cadastrado - Aguardando Aprovação'
            },
            ip_origem=request.client.host,
            user_agent=request.headers.get("user-agent", "Desconhecido")
        )
        
        # Registra na tabela de controle
        data_envio_email = datetime.now() if email_enviado else None
        if not email_enviado:
            logging.warning("Falha no envio do email de confirmação de cadastro")
        
        db.execute(
            """
            INSERT INTO formularios_usuario (usuario_id, arquivo_nome, caminho_completo, data_geracao, versao, ativo, tamanho_arquivo, status, data_envio_email)
            VALUES (:usuario_id, :arquivo_nome, :caminho_completo, :data_geracao, :versao, :ativo, :tamanho_arquivo, :status, :data_envio_email)
            """,
            {
                'usuario_id': novo_usuario.id,
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
        
        log_requisicao(request, "FIM", f"Usuário {novo_usuario.id} cadastrado com sucesso")
        
        return JSONResponse(
            status_code=201,
            content={
                "id": novo_usuario.id,
                "nome": novo_usuario.nome,
                "status": "Cadastrado com sucesso",
                "email_enviado": email_enviado,
                "comprovante_gerado": pdf_gerado,
                "caminho_pdf": caminho_pdf
            }
        )
        
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Erro ao cadastrar: dados duplicados ou inválidos."
        )
    except Exception as e:
        db.rollback()
        log_requisicao(request, "ERRO", f"Erro inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

# ===============================
# Endpoint temporário para teste - aceita dados raw
# ===============================
@router.post("/teste-cadastro-simples")
async def teste_cadastro_simples(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint temporário para testar cadastro sem validação Pydantic
    """
    try:
        # Recebe dados como JSON raw
        dados_raw = await request.json()
        
        log_requisicao(request, "INÍCIO", f"Teste cadastro simples: {dados_raw.get('nome', 'N/A')}")
        
        # Extrai e limpa CPF
        cpf_original = dados_raw.get('cpf', '')
        cpf_limpo = re.sub(r"\D", "", cpf_original)
        
        print(f"🔍 CPF original: '{cpf_original}'")
        print(f"🔍 CPF limpo: '{cpf_limpo}'")
        print(f"🔍 Comprimento: {len(cpf_limpo)}")
        
        # Validações básicas
        if len(cpf_limpo) != 11:
            raise HTTPException(status_code=400, detail=f"CPF inválido: deve ter 11 dígitos. Recebido: {len(cpf_limpo)} dígitos")
        
        # Verifica duplicidade
        usuario_existente = db.query(UsuarioSistema).filter(
            UsuarioSistema.cpf == cpf_limpo,
            UsuarioSistema.tipo == dados_raw.get('tipo')
        ).first()
        
        if usuario_existente:
            raise HTTPException(status_code=400, detail="CPF já cadastrado para este tipo de usuário")
        
        # Cria usuário básico para teste
        novo_usuario = UsuarioSistema(
            nome=dados_raw.get('nome', 'Teste'),
            cpf=cpf_limpo,
            email=dados_raw.get('email', 'teste@test.com'),
            telefone=dados_raw.get('telefone', '(11) 99999-9999'),
            senha_hash=bcrypt.hash(dados_raw.get('senha', 'senha123')),
            tipo=dados_raw.get('tipo', 'administrador'),
            status="teste",
            ativo=False,
            instituicao=dados_raw.get('instituicao', 'Teste'),
            email_institucional=dados_raw.get('email_institucional', 'teste@der.sp.gov.br'),
            telefone_institucional=dados_raw.get('telefone_institucional', '(11) 3333-4444'),
            ramal=dados_raw.get('ramal', '1234'),
            tipo_lotacao=dados_raw.get('tipo_lotacao', 'sede')
        )
        
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        
        log_requisicao(request, "FIM", f"Usuário teste {novo_usuario.id} criado com sucesso")
        
        return JSONResponse(
            status_code=201,
            content={
                "id": novo_usuario.id,
                "nome": novo_usuario.nome,
                "cpf_original": cpf_original,
                "cpf_limpo": cpf_limpo,
                "status": "Teste criado com sucesso",
                "comprimento_cpf": len(cpf_limpo)
            }
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        log_requisicao(request, "ERRO", f"Erro no teste: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")


