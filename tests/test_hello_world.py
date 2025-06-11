import pytest
from .test_helpers import verificar_api_rodando

def test_hello_world():
    """Teste básico para verificar se o sistema de testes está funcionando"""
    assert True
    print("✅ Hello World - Sistema de testes funcionando!")

def test_api_conectividade():
    """Testa se a API está acessível"""
    if verificar_api_rodando():
        print("✅ API está rodando e acessível")
        assert True
    else:
        pytest.skip("API não está rodando - inicie com 'python main.py' ou execute a task 'Iniciar API FastAPI'")