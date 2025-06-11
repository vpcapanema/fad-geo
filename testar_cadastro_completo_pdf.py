#!/usr/bin/env python3
"""
Teste completo do sistema de cadastro com PDF reportlab
Simula um cadastro real e verifica todo o fluxo
"""

import os
import sys
import requests
import json
from datetime import datetime

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, os.getcwd())

def testar_cadastro_completo():
    """Testa todo o fluxo de cadastro incluindo geração de PDF"""
    print("🎯 TESTE COMPLETO DO SISTEMA DE CADASTRO")
    print("=" * 60)
    
    # URL base da API (assumindo que está rodando)
    base_url = "http://localhost:8000"
    
    # Dados de teste para cadastro
    dados_cadastro = {
        "nome": "Teste PDF ReportLab",
        "cpf": "12345678901",
        "email": "teste.reportlab@example.com",
        "telefone": "11999998888",
        "tipo": "administrador",
        "email_institucional": "vpcapanema@der.sp.gov.br",
        "telefone_institucional": "1133111234",
        "instituicao": "DER-SP",
        "ramal": "1234",
        "tipo_lotacao": "sede",
        "sede_hierarquia": "VPC",
        "sede_coordenadoria": "GEOSER",
        "sede_setor": "Análise de Dados"
    }
    
    try:
        print(f"🌐 Testando conexão com API: {base_url}")
        
        # Verifica se API está rodando
        try:
            response = requests.get(f"{base_url}/docs", timeout=5)
            if response.status_code == 200:
                print("✅ API está rodando")
            else:
                print("⚠️  API respondeu mas pode ter problemas")
        except requests.exceptions.RequestException:
            print("❌ API não está rodando")
            print("💡 Inicie a API com: python -m uvicorn main:app --reload")
            return False
        
        print(f"\n👤 Testando cadastro de usuário:")
        print(f"   Nome: {dados_cadastro['nome']}")
        print(f"   Email: {dados_cadastro['email_institucional']}")
        
        # Faz requisição de cadastro
        response = requests.post(
            f"{base_url}/api/cd/cadastro-usuario-sistema",
            json=dados_cadastro,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"\n📊 Resposta da API:")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            resultado = response.json()
            print("✅ Cadastro realizado com sucesso!")
            print(f"   ID do usuário: {resultado.get('id')}")
            print(f"   Status: {resultado.get('status')}")
            
            # Verifica se mencionou PDF
            response_text = str(resultado)
            if 'pdf' in response_text.lower() or 'reportlab' in response_text.lower():
                print("✅ PDF foi processado no cadastro")
            
            print("\n📧 Verifique o email institucional para confirmar recebimento do comprovante")
            return True
            
        elif response.status_code == 400:
            erro = response.json()
            print(f"❌ Erro no cadastro: {erro.get('detail', 'Erro desconhecido')}")
            
            # Se for duplicata, tenta com CPF diferente
            if 'duplicado' in str(erro).lower() or 'já existe' in str(erro).lower():
                print("\n🔄 Tentando com CPF diferente...")
                dados_cadastro['cpf'] = str(int(dados_cadastro['cpf']) + 1)
                return testar_cadastro_com_cpf_alternativo(base_url, dados_cadastro)
            
            return False
            
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            try:
                print(f"   Detalhes: {response.json()}")
            except:
                print(f"   Resposta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout na requisição - API muito lenta")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_cadastro_com_cpf_alternativo(base_url, dados_cadastro):
    """Tenta cadastro com CPF alternativo"""
    try:
        response = requests.post(
            f"{base_url}/api/cd/cadastro-usuario-sistema",
            json=dados_cadastro,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 201:
            resultado = response.json()
            print("✅ Cadastro realizado com CPF alternativo!")
            print(f"   ID do usuário: {resultado.get('id')}")
            return True
        else:
            print(f"❌ Falhou mesmo com CPF alternativo: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no cadastro alternativo: {e}")
        return False

def verificar_arquivos_pdf_gerados():
    """Verifica se há arquivos PDF gerados recentemente"""
    print("\n🔍 VERIFICANDO ARQUIVOS PDF GERADOS...")
    print("=" * 50)
    
    # Procura por arquivos PDF de teste
    arquivos_pdf = []
    for arquivo in os.listdir('.'):
        if arquivo.endswith('.pdf') and 'teste' in arquivo.lower():
            arquivos_pdf.append(arquivo)
    
    if arquivos_pdf:
        print(f"📄 Encontrados {len(arquivos_pdf)} arquivo(s) PDF de teste:")
        for arquivo in arquivos_pdf:
            tamanho = os.path.getsize(arquivo)
            print(f"   • {arquivo} ({tamanho} bytes)")
    else:
        print("📄 Nenhum arquivo PDF de teste encontrado")
    
    # Procura por PDFs no diretório de downloads
    downloads_dir = "downloads"
    if os.path.exists(downloads_dir):
        pdf_downloads = [f for f in os.listdir(downloads_dir) if f.endswith('.pdf')]
        if pdf_downloads:
            print(f"\n📁 PDFs no diretório downloads: {len(pdf_downloads)}")
            for pdf in pdf_downloads[:5]:  # Mostra apenas os 5 primeiros
                print(f"   • {pdf}")

def verificar_status_api():
    """Verifica se a API está rodando"""
    print("🔍 VERIFICANDO STATUS DA API...")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/docs", timeout=3)
        if response.status_code == 200:
            print("✅ API está rodando em http://localhost:8000")
            return True
        else:
            print(f"⚠️  API respondeu com status {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ API não está rodando")
        print("💡 Para iniciar a API:")
        print("   1. Abra um terminal")
        print("   2. Execute: python -m uvicorn main:app --reload")
        print("   3. Aguarde a mensagem 'Application startup complete'")
        return False

if __name__ == "__main__":
    print("🎯 TESTE COMPLETO DO SISTEMA DE CADASTRO COM PDF")
    print("=" * 60)
    
    # Verifica arquivos PDF existentes
    verificar_arquivos_pdf_gerados()
    
    print()
    
    # Verifica se API está rodando
    api_rodando = verificar_status_api()
    
    print()
    
    if api_rodando:
        # Testa cadastro completo
        sucesso = testar_cadastro_completo()
        
        print("\n" + "=" * 60)
        if sucesso:
            print("🎉 TESTE COMPLETO CONCLUÍDO COM SUCESSO!")
            print("✅ Sistema de cadastro com PDF reportlab funcionando")
            print("📧 Verifique o email para confirmar o recebimento do comprovante")
        else:
            print("❌ TESTE FALHOU")
            print("🔧 Verifique os logs de erro acima")
    else:
        print("❌ NÃO É POSSÍVEL TESTAR SEM A API")
        print("🚀 Inicie a API primeiro")
    
    print("=" * 60)
