#!/usr/bin/env python3
"""
Teste da geração de PDF com reportlab para FAD
Versão atualizada para testar a nova implementação
"""

import os
import sys
from datetime import datetime

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, os.getcwd())

def testar_pdf_reportlab():
    """Testa a geração de PDF com reportlab"""
    print("🧪 TESTANDO GERAÇÃO DE PDF COM REPORTLAB")
    print("=" * 60)
    
    try:
        # Importa a função de geração de PDF
        from app.services.email_service import gerar_comprovante_cadastro_pdf_reportlab
        
        # Dados de teste
        dados_usuario = {
            'nome': 'Vinícius Capanema (TESTE REPORTLAB)',
            'cpf': '123.456.789-00',
            'tipo': 'administrador',
            'email': 'vinicius.teste@email.com',
            'email_institucional': 'vpcapanema@der.sp.gov.br',
            'telefone': '(11) 99999-8888',
            'telefone_institucional': '(11) 3311-1234',
            'instituicao': 'DER-SP',
            'ramal': '1234',
            'tipo_lotacao': 'sede',
            'sede_hierarquia': 'VPC',
            'sede_coordenadoria': 'GEOSER',
            'sede_setor': 'Análise de Dados',
            'status': 'Teste de PDF com ReportLab'
        }
        
        # Caminho do arquivo de teste
        caminho_pdf = f"teste_pdf_reportlab_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        print(f"📄 Gerando PDF: {caminho_pdf}")
        print(f"👤 Usuário: {dados_usuario['nome']}")
        
        # Gera PDF
        resultado = gerar_comprovante_cadastro_pdf_reportlab(dados_usuario, caminho_pdf)
        
        if resultado and os.path.exists(caminho_pdf):
            tamanho = os.path.getsize(caminho_pdf)
            print(f"✅ PDF gerado com sucesso!")
            print(f"📁 Arquivo: {caminho_pdf}")
            print(f"📊 Tamanho: {tamanho} bytes")
            
            # Pergunta se quer testar envio por email
            testar_email = input("\n📧 Testar envio por email? (s/N): ").lower().strip()
            if testar_email == 's':
                testar_envio_email_com_pdf(caminho_pdf, dados_usuario)
            
            return True
        else:
            print("❌ Falha na geração do PDF")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_envio_email_com_pdf(caminho_pdf, dados_usuario):
    """Testa envio do PDF por email"""
    print("\n📧 TESTANDO ENVIO DE EMAIL COM PDF...")
    print("=" * 50)
    
    try:
        from app.services.email_service import email_service
        
        print(f"📄 Anexando PDF: {caminho_pdf}")
        print(f"📧 Destinatário: {dados_usuario['email_institucional']}")
        
        resultado = email_service.enviar_email_confirmacao_cadastro(
            destinatario_email=dados_usuario['email_institucional'],
            destinatario_nome=dados_usuario['nome'],
            comprovante_pdf_path=caminho_pdf,
            dados_cadastro=dados_usuario,
            ip_origem="127.0.0.1",
            user_agent="Teste PDF ReportLab"
        )
        
        if resultado:
            print("✅ Email enviado com sucesso!")
            print(f"📧 Verifique o email: {dados_usuario['email_institucional']}")
        else:
            print("❌ Falha no envio do email")
            
    except Exception as e:
        print(f"❌ Erro no envio de email: {e}")
        import traceback
        traceback.print_exc()

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 VERIFICANDO DEPENDÊNCIAS...")
    print("=" * 40)
    
    dependencias = {
        'reportlab': 'Geração de PDF',
        'email': 'Envio de emails'
    }
    
    for dep, desc in dependencias.items():
        try:
            if dep == 'reportlab':
                import reportlab
                print(f"✅ {dep}: {desc} - v{reportlab.Version}")
            elif dep == 'email':
                import email
                print(f"✅ {dep}: {desc} - OK")
        except ImportError:
            print(f"❌ {dep}: {desc} - NÃO INSTALADO")
            return False
    
    return True

if __name__ == "__main__":
    print("🎯 TESTE DE PDF COM REPORTLAB - FAD")
    print("=" * 60)
    
    # Verifica dependências
    if not verificar_dependencias():
        print("\n❌ Instale as dependências necessárias")
        sys.exit(1)
    
    print()
    
    # Testa geração de PDF
    sucesso = testar_pdf_reportlab()
    
    print("\n" + "=" * 60)
    if sucesso:
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("✅ Sistema de PDF com reportlab funcionando")
    else:
        print("❌ TESTE FALHOU")
        print("🔧 Verifique os logs de erro acima")
    print("=" * 60)
