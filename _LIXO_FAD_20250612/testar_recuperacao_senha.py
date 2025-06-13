#!/usr/bin/env python3
"""
Script para testar a funcionalidade de recuperação de senha
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
sys.path.append(str(Path(__file__).parent))

from app.services.email_service import email_service
from app.database.session import get_db
from app.models.cd_usuario_sistema import UsuarioSistema
from app.models.au_recuperacao_senha import RecuperacaoSenha
from sqlalchemy.orm import Session

def testar_configuracao_email():
    """Testa a configuração do email"""
    print("🔧 Testando configuração de email...")
    
    # Exibe as configurações atuais
    print(f"SMTP Server: {email_service.smtp_server}")
    print(f"SMTP Port: {email_service.smtp_port}")
    print(f"SMTP Username: {email_service.smtp_username}")
    print(f"From Email: {email_service.from_email}")
    print(f"From Name: {email_service.from_name}")
    
    # Verifica se a senha está configurada
    if email_service.smtp_password:
        print("✅ Senha SMTP configurada")
        
        # Testa a conexão
        try:
            if email_service.testar_configuracao():
                print("✅ Conexão SMTP funcionando!")
                return True
            else:
                print("❌ Falha na conexão SMTP")
                return False
        except Exception as e:
            print(f"❌ Erro na conexão SMTP: {e}")
            return False
    else:
        print("⚠️  Senha SMTP não configurada - modo desenvolvimento")
        return True

def testar_envio_email_recuperacao():
    """Testa o envio de email de recuperação"""
    print("\n📧 Testando envio de email de recuperação...")
    
    # Dados de teste
    email_teste = "teste@exemplo.com"
    nome_teste = "Usuário Teste"
    token_teste = "test-token-123456"
    
    try:
        resultado = email_service.enviar_email_recuperacao_senha(
            destinatario_email=email_teste,
            destinatario_nome=nome_teste,
            token_recuperacao=token_teste,
            base_url="http://127.0.0.1:8000"
        )
        
        if resultado:
            print("✅ Email de recuperação enviado com sucesso!")
            return True
        else:
            print("❌ Falha no envio do email")
            return False
            
    except Exception as e:
        print(f"❌ Erro no envio de email: {e}")
        return False

def listar_usuarios_sistema():
    """Lista os usuários do sistema para teste"""
    print("\n👥 Listando usuários do sistema...")
    
    try:
        db = next(get_db())
        
        usuarios = db.query(UsuarioSistema).filter(
            UsuarioSistema.ativo == True
        ).all()
        
        if usuarios:
            print(f"📋 Encontrados {len(usuarios)} usuários ativos:")
            for i, usuario in enumerate(usuarios, 1):
                print(f"  {i}. {usuario.nome} ({usuario.email}) - {usuario.tipo} - Status: {usuario.status}")
        else:
            print("❌ Nenhum usuário ativo encontrado")
            
        db.close()
        return usuarios
        
    except Exception as e:
        print(f"❌ Erro ao listar usuários: {e}")
        return []

def testar_fluxo_completo(email_usuario=None):
    """Testa o fluxo completo de recuperação"""
    print("\n🔄 Testando fluxo completo de recuperação...")
    
    if not email_usuario:
        usuarios = listar_usuarios_sistema()
        if not usuarios:
            print("❌ Não há usuários para testar")
            return False
            
        email_usuario = usuarios[0].email
        print(f"📧 Usando email do primeiro usuário: {email_usuario}")
    
    try:
        db = next(get_db())
        
        # Busca o usuário
        usuario = db.query(UsuarioSistema).filter(
            UsuarioSistema.email == email_usuario,
            UsuarioSistema.ativo == True
        ).first()
        
        if not usuario:
            print(f"❌ Usuário {email_usuario} não encontrado")
            return False
        
        print(f"✅ Usuário encontrado: {usuario.nome}")
        
        # Cria token de recuperação
        recuperacao = RecuperacaoSenha(
            usuario_id=usuario.id,
            ip_solicitacao="127.0.0.1",
            user_agent="test-script"
        )
        
        db.add(recuperacao)
        db.commit()
        
        print(f"✅ Token de recuperação criado: {recuperacao.token}")
        
        # Testa envio de email
        resultado_email = email_service.enviar_email_recuperacao_senha(
            destinatario_email=usuario.email,
            destinatario_nome=usuario.nome,
            token_recuperacao=recuperacao.token,
            base_url="http://127.0.0.1:8000"
        )
        
        if resultado_email:
            print("✅ Email enviado com sucesso!")
            print(f"🔗 Link de recuperação: http://127.0.0.1:8000/recuperacao/redefinir/{recuperacao.token}")
            
            # Verifica validade do token
            if recuperacao.is_valid:
                print("✅ Token válido e ativo")
            else:
                print("❌ Token inválido")
                
        else:
            print("❌ Falha no envio do email")
            
        db.close()
        return resultado_email
        
    except Exception as e:
        print(f"❌ Erro no fluxo completo: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando testes de recuperação de senha FAD")
    print("=" * 50)
    
    # Testa configuração
    config_ok = testar_configuracao_email()
    
    # Testa envio básico
    envio_ok = testar_envio_email_recuperacao()
    
    # Lista usuários
    usuarios = listar_usuarios_sistema()
    
    # Testa fluxo completo
    if usuarios:
        fluxo_ok = testar_fluxo_completo()
    else:
        fluxo_ok = False
        print("⚠️  Pulando teste de fluxo completo - sem usuários")
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    print(f"  Configuração: {'✅' if config_ok else '❌'}")
    print(f"  Envio Email: {'✅' if envio_ok else '❌'}")
    print(f"  Usuários: {'✅' if usuarios else '❌'}")
    print(f"  Fluxo Completo: {'✅' if fluxo_ok else '❌'}")
    
    if config_ok and envio_ok and usuarios and fluxo_ok:
        print("\n🎉 Todos os testes passaram! Sistema de recuperação funcionando!")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique as configurações.")

if __name__ == "__main__":
    main()
