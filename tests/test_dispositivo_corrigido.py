import pytest
from .test_helpers import verificar_api_rodando
import requests
import json

def test_dispositivo_cadastrar():
    """Teste de cadastro de dispositivo rodoviário"""
    # Verifica se API está rodando
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados = {
        "codigo": "SP-300",
        "denominacao": "Dispositivo Teste SP-300",
        "tipo": "viaduto",
        "municipio": "São Paulo",
        "localizacao": "KM 10 da SP-300"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/dispositivo/cadastrar",
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        # Aceita sucesso (201) ou duplicação (400 com mensagem específica)
        assert response.status_code in [201, 400]
        
        if response.status_code == 201:
            data = response.json()
            assert data.get("success") == True
            assert "id" in data
            assert data.get("codigo") == dados["codigo"]
        elif response.status_code == 400:
            data = response.json()
            assert "já existe" in data.get("detail", "").lower() or "cadastrado" in data.get("detail", "").lower()
            
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_dispositivo_listar():
    """Teste de listagem de dispositivos"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    try:
        response = requests.get(
            "http://localhost:8000/api/cd/dispositivo/listar",
            timeout=30
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data.get("success") == True
        assert "data" in data
        assert isinstance(data["data"], list)
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_dispositivo_validacao_tipo():
    """Teste de validação do tipo"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "codigo": "SP-301",
        "denominacao": "Teste",
        "tipo": "tipo_invalido",
        "municipio": "São Paulo",
        "localizacao": "KM 15"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/dispositivo/cadastrar",
            json=dados_invalidos,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "tipo" in data.get("detail", "").lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_dispositivo_validacao_codigo():
    """Teste de validação do código"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "codigo": "sp-302",  # Minúscula
        "denominacao": "Teste",
        "tipo": "ponte",
        "municipio": "São Paulo",
        "localizacao": "KM 20"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/dispositivo/cadastrar",
            json=dados_invalidos,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "código" in data.get("detail", "").lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")
