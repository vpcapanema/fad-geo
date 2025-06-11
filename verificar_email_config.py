#!/usr/bin/env python3
"""
Teste de configuração de email - apenas para verificar se funciona
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
sys.path.append(str(Path(__file__).parent))

from app.services.email_service import email_service

def testar_conexao_email():
    """Testa apenas a conexão SMTP"""
    print("📧 TESTANDO CONFIGURAÇÃO DE EMAIL")
    print("=" * 50)
    
    print(f"SMTP Server: {email_service.smtp_server}")
    print(f"SMTP Port: {email_service.smtp_port}")
    print(f"SMTP Username: {email_service.smtp_username}")
    print(f"From Email: {email_service.from_email}")
    print(f"From Name: {email_service.from_name}")
    
    # Verifica se a senha está configurada
    if email_service.smtp_password and len(email_service.smtp_password) > 10:
        print("✅ Senha de aplicativo configurada")
        
        # Testa a conexão
        try:
            print("🔄 Testando conexão SMTP...")
            resultado = email_service.testar_configuracao()
            if resultado:
                print("✅ CONEXÃO SMTP FUNCIONANDO!")
                print("🎉 O sistema está pronto para enviar emails reais!")
                return True
            else:
                print("❌ Falha na conexão SMTP")
                return False
        except Exception as e:
            print(f"❌ Erro na conexão SMTP: {e}")
            return False
    else:
        print("❌ Senha não configurada corretamente")
        return False

def main():
    print("🔧 VERIFICAÇÃO DE CONFIGURAÇÃO DE EMAIL FAD")
    print()
    
    if testar_conexao_email():
        print("\n✅ CONFIGURAÇÃO CONCLUÍDA!")
        print("📋 PRÓXIMOS PASSOS:")
        print("1. Acesse: http://127.0.0.1:8000/recuperacao/solicitar")
        print("2. Digite seu email: vpcapanema@der.sp.gov.br")
        print("3. Selecione tipo: master")
        print("4. O sistema enviará o email para sua caixa de entrada!")
        print("5. Verifique seu email e clique no link recebido")
    else:
        print("\n❌ CONFIGURAÇÃO COM PROBLEMAS")
        print("Verifique as credenciais do Gmail.")

if __name__ == "__main__":
    main()
