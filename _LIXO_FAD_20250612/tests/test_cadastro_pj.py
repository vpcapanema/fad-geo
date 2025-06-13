import pytest

def test_cadastro_pj():
    """Teste de cadastro de pessoa jurídica"""
    from .test_helpers import cadastrar_pj, verificar_api_rodando
    
    # Verifica se API está rodando
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    dados_pj = {
        "razao_social": "Empresa Teste Ltda",
        "cnpj": "12345678000195",  # CNPJ sem formatação
        "nome_fantasia": "Teste Ltda",
        "telefone": "(11) 1234-5678",  # Mudança de telefone_institucional para telefone
        "email": "teste@empresa.com",
        "cep": "01310-100",
        "rua": "Av. Paulista",
        "numero": "1000",
        "complemento": "Sala 100",
        "bairro": "Bela Vista",
        "uf": "SP",
        "cidade": "São Paulo"
    }
    
    resposta = cadastrar_pj(dados_pj)
    
    assert resposta is not None
    # Como pode haver duplicidade, aceita tanto sucesso quanto erro de duplicação
    assert resposta.get("success") == True or "já cadastrado" in str(resposta.get("data", ""))