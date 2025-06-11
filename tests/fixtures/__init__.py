import pytest

@pytest.fixture(scope='session')
def setup_database():
    # Configuração do banco de dados para os testes
    pass

@pytest.fixture(scope='session')
def setup_email_service():
    # Configuração do serviço de e-mail para os testes
    pass