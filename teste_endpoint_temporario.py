#!/usr/bin/env python3
"""
Teste do endpoint temporário - sem validação Pydantic
"""

import requests
import json
import random

def testar_endpoint_temporario():
    """Testa o endpoint temporário que aceita qualquer formato"""
    print("🧪 TESTE ENDPOINT TEMPORÁRIO - SEM PYDANTIC")
    print("=" * 55)
    
    # Dados de teste com CPF sem formatação
    cpf_numerico = str(11111111000 + random.randint(1, 999))
    
    dados = {
        'nome': 'Teste Endpoint Temporário',
        'cpf': cpf_numerico,
        'email': 'teste.temp@example.com',
        'telefone': '(11) 99999-8888',
        'senha': 'MinhaSenh@123',
        'tipo': 'administrador',
        'instituicao': 'DER-SP',
        'tipo_lotacao': 'sede',
        'email_institucional': 'vpcapanema@der.sp.gov.br',
        'telefone_institucional': '(11) 3311-1234',
        'ramal': '1234'
    }
    
    print(f"👤 Nome: {dados['nome']}")
    print(f"🆔 CPF: {dados['cpf']} (comprimento: {len(dados['cpf'])})")
    print()
    
    url = 'http://localhost:8000/api/cd/teste-cadastro-simples'
    
    try:
        print(f"🌐 URL: {url}")
        response = requests.post(
            url,
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 201:
            resultado = response.json()
            print("✅ SUCESSO!")
            print(f"🆔 ID: {resultado.get('id')}")
            print(f"📋 CPF Original: '{resultado.get('cpf_original')}'")
            print(f"🧹 CPF Limpo: '{resultado.get('cpf_limpo')}'")
            print(f"📏 Comprimento: {resultado.get('comprimento_cpf')}")
            return True
            
        elif response.status_code == 400:
            erro = response.json()
            print(f"❌ Erro de validação: {erro.get('detail')}")
            
        elif response.status_code == 422:
            erro = response.json()
            print("❌ Erro Pydantic:")
            for detail in erro.get('detail', []):
                print(f"   • {detail}")
                
        else:
            print(f"❌ Erro {response.status_code}")
            try:
                erro = response.json()
                print(f"📄 Detalhes: {erro}")
            except:
                print(f"📄 Resposta: {response.text[:200]}...")
                
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - API não está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
        
    return False

def testar_diferentes_formatos_cpf():
    """Testa diferentes formatos de CPF"""
    print("\n🔬 TESTANDO DIFERENTES FORMATOS DE CPF")
    print("=" * 50)
    
    base_cpf = 11111111000 + random.randint(50, 99)
    
    formatos_teste = [
        str(base_cpf + 1),  # Apenas números
        f"{str(base_cpf + 2)[:3]}.{str(base_cpf + 2)[3:6]}.{str(base_cpf + 2)[6:9]}-{str(base_cpf + 2)[9:]}",  # Formatado
        f"{str(base_cpf + 3)} ",  # Com espaço
        f" {str(base_cpf + 4)}",  # Espaço no início
    ]
    
    url = 'http://localhost:8000/api/cd/teste-cadastro-simples'
    
    for i, cpf_teste in enumerate(formatos_teste, 1):
        print(f"\n🧪 Teste {i}: CPF = '{cpf_teste}'")
        
        dados = {
            'nome': f'Teste Formato {i}',
            'cpf': cpf_teste,
            'email': f'teste{i}@example.com',
            'tipo': 'administrador',
            'instituicao': 'DER-SP',
            'email_institucional': 'vpcapanema@der.sp.gov.br',
            'telefone_institucional': '(11) 3311-1234',
            'ramal': '1234'
        }
        
        try:
            response = requests.post(url, json=dados, timeout=10)
            
            if response.status_code == 201:
                resultado = response.json()
                print(f"   ✅ Sucesso - CPF limpo: '{resultado.get('cpf_limpo')}'")
            else:
                erro = response.json()
                print(f"   ❌ Erro: {erro.get('detail', 'Desconhecido')}")
                
        except Exception as e:
            print(f"   ❌ Exceção: {e}")

if __name__ == "__main__":
    # Testa endpoint temporário
    sucesso = testar_endpoint_temporario()
    
    if sucesso:
        # Se funcionou, testa diferentes formatos
        testar_diferentes_formatos_cpf()
    
    print("\n" + "=" * 55)
    if sucesso:
        print("🎉 ENDPOINT TEMPORÁRIO FUNCIONANDO!")
        print("✅ CPF sem formatação aceito corretamente")
    else:
        print("❌ PROBLEMA NO ENDPOINT TEMPORÁRIO")
        print("🔧 Verifique se a API está rodando")
    print("=" * 55)
