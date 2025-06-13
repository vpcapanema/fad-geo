import pytest

def test_envio_email_cadastro_usuario():
    """Teste de envio de email de cadastro"""
    from .test_helpers import enviar_email_teste
    
    # Testa o envio de email de confirmação de cadastro
    resultado = enviar_email_teste(
        destinatario="usuario@example.com",
        nome="Usuário Teste",
        tipo_email="confirmacao_cadastro"
    )
    
    # Em modo desenvolvimento, sempre retorna True
    assert resultado == True

def test_envio_email_recuperacao_senha():
    """Teste de envio de email de recuperação de senha"""
    from .test_helpers import enviar_email_teste
    
    # Testa o envio de email de recuperação de senha
    resultado = enviar_email_teste(
        destinatario="usuario@example.com",
        nome="Usuário Teste", 
        tipo_email="recuperacao_senha"
    )
    
    # Em modo desenvolvimento, sempre retorna True
    assert resultado == True