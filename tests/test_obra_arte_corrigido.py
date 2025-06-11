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
        "extensao_m": 150.50
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

def test_obra_arte_obter_por_id():
    """Teste de obtenção de obra de arte por ID"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    try:
        # Primeiro obter lista para pegar um ID válido
        response = requests.get(
            "http://localhost:8000/api/cd/obra-arte/listar",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            obras = data.get("data", [])
            if obras:
                # Testa com ID válido
                obra_id = obras[0]["id"]
                response = requests.get(
                    f"http://localhost:8000/api/cd/obra-arte/{obra_id}",
                    timeout=30
                )
                assert response.status_code == 200
                data = response.json()
                assert data.get("id") == obra_id
        
        # Testa com ID inválido
        response = requests.get(
            "http://localhost:8000/api/cd/obra-arte/99999",
            timeout=30
        )
        assert response.status_code == 404
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_obra_arte_validacao_campos():
    """Teste de validação de campos obrigatórios"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "codigo": "",  # Campo obrigatório vazio
        "denominacao": "Teste",
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
        
        assert response.status_code == 400
        data = response.json()
        assert "código" in data.get("detail", "").lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_obra_arte_validacao_tipo():
    """Teste de validação do tipo"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "codigo": "OAE-003",
        "denominacao": "Teste",
        "tipo": "tipo_invalido",
        "municipio": "São Paulo",
        "extensao_m": 100.0
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
        assert "tipo" in data.get("detail", "").lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_obra_arte_validacao_extensao():
    """Teste de validação da extensão"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "codigo": "OAE-004",
        "denominacao": "Teste",
        "tipo": "ponte",
        "municipio": "São Paulo",
        "extensao_m": -50.0  # Valor negativo
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
