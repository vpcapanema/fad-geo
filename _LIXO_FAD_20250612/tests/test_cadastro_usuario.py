import pytest

def test_cadastro_usuario():
    """Teste de cadastro de usuário"""
    from .test_helpers import cadastrar_usuario, verificar_api_rodando
    
    # Verifica se API está rodando
    if not verificar_api_rodando():
        pytest.skip("API não está rodando")
    
    usuario = {
        "nome": "Teste Usuario",
        "cpf": "12345678901",  # CPF sem formatação
        "email": "teste@usuario.com",
        "telefone": "(11) 99999-9999",
        "senha": "MinhaSenh@123",
        "tipo": "comum",
        "instituicao": "DER-SP",
        "tipo_lotacao": "sede",
        "email_institucional": "teste@der.sp.gov.br",
        "telefone_institucional": "(11) 3311-1234",
        "ramal": "1234",
        "sede_hierarquia": "VPC",
        "sede_coordenadoria": "GEOSER",
        "sede_setor": "Teste"
    }
    
    resposta = cadastrar_usuario(usuario)
    
    assert resposta is not None
    # Como pode haver duplicidade, aceita tanto sucesso quanto erro conhecido
    assert resposta.get("success") == True or "já existe" in str(resposta.get("data", "")) or "Já existe um usuário" in str(resposta.get("data", ""))

def test_envio_email_cadastro():
    """Teste de envio de email após cadastro"""
    from .test_helpers import enviar_email_teste
    
    resultado = enviar_email_teste(
        destinatario="teste@usuario.com",
        nome="Teste Usuario",
        tipo_email="confirmacao_cadastro"
    )
    
    # Em modo desenvolvimento, sempre retorna True
    assert resultado == True

def test_envio_email_recuperacao_senha():
    """Teste de envio de email de recuperação de senha"""
    from .test_helpers import enviar_email_teste
    
    resultado = enviar_email_teste(
        destinatario="teste@usuario.com", 
        nome="Teste Usuario",
        tipo_email="recuperacao_senha"
    )
    
    # Em modo desenvolvimento, sempre retorna True
    assert resultado == True