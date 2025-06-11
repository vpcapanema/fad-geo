#!/usr/bin/env python3
"""
Script para testar o endpoint diretamente
"""

import requests
import json

def testar_endpoint():
    """Testa o endpoint de elementos rodoviários"""
    
    url = "http://localhost:8000/elementos/trecho"
    dados = {
        "codigo": "SP-088",
        "denominacao": "Rodovia dos Tamoios", 
        "municipio": "São José dos Campos"
    }
    
    print(f"🌐 Fazendo POST para: {url}")
    print(f"📝 Dados: {json.dumps(dados, indent=2)}")
    
    try:
        response = requests.post(
            url,
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                data = response.json()
                print(f"📄 Response JSON: {json.dumps(data, indent=2)}")
            except:
                print(f"📄 Response Text: {response.text}")
        else:
            print(f"📄 Response Text: {response.text}")
            
        return {
            'status_code': response.status_code,
            'success': response.status_code in [200, 201],
            'data': response.text
        }
        
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return {
            'status_code': 0,
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    resultado = testar_endpoint()
    print(f"\n🎯 Resultado: {resultado}")
