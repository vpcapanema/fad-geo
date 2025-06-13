import pytest
from .test_helpers import verificar_api_rodando
import requests
import json

def test_obra_arte_cadastrar():
    """Teste de cadastro de obra de arte rodoviária"""
    # Verifica se API está rodando
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados = {
        "codigo": "OAE-002",
        "denominacao": "Ponte Teste OAE-002",
        "tipo": "ponte",
        "municipio": "São Paulo",
        "extensao_km": 0.15  # Convertido de metros para quilômetros
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/obra-arte/cadastrar",
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

def test_obra_arte_listar():
    """Teste de listagem de obras de arte"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    try:
        response = requests.get(
            "http://localhost:8000/api/cd/obra-arte/listar",
            timeout=30
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data.get("success") == True
        assert "data" in data
        assert isinstance(data["data"], list)
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_obra_arte_validacao_codigo_obrigatorio():
    """Teste de validação do código obrigatório"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "denominacao": "Ponte Teste",
        "tipo": "ponte",
        "municipio": "São Paulo"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/obra-arte/cadastrar",
            json=dados_invalidos,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "codigo" in str(data).lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_obra_arte_validacao_denominacao_obrigatoria():
    """Teste de validação da denominação obrigatória"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "codigo": "OAE-003",
        "tipo": "ponte",
        "municipio": "São Paulo"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/obra-arte/cadastrar",
            json=dados_invalidos,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "denominacao" in str(data).lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_obra_arte_validacao_tipo_obrigatorio():
    """Teste de validação do tipo obrigatório"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "codigo": "OAE-004",
        "denominacao": "Ponte Teste",
        "municipio": "São Paulo"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/obra-arte/cadastrar",
            json=dados_invalidos,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "tipo" in str(data).lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_obra_arte_validacao_extensao_negativa():
    """Teste de validação da extensão negativa"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "codigo": "OAE-005",
        "denominacao": "Ponte Teste",
        "tipo": "ponte",
        "municipio": "São Paulo",
        "extensao_km": -0.05  # Valor negativo
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/obra-arte/cadastrar",
            json=dados_invalidos,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "extensao" in data.get("detail", "").lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_obra_arte_cadastrar_campos_opcionais():
    """Teste de cadastro com apenas campos obrigatórios"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados = {
        "codigo": "OAE-006",
        "denominacao": "Obra Mínima",
        "tipo": "viaduto"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/obra-arte/cadastrar",
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
            assert data.get("denominacao") == dados["denominacao"]
            assert data.get("tipo") == dados["tipo"]
        elif response.status_code == 400:
            data = response.json()
            assert "já existe" in data.get("detail", "").lower() or "cadastrado" in data.get("detail", "").lower()
            
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_obra_arte_codigo_unico():
    """Teste de unicidade do código"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados = {
        "codigo": "OAE-999",
        "denominacao": "Obra Teste Duplicata",
        "tipo": "ponte"
    }
    
    try:
        # Primeira tentativa
        response1 = requests.post(
            "http://localhost:8000/api/cd/obra-arte/cadastrar",
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        # Segunda tentativa com mesmo código
        response2 = requests.post(
            "http://localhost:8000/api/cd/obra-arte/cadastrar",
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        # Uma deve ser sucesso, outra deve falhar
        assert (response1.status_code == 201 and response2.status_code == 400) or \
               (response1.status_code == 400 and response2.status_code == 400)
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")
