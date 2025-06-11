import pytest

def test_elementos_rodoviarios():
    """Teste de cadastro de elementos rodoviários"""
    from .test_helpers import cadastrar_elemento_rodoviario, verificar_api_rodando
    
    # Verifica se API está rodando
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados = {
        "codigo": "SP-088",  # Formato correto para o endpoint
        "denominacao": "Rodovia dos Tamoios", 
        "municipio": "São José dos Campos",
        "extensao": "100",
        "tipo": "rodovia"
    }
    
    resposta = cadastrar_elemento_rodoviario(dados)
    
    assert resposta is not None
    # Aceita sucesso ou erro de duplicação
    assert resposta.get("success") == True or "já cadastrado" in str(resposta.get("data", ""))