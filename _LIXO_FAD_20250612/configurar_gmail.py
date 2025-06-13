#!/usr/bin/env python3
"""
Guia para configurar senha de aplicativo do Gmail
"""

def mostrar_guia_gmail():
    print("🔧 CONFIGURAÇÃO DE SENHA DE APLICATIVO GMAIL")
    print("=" * 60)
    print()
    print("❗ PROBLEMA DETECTADO:")
    print("   O Gmail não permite mais usar a senha normal da conta")
    print("   para aplicações de terceiros. É necessário usar uma")
    print("   'senha de aplicativo' específica.")
    print()
    print("📋 PASSO A PASSO PARA RESOLVER:")
    print()
    print("1️⃣  ATIVAR VERIFICAÇÃO EM 2 ETAPAS")
    print("   - Acesse: https://myaccount.google.com/security")
    print("   - Clique em 'Verificação em 2 etapas'")
    print("   - Siga as instruções para ativar")
    print()
    print("2️⃣  GERAR SENHA DE APLICATIVO")
    print("   - Acesse: https://myaccount.google.com/apppasswords")
    print("   - Selecione 'Email' como aplicativo")
    print("   - Selecione 'Outro (nome personalizado)' como dispositivo")
    print("   - Digite: 'FAD Sistema Recuperacao'")
    print("   - Clique em 'Gerar'")
    print()
    print("3️⃣  COPIAR A SENHA GERADA")
    print("   - O Gmail mostrará uma senha de 16 caracteres")
    print("   - Exemplo: 'abcd efgh ijkl mnop'")
    print("   - COPIE esta senha (sem os espaços)")
    print()
    print("4️⃣  ATUALIZAR O ARQUIVO .env")
    print("   - Abra o arquivo .env na pasta do projeto")
    print("   - Substitua a linha:")
    print("     SMTP_PASSWORD=Malditas131533*")
    print("   - Por:")
    print("     SMTP_PASSWORD=abcdefghijklmnop")
    print("   - (use a senha de aplicativo que você copiou)")
    print()
    print("5️⃣  REINICIAR O SISTEMA")
    print("   - Execute: python testar_recuperacao_senha.py")
    print("   - Deve funcionar corretamente agora!")
    print()
    print("💡 DICAS IMPORTANTES:")
    print("   - A senha de aplicativo tem 16 caracteres")
    print("   - NÃO use espaços no arquivo .env")
    print("   - Se não funcionar, gere uma nova senha de aplicativo")
    print("   - Cada aplicativo deve ter sua própria senha")
    print()
    print("🔗 LINKS ÚTEIS:")
    print("   Segurança da conta: https://myaccount.google.com/security")
    print("   Senhas de app:      https://myaccount.google.com/apppasswords")
    print("   Suporte Google:     https://support.google.com/accounts/answer/185833")
    print()
    print("=" * 60)

def verificar_configuracao_atual():
    print("🔍 VERIFICANDO CONFIGURAÇÃO ATUAL")
    print("=" * 60)
    
    import os
    from pathlib import Path
    
    env_file = Path("c:/Users/vinic/fad-geo/.env")
    
    if env_file.exists():
        print("✅ Arquivo .env encontrado")
        
        with open(env_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            if line.startswith("SMTP_PASSWORD="):
                password = line.split("=", 1)[1].strip()
                print(f"📧 Senha atual: {password}")
                
                if len(password) == 16 and password.isalnum():
                    print("✅ Formato parece ser senha de aplicativo (16 caracteres)")
                elif password == "Malditas131533*":
                    print("❌ Ainda usando senha normal - precisa ser senha de aplicativo")
                else:
                    print("⚠️  Formato não reconhecido - verifique se é senha de aplicativo")
                break
        else:
            print("❌ SMTP_PASSWORD não encontrado no .env")
    else:
        print("❌ Arquivo .env não encontrado")
    
    print()

def main():
    print("🚀 ASSISTENTE DE CONFIGURAÇÃO EMAIL FAD")
    print()
    
    verificar_configuracao_atual()
    mostrar_guia_gmail()
    
    print("⌨️  PRÓXIMOS PASSOS:")
    print("1. Siga o guia acima para configurar a senha de aplicativo")
    print("2. Execute: python testar_recuperacao_senha.py")
    print("3. Se funcionar, teste a recuperação via interface web!")
    print()

if __name__ == "__main__":
    main()
