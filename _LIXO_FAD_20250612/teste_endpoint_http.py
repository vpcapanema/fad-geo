#!/usr/bin/env python3
"""
Teste do endpoint real de cadastro de usuário via HTTP
"""

import requests
import json
import sys
import os

def testar_endpoint_cadastro():
    """Testa o endpoint de cadastro de usuário via HTTP"""
    print("=" * 80)
    print("🌐 TESTE DO ENDPOINT REAL VIA HTTP")
    print("=" * 80)
    
    try:        # URL do endpoint (assumindo que está rodando na porta padrão 8000)
        url = "http://localhost:8000/api/cd/cadastro-usuario-sistema"
          # Dados de teste para cadastro
        dados_teste = {
            "nome": "Teste Endpoint HTTP",
            "cpf": "12345678900",  # CPF sem formatação (11 dígitos)
            "email": "teste.http@teste.com",
            "telefone": "11999999999",  # Telefone sem formatação (11 dígitos)
            "senha": "senha123",
            "tipo": "analista",
            "instituicao": "DER-SP",
            "tipo_lotacao": "sede",
            "email_institucional": "teste.http@der.sp.gov.br",
            "telefone_institucional": "1112345678",  # Telefone sem formatação (10 dígitos)
            "ramal": "5678",
            "sede_hierarquia": "Diretoria de Engenharia",
            "sede_coordenadoria": "Coordenadoria de Projetos",
            "sede_setor": "Setor de Análise"
        }
        
        print(f"📤 Fazendo requisição POST para: {url}")
        print(f"📋 Dados sendo enviados:")
        for chave, valor in dados_teste.items():
            if chave != 'senha':  # Não mostrar senha no log
                print(f"   {chave}: {valor}")
        
        # Fazer a requisição POST
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(url, json=dados_teste, headers=headers, timeout=30)
        
        print(f"\n📡 Resposta recebida:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            # Sucesso
            resposta = response.json()
            print(f"\n✅ CADASTRO REALIZADO COM SUCESSO!")
            print(f"   📋 ID do usuário: {resposta.get('id')}")
            print(f"   📋 Nome: {resposta.get('nome')}")
            print(f"   📋 Status: {resposta.get('status')}")
            print(f"   📧 Email enviado: {resposta.get('email_enviado')}")
            print(f"   📄 PDF gerado: {resposta.get('comprovante_gerado')}")
            print(f"   📄 Formulário HTML: {resposta.get('formulario_html')}")
            print(f"   📄 Caminho PDF: {resposta.get('caminho_pdf')}")              # Verifica se o campo formulario_html não está None
            caminho_formulario = resposta.get('formulario_html')
            if caminho_formulario is not None:
                print(f"\n🎉 CAMPO 'formulario_html' RETORNADO CORRETAMENTE!")
                print(f"   📁 Caminho: {caminho_formulario}")
                
                # Verifica se o arquivo existe
                if os.path.exists(caminho_formulario):
                    tamanho = os.path.getsize(caminho_formulario)
                    print(f"   ✅ Arquivo existe e tem {tamanho} bytes")
                else:
                    print(f"   ❌ Arquivo não encontrado no sistema")
            else:
                print(f"\n❌ PROBLEMA: Campo 'formulario_html' retorna None")
                return False
                
        else:
            # Erro
            print(f"\n❌ ERRO NA REQUISIÇÃO:")
            print(f"   Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERRO DE CONEXÃO:")
        print(f"   Não foi possível conectar ao servidor em {url}")
        print(f"   Verifique se a API está rodando")
        return False
        
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def verificar_servidor():
    """Verifica se o servidor está rodando"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Servidor está rodando (Status: {response.status_code})")
        return True
    except:
        print(f"❌ Servidor não está rodando em http://localhost:8000/")
        return False

if __name__ == "__main__":
    print("🔍 Verificando se o servidor está rodando...")
    if verificar_servidor():
        testar_endpoint_cadastro()
    else:
        print("\n💡 Para testar o endpoint:")
        print("   1. Inicie a API com: python main.py")
        print("   2. Execute este script novamente")
