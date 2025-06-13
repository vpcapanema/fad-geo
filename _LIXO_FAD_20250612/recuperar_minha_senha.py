#!/usr/bin/env python3
"""
Script para recuperar a senha do próprio usuário (Vinicius)
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
sys.path.append(str(Path(__file__).parent))

from app.database.session import get_db
from app.models.cd_usuario_sistema import UsuarioSistema
from app.models.au_recuperacao_senha import RecuperacaoSenha
from app.services.email_service import email_service
from app.utils.password_utils import invalidar_tokens_anteriores
from sqlalchemy.orm import Session

def recuperar_senha_vinicius():
    """Gera um token de recuperação para o usuário Vinicius"""
    print("🔑 RECUPERAÇÃO DE SENHA - VINICIUS")
    print("=" * 50)
    
    try:
        db = next(get_db())
        
        # Busca o usuário Vinicius
        usuario = db.query(UsuarioSistema).filter(
            UsuarioSistema.email == "vpcapanema@der.sp.gov.br"
        ).first()
        
        if not usuario:
            print("❌ Usuário vpcapanema@der.sp.gov.br não encontrado")
            print("\n📋 Usuários master disponíveis:")
            
            masters = db.query(UsuarioSistema).filter(
                UsuarioSistema.tipo == "master",
                UsuarioSistema.ativo == True
            ).all()
            
            for master in masters:
                print(f"   - {master.nome} ({master.email})")
                
            return False
        
        print(f"✅ Usuário encontrado: {usuario.nome}")
        print(f"📧 Email: {usuario.email}")
        print(f"👤 Tipo: {usuario.tipo}")
        print(f"✅ Status: {usuario.status}")
        
        # Invalida tokens anteriores
        invalidar_tokens_anteriores(db, usuario.id)
        
        # Cria novo token de recuperação
        recuperacao = RecuperacaoSenha(
            usuario_id=usuario.id,
            ip_solicitacao="127.0.0.1",
            user_agent="script-recuperacao-vinicius"
        )
        
        db.add(recuperacao)
        db.commit()
        
        print(f"✅ Token de recuperação criado: {recuperacao.token}")
        
        # Envia email (modo desenvolvimento)
        email_enviado = email_service.enviar_email_recuperacao_senha(
            destinatario_email=usuario.email,
            destinatario_nome=usuario.nome,
            token_recuperacao=recuperacao.token,
            base_url="http://127.0.0.1:8000"
        )
        
        if email_enviado:
            print("\n🎉 SUCESSO! Token de recuperação gerado.")
            print("\n🔗 LINK DIRETO PARA REDEFINIR SUA SENHA:")
            print(f"   http://127.0.0.1:8000/recuperacao/redefinir/{recuperacao.token}")
            print("\n📋 INSTRUÇÕES:")
            print("1. Clique no link acima ou copie e cole no navegador")
            print("2. Digite sua nova senha (deve ser forte)")
            print("3. Confirme a nova senha")
            print("4. Clique em 'Redefinir Senha'")
            print("\n⏰ IMPORTANTE:")
            print("   - Este token expira em 15 minutos")
            print("   - Só pode ser usado uma vez")
            print("   - Para sua segurança, não compartilhe este link")
            
            return True
        else:
            print("❌ Falha no envio do email")
            return False
            
        db.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 SCRIPT DE RECUPERAÇÃO DE SENHA PESSOAL")
    print("   Para: Vinicius do Prado Capanema")
    print()
    
    if recuperar_senha_vinicius():
        print("\n✅ Recuperação gerada com sucesso!")
        print("   Acesse o link mostrado acima para redefinir sua senha.")
    else:
        print("\n❌ Falha na recuperação.")
        print("   Verifique os logs acima para mais detalhes.")

if __name__ == "__main__":
    main()
