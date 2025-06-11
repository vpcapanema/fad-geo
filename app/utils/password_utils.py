import re
from typing import Tuple, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.au_recuperacao_senha import RecuperacaoSenha

def validar_senha_forte(senha: str) -> Tuple[bool, str]:
    """
    Valida se a senha atende aos critérios de segurança
    
    Args:
        senha: Senha a ser validada
        
    Returns:
        Tuple[bool, str]: (é_válida, mensagem)
    """
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres"
    
    if len(senha) > 128:
        return False, "A senha não pode ter mais de 128 caracteres"
    
    if not re.search(r'[A-Z]', senha):
        return False, "A senha deve conter pelo menos uma letra maiúscula"
    
    if not re.search(r'[a-z]', senha):
        return False, "A senha deve conter pelo menos uma letra minúscula"
    
    if not re.search(r'\d', senha):
        return False, "A senha deve conter pelo menos um número"
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', senha):
        return False, "A senha deve conter pelo menos um caractere especial (!@#$%^&*...)"
    
    # Verifica sequências comuns
    sequencias_comuns = ['123456', 'abcdef', 'qwerty', 'password', 'senha123']
    senha_lower = senha.lower()
    for seq in sequencias_comuns:
        if seq in senha_lower:
            return False, f"A senha não pode conter sequências comuns como '{seq}'"
    
    return True, "Senha válida"

def verificar_rate_limit_recuperacao(
    db: Session, 
    email: str, 
    limite: int = 3, 
    janela_horas: int = 1
) -> Tuple[bool, int]:
    """
    Verifica se o usuário não excedeu o limite de tentativas de recuperação
    
    Args:
        db: Sessão do banco de dados
        email: Email do usuário
        limite: Número máximo de tentativas permitidas
        janela_horas: Janela de tempo em horas
        
    Returns:
        Tuple[bool, int]: (pode_tentar, tentativas_restantes)
    """
    agora = datetime.utcnow()
    inicio_janela = agora - timedelta(hours=janela_horas)
    
    # Primeiro, busca o usuário pelo email
    from app.models.cd_usuario_sistema import UsuarioSistema
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.email == email).first()
    if not usuario:
        return True, limite  # Se não existe, pode tentar
    
    # Agora conta as tentativas pelo usuario_id
    tentativas = db.query(RecuperacaoSenha).filter(
        RecuperacaoSenha.usuario_id == usuario.id,
        RecuperacaoSenha.criado_em >= inicio_janela
    ).count()
    
    pode_tentar = tentativas < limite
    tentativas_restantes = max(0, limite - tentativas)
    
    return pode_tentar, tentativas_restantes

def invalidar_tokens_anteriores(db: Session, usuario_id: int):
    """
    Invalida todos os tokens de recuperação anteriores de um usuário
    
    Args:
        db: Sessão do banco de dados
        usuario_id: ID do usuário
    """
    tokens_ativos = db.query(RecuperacaoSenha).filter(
        RecuperacaoSenha.usuario_id == usuario_id,
        RecuperacaoSenha.usado_em.is_(None)
    ).all()
    
    for token in tokens_ativos:
        token.marcar_como_usado()
    
    db.commit()

def gerar_sugestoes_senha() -> List[str]:
    """
    Gera sugestões de senhas fortes
    
    Returns:
        List[str]: Lista de sugestões de senha
    """
    import random
    import string
    
    sugestoes = []
    
    # Palavras base
    palavras = ['FAD', 'Seguro', 'Estrada', 'Dados', 'Geo', 'Analise']
    simbolos = ['!', '@', '#', '$', '%', '&', '*']
    
    for i in range(3):
        palavra = random.choice(palavras)
        numero = random.randint(10, 99)
        simbolo = random.choice(simbolos)
        
        # Variações
        if i == 0:
            senha = f"{palavra}{numero}{simbolo}"
        elif i == 1:
            senha = f"{simbolo}{palavra}{numero}"
        else:
            senha = f"{palavra.lower()}{numero}{simbolo}{random.randint(10, 99)}"
        
        sugestoes.append(senha)
    
    return sugestoes

def validar_email_formato(email: str) -> bool:
    """
    Valida o formato do email
    
    Args:
        email: Email a ser validado
        
    Returns:
        bool: True se válido, False caso contrário
    """
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def log_tentativa_recuperacao(
    db: Session,
    email: str,
    ip_origem: str,
    user_agent: str,
    sucesso: bool,
    motivo: str = None
):
    """
    Registra tentativa de recuperação para auditoria
    
    Args:
        db: Sessão do banco de dados
        email: Email usado na tentativa
        ip_origem: IP de origem
        user_agent: User agent do navegador
        sucesso: Se a tentativa foi bem-sucedida
        motivo: Motivo da falha (se houver)
    """
    # Aqui você pode implementar um sistema de log mais robusto
    # Por exemplo, salvando em uma tabela de auditoria
    import logging
    
    logger = logging.getLogger(__name__)
    
    if sucesso:
        logger.info(f"Recuperação de senha solicitada com sucesso para {email} de {ip_origem}")
    else:
        logger.warning(f"Tentativa de recuperação falhou para {email} de {ip_origem}: {motivo}")

def limpar_tokens_expirados(db: Session):
    """
    Remove tokens expirados do banco de dados (cleanup)
    
    Args:
        db: Sessão do banco de dados
    """
    agora = datetime.utcnow()
    
    tokens_expirados = db.query(RecuperacaoSenha).filter(
        RecuperacaoSenha.expira_em < agora
    ).all()
    
    for token in tokens_expirados:
        db.delete(token)
    
    db.commit()
    
    return len(tokens_expirados)
