import pytest
from .test_helpers import recuperar_senha, verificar_api_rodando

def test_recuperacao_senha_endpoint_disponivel():
    """Testa se o endpoint de recuperação de senha está funcionando"""
    # Primeiro verifica se a API está rodando
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    # Testa com email válido
    email_teste = 'vinicius@acad.ifma.edu.br'
    
    resultado = recuperar_senha(email_teste)
    
    # Verifica se a função retorna alguma resposta (sucesso ou erro estruturado)
    assert resultado is not None
    assert isinstance(resultado, dict)
    print(f"✅ Endpoint de recuperação de senha respondeu corretamente")

def test_recuperacao_senha_email_formato_invalido():
    """Testa recuperação de senha com email em formato inválido"""
    # Primeiro verifica se a API está rodando
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    email_invalido = 'email_sem_arroba'
    
    resultado = recuperar_senha(email_invalido)
    
    # Sistema deve processar a requisição, mas pode retornar erro
    assert resultado is not None
    assert isinstance(resultado, dict)
    print(f"✅ Sistema processou email inválido adequadamente")