#!/usr/bin/env python3
"""
Teste para debug do problema com caminho_formulario
"""

import requests
import json
import random
import string

def gerar_cpf_valido():
    """Gera um CPF válido para teste"""
    def calcular_digito(digitos):
        soma = sum(int(digitos[i]) * (len(digitos) + 1 - i) for i in range(len(digitos)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)
    
    # Gera 9 dígitos aleatórios
    base = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    
    # Calcula primeiro dígito verificador
    primeiro_digito = calcular_digito(base)
    
    # Calcula segundo dígito verificador
    segundo_digito = calcular_digito(base + primeiro_digito)
    
    return base + primeiro_digito + segundo_digito

def gerar_telefone():
    """Gera telefone válido"""
    return f"11{''.join([str(random.randint(0, 9)) for _ in range(9)])}"

def teste_cadastro_debug():
    """Teste de cadastro com dados mínimos para debug"""
    
    cpf = gerar_cpf_valido()
    telefone = gerar_telefone()
      # Dados mínimos para cadastro
    usuario_data = {
        "pessoa_fisica_id": None,
        "nome": "Debug Test User",
        "cpf": cpf,
        "email": f"debug.test.{random.randint(1000, 9999)}@teste.com",
        "telefone": telefone,
        "senha": "MinhaSenh@123",
        "tipo": "analista",
        
        # Informações profissionais mínimas
        "instituicao": "DER/SP",
        "tipo_lotacao": "sede",
        "sede_hierarquia": "Diretoria Técnica",
        "sede_coordenadoria": "Coordenação de Projetos",
        "sede_setor": "Setor de Testes",
        "email_institucional": f"debug.institucional.{random.randint(1000, 9999)}@der.sp.gov.br",
        "telefone_institucional": telefone,
        "ramal": "1234"
    }
    
    print(f"🧪 TESTE DEBUG - Cadastrando usuário:")
    print(f"   Nome: {usuario_data['nome']}")
    print(f"   CPF: {cpf}")
    print(f"   Email: {usuario_data['email']}")
    print(f"   Tipo: {usuario_data['tipo']}")
    print()
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/cadastro-usuario-sistema",
            json=usuario_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📡 Status da resposta: {response.status_code}")
        print(f"📄 Headers da resposta: {dict(response.headers)}")
        print()
        
        try:
            response_data = response.json()
            print(f"📋 Dados da resposta:")
            for key, value in response_data.items():
                print(f"   {key}: {value}")
              # Verifica especificamente o campo formulario_html
            caminho_formulario = response_data.get('formulario_html')
            print()
            print(f"🔍 ANÁLISE DO CAMPO 'formulario_html':")
            print(f"   Valor: {caminho_formulario}")
            print(f"   Tipo: {type(caminho_formulario)}")
            print(f"   É None?: {caminho_formulario is None}")
            print(f"   É string vazia?: {caminho_formulario == ''}")
            
            if caminho_formulario and isinstance(caminho_formulario, str):
                import os
                print(f"   Arquivo existe?: {os.path.exists(caminho_formulario)}")
                if os.path.exists(caminho_formulario):
                    print(f"   Tamanho do arquivo: {os.path.getsize(caminho_formulario)} bytes")
                    
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON. Resposta raw:")
            print(response.text[:500])
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    teste_cadastro_debug()
