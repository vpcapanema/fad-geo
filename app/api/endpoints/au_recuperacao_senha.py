from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
import logging
from datetime import datetime

from app.database.session import get_db
from app.models.cd_usuario_sistema import UsuarioSistema
from app.models.au_recuperacao_senha import RecuperacaoSenha
from app.services.email_service import email_service
from app.utils.password_utils import (
    validar_senha_forte,
    verificar_rate_limit_recuperacao,
    invalidar_tokens_anteriores,
    validar_email_formato,
    log_tentativa_recuperacao,
    gerar_sugestoes_senha
)
from app.security.hashing import hash_senha

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/recuperacao",
    tags=["Recuperação de Senha"]
)

templates = Jinja2Templates(directory="app/templates")

# ==================== PÁGINAS HTML ====================

@router.get("/solicitar", response_class=HTMLResponse)
def pagina_solicitar_recuperacao(request: Request):
    """Página para solicitar recuperação de senha"""
    return templates.TemplateResponse("au_recuperar_senha.html", {
        "request": request
    })

@router.get("/redefinir/{token}", response_class=HTMLResponse)
def pagina_redefinir_senha(request: Request, token: str, db: Session = Depends(get_db)):
    """Página para redefinir senha com token"""
    
    # Busca o token no banco
    recuperacao = db.query(RecuperacaoSenha).filter(
        RecuperacaoSenha.token == token
    ).first()
    
    if not recuperacao:
        return templates.TemplateResponse("au_token_invalido.html", {
            "request": request,
            "erro": "Token não encontrado"
        })
    
    if not recuperacao.is_valid:
        motivo = "expirado" if recuperacao.is_expired else "usado"
        return templates.TemplateResponse("au_token_invalido.html", {
            "request": request,
            "erro": f"Token {motivo}",
            "token_expirado": recuperacao.is_expired,
            "token_usado": recuperacao.is_used
        })
    
    # Busca dados do usuário
    usuario = db.query(UsuarioSistema).filter(
        UsuarioSistema.id == recuperacao.usuario_id
    ).first()
    
    if not usuario:
        return templates.TemplateResponse("au_token_invalido.html", {
            "request": request,
            "erro": "Usuário não encontrado"
        })
    
    # Gera sugestões de senha
    sugestoes = gerar_sugestoes_senha()
    
    return templates.TemplateResponse("au_redefinir_senha.html", {
        "request": request,
        "token": token,
        "usuario_nome": usuario.nome,
        "usuario_email": usuario.email,
        "sugestoes_senha": sugestoes
    })

@router.get("/sucesso", response_class=HTMLResponse)
def pagina_sucesso(request: Request):
    """Página de confirmação de recuperação enviada"""
    return templates.TemplateResponse("au_email_enviado.html", {
        "request": request
    })

@router.get("/email-enviado", response_class=HTMLResponse)
async def email_enviado_page(request: Request):
    """Página de confirmação de email enviado"""
    return templates.TemplateResponse("au_email_enviado.html", {"request": request})

@router.get("/senha-alterada", response_class=HTMLResponse)
async def senha_alterada_page(request: Request):
    """Página de confirmação de senha alterada"""
    return templates.TemplateResponse("au_senha_alterada.html", {"request": request})

@router.get("/token-invalido", response_class=HTMLResponse)
async def token_invalido_page(request: Request):
    """Página de token inválido ou expirado"""
    return templates.TemplateResponse("au_token_invalido.html", {"request": request})

# ==================== ENDPOINTS API ====================

@router.post("/solicitar", response_class=JSONResponse)
def solicitar_recuperacao_senha(
    request: Request,
    email: str = Form(...),
    tipo: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Processa solicitação de recuperação de senha
    """
    try:
        # Pega informações da requisição
        ip_origem = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Validações básicas
        if not validar_email_formato(email):
            log_tentativa_recuperacao(db, email, ip_origem, user_agent, False, "Email inválido")
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Formato de email inválido"}
            )
        
        if tipo not in ["analista", "coordenador", "master"]:
            log_tentativa_recuperacao(db, email, ip_origem, user_agent, False, "Tipo inválido")
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Tipo de usuário inválido"}
            )
        
        # Verifica rate limiting
        pode_tentar, tentativas_restantes = verificar_rate_limit_recuperacao(db, email)
        if not pode_tentar:
            log_tentativa_recuperacao(db, email, ip_origem, user_agent, False, "Rate limit excedido")
            return JSONResponse(
                status_code=429,
                content={
                    "success": False, 
                    "message": "Muitas tentativas. Tente novamente em 1 hora.",
                    "tentativas_restantes": tentativas_restantes
                }
            )
        
        # Busca o usuário
        usuario = db.query(UsuarioSistema).filter(
            UsuarioSistema.email == email,
            UsuarioSistema.tipo == tipo,
            UsuarioSistema.ativo == True
        ).first()
        
        if not usuario:
            # Por segurança, não revelamos se o email existe ou não
            log_tentativa_recuperacao(db, email, ip_origem, user_agent, False, "Usuário não encontrado")
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "Se o email existir, você receberá instruções para recuperação."
                }
            )
        
        if usuario.status != "aprovado":
            log_tentativa_recuperacao(db, email, ip_origem, user_agent, False, "Usuário não aprovado")
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "Se o email existir, você receberá instruções para recuperação."
                }
            )
        
        # Invalida tokens anteriores
        invalidar_tokens_anteriores(db, usuario.id)
          # Cria novo token de recuperação
        recuperacao = RecuperacaoSenha(
            usuario_id=usuario.id,
            ip_solicitacao=ip_origem,
            user_agent=user_agent
        )
        
        db.add(recuperacao)
        db.commit()
        
        # Envia email
        base_url = str(request.base_url).rstrip('/')
        email_enviado = email_service.enviar_email_recuperacao_senha(
            destinatario_email=email,
            destinatario_nome=usuario.nome,
            token_recuperacao=recuperacao.token,
            base_url=base_url
        )
        if email_enviado:
            log_tentativa_recuperacao(db, email, ip_origem, user_agent, True)
            
            # Verifica se está em modo desenvolvimento para fornecer feedback específico
            import os
            environment = os.getenv("ENVIRONMENT", "development")
            smtp_password = os.getenv("SMTP_PASSWORD", "")
            
            if (environment == "development" or 
                not smtp_password or 
                smtp_password in ["sua_senha_de_app_aqui", "DESENVOLVIMENTO", "Malditas131533*"]):
                message = "✅ MODO DESENVOLVIMENTO: Link de recuperação gerado! Verifique o console do servidor para o link direto."
            else:
                message = "📧 Instruções de recuperação enviadas para seu email institucional."
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": message,
                    "redirect": "/recuperacao/email-enviado",
                    "development_mode": environment == "development"
                }
            )
        else:
            # Se falhou o envio, remove o token
            db.delete(recuperacao)
            db.commit()
            log_tentativa_recuperacao(db, email, ip_origem, user_agent, False, "Falha no envio de email")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Erro interno. Tente novamente em alguns minutos."
                }            )
    except Exception as e:
        logger.error(f"Erro na recuperação de senha: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Erro interno do servidor: {str(e)}"}
        )

@router.post("/redefinir", response_class=JSONResponse)
def redefinir_senha(
    request: Request,
    token: str = Form(...),
    nova_senha: str = Form(...),
    confirmar_senha: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Processa redefinição de senha com token
    """
    try:
        # Pega informações da requisição
        ip_origem = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Valida se as senhas coincidem
        if nova_senha != confirmar_senha:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "As senhas não coincidem"}
            )
        
        # Valida força da senha
        senha_valida, mensagem_senha = validar_senha_forte(nova_senha)
        if not senha_valida:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": mensagem_senha}
            )
        
        # Busca o token
        recuperacao = db.query(RecuperacaoSenha).filter(
            RecuperacaoSenha.token == token
        ).first()
        
        if not recuperacao:
            logger.warning(f"Tentativa de uso de token inexistente: {token} de {ip_origem}")
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Token não encontrado"}
            )
        
        if not recuperacao.is_valid:
            motivo = "expirado" if recuperacao.is_expired else "já foi usado"
            logger.warning(f"Tentativa de uso de token inválido: {token} ({motivo}) de {ip_origem}")
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": f"Token {motivo}"}
            )
        
        # Busca o usuário
        usuario = db.query(UsuarioSistema).filter(
            UsuarioSistema.id == recuperacao.usuario_id
        ).first()
        
        if not usuario:
            logger.error(f"Usuário não encontrado para token: {token}")
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Usuário não encontrado"}
            )
        
        # Atualiza a senha
        usuario.senha_hash = hash_senha(nova_senha)
        
        # Marca token como usado
        recuperacao.marcar_como_usado()
        
        # Invalida outros tokens do usuário
        invalidar_tokens_anteriores(db, usuario.id)
        
        db.commit()
        
        logger.info(f"Senha redefinida com sucesso para usuário {usuario.email} de {ip_origem}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Senha alterada com sucesso!",
                "redirect": "/recuperacao/senha-alterada"
            }
        )
    
    except Exception as e:
        logger.error(f"Erro na redefinição de senha: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Erro interno do servidor"}
        )

@router.get("/validar-token/{token}", response_class=JSONResponse)
def validar_token_recuperacao(token: str, db: Session = Depends(get_db)):
    """
    Valida se um token de recuperação é válido
    """
    try:
        recuperacao = db.query(RecuperacaoSenha).filter(
            RecuperacaoSenha.token == token
        ).first()
        
        if not recuperacao:
            return JSONResponse(
                status_code=404,
                content={"valid": False, "reason": "not_found"}
            )
        
        if recuperacao.is_expired:
            return JSONResponse(
                status_code=400,
                content={"valid": False, "reason": "expired"}
            )
        
        if recuperacao.is_used:
            return JSONResponse(
                status_code=400,
                content={"valid": False, "reason": "used"}
            )
        
        if not recuperacao.ativo:
            return JSONResponse(
                status_code=400,
                content={"valid": False, "reason": "inactive"}
            )
        
        return JSONResponse(
            status_code=200,
            content={"valid": True}
        )
    
    except Exception as e:
        logger.error(f"Erro na validação de token: {e}")
        return JSONResponse(
            status_code=500,
            content={"valid": False, "reason": "error"}
        )
