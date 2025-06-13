"""
Teste específico para envio de email com PDF anexo
"""

import os
import sys
import tempfile
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.getcwd())

def criar_pdf_teste():
    """Cria um PDF de teste simples"""
    try:
        # Usando reportlab para criar um PDF simples
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Cria arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()
        
        # Cria o PDF
        c = canvas.Canvas(temp_path, pagesize=letter)
        width, height = letter
        
        # Adiciona conteúdo ao PDF
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 100, "COMPROVANTE DE CADASTRO - FAD")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 150, "Nome: Vinicius Capanema (TESTE)")
        c.drawString(100, height - 170, "Email: vpcapanema@der.sp.gov.br")
        c.drawString(100, height - 190, "Tipo: Administrador")
        c.drawString(100, height - 210, "Status: Teste de Sistema")
        
        c.drawString(100, height - 250, "Este é um PDF de teste para verificar o anexo em emails.")
        c.drawString(100, height - 270, f"Gerado em: {os.path.basename(temp_path)}")
        
        c.save()
        
        print(f"✅ PDF de teste criado: {temp_path}")
        print(f"📏 Tamanho: {os.path.getsize(temp_path)} bytes")
        
        return temp_path
        
    except ImportError:
        print("⚠️ reportlab não encontrado, criando PDF simples com texto...")
        # Fallback: cria um arquivo de texto simples
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8')
        temp_file.write("""
COMPROVANTE DE CADASTRO - FAD (TESTE)
=====================================

Nome: Vinicius Capanema (TESTE)
Email: vpcapanema@der.sp.gov.br
Tipo: Administrador
Status: Teste de Sistema

Este é um arquivo de teste para verificar anexos em emails.
""")
        temp_file.close()
        
        print(f"✅ Arquivo de teste criado: {temp_file.name}")
        return temp_file.name

def testar_email_com_anexo():
    """Testa envio de email com anexo"""
    print("🧪 TESTE DE EMAIL COM ANEXO PDF")
    print("=" * 50)
    
    try:
        # Importa o serviço de email
        from app.services.email_service import email_service
        
        # Cria PDF de teste
        caminho_pdf = criar_pdf_teste()
        
        # Dados de teste
        dados_teste = {
            'nome': 'Vinicius Capanema',
            'cpf': '123.456.789-00',
            'tipo': 'administrador',
            'email_institucional': 'vpcapanema@der.sp.gov.br',
            'instituicao': 'DER-SP',
            'status': 'Teste de Sistema'
        }
        
        print("\n📧 Enviando email de teste...")
        print(f"📍 Destinatário: vpcapanema@der.sp.gov.br")
        print(f"📎 Anexo: {os.path.basename(caminho_pdf)}")
        print(f"📏 Tamanho do anexo: {os.path.getsize(caminho_pdf)} bytes")
        
        # Envia email
        resultado = email_service.enviar_email_confirmacao_cadastro(
            destinatario_email="vpcapanema@der.sp.gov.br",
            destinatario_nome="Vinicius Capanema",
            comprovante_pdf_path=caminho_pdf,
            dados_cadastro=dados_teste,
            ip_origem="127.0.0.1",
            user_agent="TesteAnexoPDF/1.0"
        )
        
        if resultado:
            print("✅ Email enviado com sucesso!")
            print("\n📋 Verifique seu email institucional:")
            print("   - Email de confirmação de cadastro")
            print("   - Anexo PDF deve estar presente")
            print("   - Conteúdo HTML formatado")
        else:
            print("❌ Falha no envio do email")
            
        # Limpeza
        try:
            os.unlink(caminho_pdf)
            print(f"\n🗑️ Arquivo temporário removido: {os.path.basename(caminho_pdf)}")
        except:
            pass
            
        return resultado
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def verificar_configuracao_ambiente():
    """Verifica configuração do ambiente"""
    print("\n🔧 VERIFICANDO CONFIGURAÇÃO...")
    print("=" * 50)
    
    # Verifica variáveis de ambiente
    environment = os.getenv("ENVIRONMENT", "development")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    
    print(f"🌍 Ambiente: {environment}")
    print(f"📧 SMTP configurado: {'Sim' if smtp_password else 'Não'}")
    
    if environment == "production" and smtp_password:
        print("✅ Configuração para envio real de emails")
        return True
    else:
        print("⚠️ Modo desenvolvimento - emails serão simulados")
        return False

def main():
    """Função principal"""
    print("🔬 TESTE ESPECÍFICO - EMAIL COM ANEXO PDF")
    print("=" * 60)
    
    # Verifica configuração
    is_production = verificar_configuracao_ambiente()
    
    if is_production:
        print("\n⚠️ ATENÇÃO: Modo produção ativo!")
        print("   O email será enviado REALMENTE para vpcapanema@der.sp.gov.br")
        confirmacao = input("\nDeseja continuar? (s/N): ").lower().strip()
        if confirmacao != 's':
            print("❌ Teste cancelado pelo usuário")
            return
    
    # Executa teste
    resultado = testar_email_com_anexo()
    
    print("\n" + "=" * 60)
    if resultado:
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        if is_production:
            print("📧 Verifique seu email institucional para confirmar o anexo PDF")
        else:
            print("💡 Execute em modo produção para envio real")
    else:
        print("❌ TESTE FALHOU - Verifique os logs acima")
    print("=" * 60)

if __name__ == "__main__":
    main()
