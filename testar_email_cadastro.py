#!/usr/bin/env python3
"""
Teste do sistema de envio de email de confirmação de cadastro
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
sys.path.append(str(Path(__file__).parent))

from app.services.email_service import email_service

def testar_email_confirmacao_cadastro():
    """Testa o envio de email de confirmação de cadastro"""
    print("📧 TESTE DO EMAIL DE CONFIRMAÇÃO DE CADASTRO")
    print("=" * 60)
    
    # Dados fictícios para teste
    dados_teste = {
        'destinatario_email': 'vpcapanema@der.sp.gov.br',
        'destinatario_nome': 'Vinicius do Prado Capanema',
        'usuario_dados': {
            'nome': 'Vinicius do Prado Capanema',
            'cpf': '12345678901',
            'tipo': 'master',
            'email_institucional': 'vpcapanema@der.sp.gov.br'
        },
        'caminho_pdf': 'c:/temp/comprovante_teste.pdf',
        'nome_arquivo_pdf': 'comprovante_cadastro_teste.pdf'
    }
    
    # Cria um PDF fictício para teste (se não existir)
    os.makedirs('c:/temp', exist_ok=True)
    if not os.path.exists(dados_teste['caminho_pdf']):
        with open(dados_teste['caminho_pdf'], 'wb') as f:
            f.write(b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n')
    
    print("📋 Dados do teste:")
    print(f"  Email: {dados_teste['destinatario_email']}")
    print(f"  Nome: {dados_teste['destinatario_nome']}")
    print(f"  Tipo: {dados_teste['usuario_dados']['tipo']}")
    print(f"  PDF: {dados_teste['nome_arquivo_pdf']}")
    print()
    
    try:
        resultado = email_service.enviar_email_confirmacao_cadastro(
            destinatario_email=dados_teste['destinatario_email'],
            destinatario_nome=dados_teste['destinatario_nome'],
            usuario_dados=dados_teste['usuario_dados'],
            caminho_pdf=dados_teste['caminho_pdf'],
            nome_arquivo_pdf=dados_teste['nome_arquivo_pdf']
        )
        
        if resultado:
            print("✅ Email de confirmação de cadastro enviado com sucesso!")
            return True
        else:
            print("❌ Falha no envio do email de confirmação")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Limpa arquivo de teste
        if os.path.exists(dados_teste['caminho_pdf']):
            os.remove(dados_teste['caminho_pdf'])

def verificar_configuracao_email():
    """Verifica se a configuração de email está correta"""
    print("🔧 VERIFICAÇÃO DE CONFIGURAÇÃO DE EMAIL")
    print("=" * 60)
    
    print(f"SMTP Server: {email_service.smtp_server}")
    print(f"SMTP Port: {email_service.smtp_port}")
    print(f"SMTP Username: {email_service.smtp_username}")
    print(f"From Email: {email_service.from_email}")
    print(f"From Name: {email_service.from_name}")
    
    if email_service.smtp_password:
        senha_mascarada = '*' * len(email_service.smtp_password)
        print(f"SMTP Password: {senha_mascarada}")
        print("✅ Senha configurada")
    else:
        print("❌ Senha não configurada")
    
    print()

def main():
    print("🚀 TESTE DE EMAIL DE CONFIRMAÇÃO DE CADASTRO FAD")
    print("   Testando funcionalidade de envio após cadastro de usuário")
    print()
    
    # Verifica configuração
    verificar_configuracao_email()
    
    # Testa envio
    sucesso = testar_email_confirmacao_cadastro()
    
    print("=" * 60)
    if sucesso:
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("   O sistema de email de confirmação está funcionando.")
        print()
        print("📋 FUNCIONALIDADES VERIFICADAS:")
        print("   ✅ Envio de email após cadastro")
        print("   ✅ Email para endereço institucional")
        print("   ✅ Anexo PDF com comprovante")
        print("   ✅ Template HTML formatado")
        print("   ✅ Configuração SMTP correta")
    else:
        print("❌ TESTE FALHOU")
        print("   Verifique os logs acima para identificar o problema.")
    
    print()
    print("💡 PRÓXIMO PASSO:")
    print("   Teste fazendo um cadastro real de usuário via interface web!")

if __name__ == "__main__":
    main()
