"""
Patch para adicionar monitoramento de logs ao serviço de email
"""

import time
from typing import Self

# Definir o início do tempo de processamento no início do método
inicio_tempo = time.time()

# Adicionar ao final do método enviar_email_recuperacao_senha, antes do return True:
# Certifique-se de definir destinatario_email antes de usá-lo
destinatario_email = "email@exemplo.com"  # Substitua pelo valor correto ou obtenha dinamicamente
assunto = "Assunto do email"  # Defina o assunto apropriado aqui
tempo_processamento = int((time.time() - inicio_tempo) * 1000)
Self.registrar_log_email(
    tipo_email="recuperacao_senha",
    destinatario=destinatario_email,
    assunto=assunto,
    status="sucesso",
    tempo_processamento_ms=tempo_processamento
)
