"""
Funções auxiliares para os testes do sistema FAD
"""

import requests
import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.email_service import email_service
from app.database.session import get_db
from app.models.cd_usuario_sistema import UsuarioSistema
from app.models.cd_pessoa_fisica import PessoaFisica
from app.models.cd_pessoa_juridica import PessoaJuridica

# URL base da API
BASE_URL = "http://localhost:8000"

def cadastrar_pj(dados_pj):
    """Wrapper para cadastro de pessoa jurídica"""
    try:
        response = requests.post(
            f"{BASE_URL}/cadastro/pessoa-juridica",
            json=dados_pj,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        return {
            'success': response.status_code in [200, 201],  # Aceita tanto 200 quanto 201
            'status_code': response.status_code,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def cadastrar_usuario(usuario_data):
    """Wrapper para cadastro de usuário"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/cd/cadastro-usuario-sistema",
            json=usuario_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        return {
            'success': response.status_code == 200,
            'status_code': response.status_code,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def cadastrar_elemento_rodoviario(dados):
    """Wrapper para cadastro de elementos rodoviários"""
    try:
        response = requests.post(
            f"{BASE_URL}/elementos/trecho",  # Endpoint correto sem prefix
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        return {
            'success': response.status_code in [200, 201],  # Aceita tanto 200 quanto 201
            'status_code': response.status_code,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def recuperar_senha(email):
    """Wrapper para recuperação de senha"""
    try:
        response = requests.post(
            f"{BASE_URL}/recuperacao/solicitar",
            data={'email': email},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=30
        )
        return {
            'success': response.status_code == 200,
            'status_code': response.status_code,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def verificar_api_rodando():
    """Verifica se a API está rodando"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def enviar_email_teste(destinatario, nome, tipo_email="teste"):
    """Wrapper para envio de email de teste"""
    try:
        if tipo_email == "confirmacao_cadastro":
            return email_service.enviar_email_confirmacao_cadastro(
                destinatario_email=destinatario,
                destinatario_nome=nome,
                comprovante_pdf_path=None,
                dados_cadastro={
                    'nome': nome,
                    'tipo': 'teste',
                    'status': 'teste'
                }
            )
        if tipo_email == "recuperacao_senha":
            return email_service.enviar_email_recuperacao_senha(
                destinatario_email=destinatario,
                destinatario_nome=nome,
                token_recuperacao="token_teste_12345"
            )
        else:
            return False
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False
