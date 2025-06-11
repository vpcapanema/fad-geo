import pytest
from .test_helpers import verificar_api_rodando
import requests
import json

def test_rodovia_cadastrar():
    """Teste de cadastro de rodovia"""
    # Verifica se API está rodando
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados = {
        "codigo": "SP-200",
        "denominacao": "Rodovia Teste SP-200",
        "tipo": "estadual",
        "municipio": "São Paulo",
        "extensao_km": 120.5
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/rodovia/cadastrar",
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
            assert "já existe" in data.get("detail", "").lower() or "cadastrada" in data.get("detail", "").lower()
            
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_rodovia_listar():
    """Teste de listagem de rodovias"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    try:
        response = requests.get(
            "http://localhost:8000/api/cd/rodovia/listar",
            timeout=30
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data.get("success") == True
        assert "data" in data
        assert isinstance(data["data"], list)
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_rodovia_validacao_codigo_obrigatorio():
    """Teste de validação do código obrigatório"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "denominacao": "Rodovia Teste",
        "tipo": "estadual",
        "municipio": "São Paulo"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/rodovia/cadastrar",
            json=dados_invalidos,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        assert response.status_code in [400, 422]  # Validation error
        data = response.json()
        assert "codigo" in str(data).lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_rodovia_validacao_denominacao_obrigatoria():
    """Teste de validação da denominação obrigatória"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "codigo": "SP-201",
        "tipo": "estadual",
        "municipio": "São Paulo"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/rodovia/cadastrar",
            json=dados_invalidos,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        assert response.status_code in [400, 422]  # Validation error
        data = response.json()
        assert "denominacao" in str(data).lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_rodovia_validacao_extensao_negativa():
    """Teste de validação da extensão negativa"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_invalidos = {
        "codigo": "SP-202",
        "denominacao": "Rodovia Teste",
        "tipo": "estadual",
        "municipio": "São Paulo",
        "extensao_km": -10.0  # Valor negativo
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/rodovia/cadastrar",
            json=dados_invalidos,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "extensão" in data.get("detail", "").lower()
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_rodovia_cadastrar_campos_opcionais():
    """Teste de cadastro com campos obrigatórios mínimos"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados = {
        "codigo": "SP-203",
        "denominacao": "Rodovia Mínima",
        "municipio": "São Paulo"  # Campo obrigatório conforme erro da API
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/cd/rodovia/cadastrar",
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
        elif response.status_code == 400:
            data = response.json()
            assert "já existe" in data.get("detail", "").lower() or "cadastrada" in data.get("detail", "").lower()
            
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")

def test_rodovia_codigo_unico():
    """Teste de unicidade do código"""
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados = {
        "codigo": "SP-999",
        "denominacao": "Rodovia Teste Duplicata",
        "municipio": "São Paulo"
    }
    
    try:
        # Primeira tentativa
        response1 = requests.post(
            "http://localhost:8000/api/cd/rodovia/cadastrar",
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        # Segunda tentativa com mesmo código
        response2 = requests.post(
            "http://localhost:8000/api/cd/rodovia/cadastrar",
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        # Uma deve ser sucesso, outra deve falhar
        assert (response1.status_code == 201 and response2.status_code == 400) or \
               (response1.status_code == 400 and response2.status_code == 400)
        
    except Exception as e:
        pytest.fail(f"Erro na requisição: {e}")
