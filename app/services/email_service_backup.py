import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Optional, List
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_username = os.getenv("SMTP_USERNAME", "noreply@fad.sp.gov.br")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = "noreply@fad.sp.gov.br"
        self.from_name = "FAD - Plataforma de Análise Dinamizada"

    def _create_smtp_connection(self):
        """Cria conexão SMTP segura"""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            return server
        except Exception as e:
            logger.error(f"Erro ao conectar SMTP: {e}")
            raise

    def enviar_email_recuperacao_senha(
        self, 
        destinatario_email: str, 
        destinatario_nome: str, 
        token_recuperacao: str,
        base_url: str = "http://127.0.0.1:8000"
    ) -> bool:
        """
        Envia email de recuperação de senha
        
        Args:
            destinatario_email: Email do destinatário
            destinatario_nome: Nome do destinatário
            token_recuperacao: Token único para recuperação
            base_url: URL base da aplicação
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        try:
            # Modo de desenvolvimento - simula envio de email
            if not self.smtp_password or self.smtp_password == "":
                logger.info("=== MODO DESENVOLVIMENTO - EMAIL SIMULADO ===")
                logger.info(f"Para: {destinatario_email}")
                logger.info(f"Nome: {destinatario_nome}")
                logger.info(f"Link de recuperação: {base_url}/recuperacao/redefinir/{token_recuperacao}")
                logger.info("===============================================")
                return True
            
            # Link de recuperação
            link_recuperacao = f"{base_url}/recuperacao/redefinir/{token_recuperacao}"
            
            # HTML do email
            html_content = self._get_template_recuperacao_senha(
                destinatario_nome, 
                link_recuperacao
            )
            
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "🔐 Recuperação de Senha - FAD"
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = destinatario_email
            
            # Adicionar conteúdo HTML
            part_html = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(part_html)
            
            # Enviar email
            with self._create_smtp_connection() as server:
                server.send_message(msg)
                
            logger.info(f"Email de recuperação enviado para: {destinatario_email}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar email de recuperação: {e}")
            return False

    def _get_template_recuperacao_senha(self, nome_usuario: str, link_recuperacao: str) -> str:
        """Template HTML para email de recuperação de senha"""
        return f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recuperação de Senha - FAD</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f4f7f9;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #003366, #006699);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }}
        .content {{
            padding: 30px 20px;
        }}
        .greeting {{
            font-size: 18px;
            margin-bottom: 20px;
            color: #003366;
        }}
        .message {{
            margin-bottom: 30px;
            line-height: 1.8;
        }}
        .button-container {{
            text-align: center;
            margin: 30px 0;
        }}
        .recovery-button {{
            display: inline-block;
            background: #006699;
            color: white !important;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0 2px 8px rgba(0,102,153,0.3);
            transition: background-color 0.3s ease;
        }}
        .recovery-button:hover {{
            background: #005080;
        }}
        .warning {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
        }}
        .security-info {{
            background: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
            color: #0d47a1;
            font-size: 14px;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
        .logo {{
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🔐</div>
            <h1>Recuperação de Senha</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">FAD - Ferramenta de Análise Dinamizada</p>
        </div>
        
        <div class="content">
            <div class="greeting">
                Olá, <strong>{nome_usuario}</strong>!
            </div>
            
            <div class="message">
                <p>Você solicitou a recuperação de senha para sua conta na plataforma FAD.</p>
                <p>Para redefinir sua senha, clique no botão abaixo:</p>
            </div>
            
            <div class="button-container">
                <a href="{link_recuperacao}" class="recovery-button">
                    🔐 Redefinir Minha Senha
                </a>
            </div>
            
            <div class="warning">
                <strong>⚠️ Importante:</strong> Este link expira em <strong>15 minutos</strong> por motivos de segurança.
            </div>
            
            <div class="security-info">
                <strong>🛡️ Informações de Segurança:</strong><br>
                • Se você não solicitou esta recuperação, ignore este email<br>
                • Nunca compartilhe este link com outras pessoas<br>
                • O link só pode ser usado uma única vez<br>
                • Em caso de dúvidas, entre em contato conosco
            </div>
        </div>
        
        <div class="footer">
            <p><strong>FAD - Ferramenta de Análise Dinamizada</strong></p>
            <p>VPC-GEOSER | Departamento de Estradas de Rodagem do Estado de São Paulo</p>
            <p>Este é um email automático, não responda a esta mensagem.</p>
        </div>
    </div>
</body>
</html>
        """

    def testar_configuracao(self) -> bool:
        """Testa se a configuração SMTP está funcionando"""
        try:
            with self._create_smtp_connection() as server:
                logger.info("Conexão SMTP testada com sucesso!")
                return True
        except Exception as e:
            logger.error(f"Falha no teste SMTP: {e}")
            return False

# Instância global do serviço de email
email_service = EmailService()
