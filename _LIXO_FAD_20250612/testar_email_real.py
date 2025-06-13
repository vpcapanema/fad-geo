#!/usr/bin/env python3
"""
Teste de envio real de email de recuperação com a senha de aplicativo
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
sys.path.append(str(Path(__file__).parent))

from app.services.email_service import email_service

def testar_envio_real():
    """Testa o envio real de email com a senha de aplicativo"""
    print("📧 TESTE DE ENVIO REAL DE EMAIL")
    print("=" * 60)
    
    # Configurações atuais
    print("⚙️  CONFIGURAÇÕES ATUAIS:")
    print(f"   SMTP Server: {email_service.smtp_server}")
    print(f"   SMTP Port: {email_service.smtp_port}")
    print(f"   Username: {email_service.smtp_username}")
    print(f"   From Email: {email_service.from_email}")
    print(f"   Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print()
    
    # Verifica se a senha está configurada
    if email_service.smtp_password and email_service.smtp_password != "DESENVOLVIMENTO":
        print("✅ Senha de aplicativo configurada")
    else:
        print("❌ Senha de aplicativo não configurada")
        return False
    
    # Testa a conexão SMTP
    print("\n🔧 TESTANDO CONEXÃO SMTP...")
    try:
        if email_service.testar_configuracao():
            print("✅ Conexão SMTP funcionando!")
        else:
            print("❌ Falha na conexão SMTP")
            return False
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False
    
    # Testa envio de email real
    print("\n📤 TESTANDO ENVIO DE EMAIL REAL...")
    try:
        sucesso = email_service.enviar_email_recuperacao_senha(
            destinatario_email="vpcapanema@der.sp.gov.br",
            destinatario_nome="Vinicius do Prado Capanema",
            token_recuperacao="test-token-12345",
            base_url="http://127.0.0.1:8000"
        )
        
        if sucesso:
            print("🎉 EMAIL ENVIADO COM SUCESSO!")
            print("📧 Verifique sua caixa de entrada: vpcapanema@der.sp.gov.br")
            print("📂 Se não aparecer na caixa de entrada, verifique a pasta de spam")
            return True
        else:
            print("❌ Falha no envio do email")
            return False
            
    except Exception as e:
        print(f"❌ Erro no envio: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 TESTE DE EMAIL REAL - FAD RECUPERAÇÃO")
    print("   Com senha de aplicativo: ayfe lzis jjkd pcwv")
    print("   Aplicativo: FAD-SERVIDOR")
    print()
    
    resultado = testar_envio_real()
    
    print("\n" + "=" * 60)
    if resultado:
        print("✅ CONFIGURAÇÃO FUNCIONANDO!")
        print("   O sistema agora pode enviar emails reais.")
        print("   Você pode usar a recuperação de senha normalmente.")
    else:
        print("❌ PROBLEMA NA CONFIGURAÇÃO")
        print("   Verifique os logs acima para identificar o erro.")

if __name__ == "__main__":
    main()
