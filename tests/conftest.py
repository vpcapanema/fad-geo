import pytest

@pytest.fixture(scope='session')
def setup_database():
    # Configuração do banco de dados para os testes
    pass

@pytest.fixture(scope='session')
def setup_email_service():
    # Configuração do serviço de e-mail para os testes
    pass

@pytest.fixture(autouse=True)
def run_around_tests(setup_database, setup_email_service):
    # Código que será executado antes e depois de cada teste
    pass