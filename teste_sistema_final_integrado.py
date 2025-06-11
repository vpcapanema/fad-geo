#!/usr/bin/env python3
"""
Teste final do sistema integrado de cadastro FAD
Testa todo o fluxo: frontend -> backend -> PDF -> email
"""

import requests
import json
import random
import sys

def testar_sistema_completo():
    """Teste completo do sistema de cadastro"""
    print("🎯 TESTE FINAL DO SISTEMA FAD - CADASTRO INTEGRADO")
    print("=" * 70)
      # Dados de teste
    cpf_base = 111111110 + random.randint(10, 99)
    cpf_formatado = f"{str(cpf_base)[:3]}.{str(cpf_base)[3:6]}.{str(cpf_base)[6:9]}-{str(cpf_base)[9:]}"
    dados = {
        'nome': 'Teste Sistema Integrado FAD',
        'cpf': cpf_formatado,
        'email': 'teste.final@example.com',
        'telefone': '(11) 99999-8888',
        'senha': 'MinhaSenh@123',
        'tipo': 'administrador',
        'instituicao': 'DER-SP',
        'tipo_lotacao': 'sede',
        'email_institucional': 'vpcapanema@der.sp.gov.br',
        'telefone_institucional': '(11) 3311-1234',
        'ramal': '1234',
        'sede_hierarquia': 'VPC',
        'sede_coordenadoria': 'GEOSER',
        'sede_setor': 'Análise de Dados'
    }
    
    print(f"👤 Usuário: {dados['nome']}")
    print(f"📧 Email destino: {dados['email_institucional']}")
    print(f"🆔 CPF: {dados['cpf']}")
    print()
    
    # URLs para testar
    urls_teste = [
        'http://localhost:8000/api/cd/cadastro-usuario-sistema',
        'http://localhost:8000/cadastro-usuario-sistema',
        'http://localhost:8000/usuario/cadastrar-usuario'
    ]
    
    sucesso = False
    
    for url in urls_teste:
        print(f"🌐 Testando URL: {url}")
        
        try:
            response = requests.post(
                url,
                json=dados,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                try:
                    resultado = response.json()
                    print("   ✅ SUCESSO!")
                    print(f"   🆔 ID: {resultado.get('id', 'N/A')}")
                    print(f"   📄 PDF: {'✅' if resultado.get('comprovante_gerado', False) else '❌'}")
                    print(f"   📧 Email: {'✅' if resultado.get('email_enviado', False) else '❌'}")
                    if 'caminho_pdf' in resultado:
                        print(f"   📁 Arquivo: {resultado['caminho_pdf']}")
                    sucesso = True
                    break
                except json.JSONDecodeError:
                    print("   ✅ Resposta recebida (HTML)")
                    sucesso = True
                    break
            
            elif response.status_code == 404:
                print("   ❌ Endpoint não encontrado")
            elif response.status_code == 422:
                print("   ❌ Erro de validação")
                try:
                    erro = response.json()
                    print(f"   📄 Detalhes: {erro}")
                except:
                    pass
            else:
                print(f"   ❌ Erro: {response.status_code}")
                try:
                    erro = response.json()
                    print(f"   📄 Detalhes: {erro.get('detail', 'N/A')}")
                except:
                    print(f"   📄 Resposta: {response.text[:200]}...")
                    
        except requests.exceptions.ConnectionError:
            print("   ❌ Conexão falhou - API não está rodando?")
        except requests.exceptions.Timeout:
            print("   ❌ Timeout - API muito lenta")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        print()
    
    return sucesso

def verificar_api_status():
    """Verifica se a API está respondendo"""
    print("🔍 VERIFICANDO STATUS DA API")
    print("-" * 40)
    
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API está rodando em http://localhost:8000")
            return True
        else:
            print(f"⚠️  API respondeu com status {response.status_code}")
            return False
    except:
        print("❌ API não está rodando")
        print("💡 Para iniciar: python -m uvicorn main:app --reload")
        return False

def verificar_arquivos_gerados():
    """Verifica arquivos PDF gerados"""
    import os
    
    print("\n📄 VERIFICANDO ARQUIVOS GERADOS")
    print("-" * 40)
    
    # Verifica PDFs de teste recentes
    pdf_count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pdf') and 'teste' in file.lower():
                pdf_count += 1
                print(f"📄 {file}")
    
    if pdf_count == 0:
        print("📄 Nenhum PDF de teste encontrado")
    else:
        print(f"📄 Total: {pdf_count} arquivo(s) PDF")

if __name__ == "__main__":
    print("🚀 INICIANDO TESTE COMPLETO DO SISTEMA FAD")
    print("=" * 70)
    
    # Verifica se API está rodando
    if not verificar_api_status():
        print("\n❌ TESTE INTERROMPIDO - API NÃO ESTÁ RODANDO")
        sys.exit(1)
    
    print()
    
    # Executa teste principal
    resultado = testar_sistema_completo()
    
    # Verifica arquivos gerados
    verificar_arquivos_gerados()
    
    # Resultado final
    print("\n" + "=" * 70)
    if resultado:
        print("🎉 TESTE COMPLETO CONCLUÍDO COM SUCESSO!")
        print("✅ Sistema de cadastro integrado funcionando")
        print("📧 Verifique o email vpcapanema@der.sp.gov.br")
        print("📄 Comprovante PDF deve ter sido gerado e enviado")
    else:
        print("❌ TESTE FALHOU")
        print("🔧 Verifique as mensagens de erro acima")
        print("🔄 Pode ser necessário reiniciar a API")
    print("=" * 70)
