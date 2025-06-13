#!/usr/bin/env python3
"""
Script para enviar email real de recuperação de senha para Vinicius
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

def enviar_recuperacao_real():
    """Envia email real de recuperação para vpcapanema@der.sp.gov.br"""
    print("📧 ENVIANDO EMAIL REAL DE RECUPERAÇÃO")
    print("=" * 60)
    
    try:
        db = next(get_db())
        
        # Busca o usuário Vinicius
        usuario = db.query(UsuarioSistema).filter(
            UsuarioSistema.email == "vpcapanema@der.sp.gov.br"
        ).first()
        
        if not usuario:
            print("❌ Usuário vpcapanema@der.sp.gov.br não encontrado")
            return False
        
        print(f"✅ Usuário encontrado: {usuario.nome}")
        print(f"📧 Email institucional: {usuario.email}")
        print(f"👤 Tipo: {usuario.tipo}")
        print(f"✅ Status: {usuario.status}")
        
        # Invalida tokens anteriores
        invalidar_tokens_anteriores(db, usuario.id)
        print("🔄 Tokens anteriores invalidados")
        
        # Cria novo token de recuperação
        recuperacao = RecuperacaoSenha(
            usuario_id=usuario.id,
            ip_solicitacao="127.0.0.1",
            user_agent="script-email-real"
        )
        
        db.add(recuperacao)
        db.commit()
        
        print(f"🔑 Token criado: {recuperacao.token}")
        print(f"⏰ Válido até: {recuperacao.data_expiracao}")
        
        # Envia email REAL
        print("\n📤 ENVIANDO EMAIL REAL...")
        email_enviado = email_service.enviar_email_recuperacao_senha(
            destinatario_email=usuario.email,
            destinatario_nome=usuario.nome,
            token_recuperacao=recuperacao.token,
            base_url="http://127.0.0.1:8000"
        )
        
        if email_enviado:
            print("\n🎉 EMAIL ENVIADO COM SUCESSO!")
            print("=" * 60)
            print("📧 DESTINATÁRIO:", usuario.email)
            print("👤 NOME:", usuario.nome)
            print("🔗 LINK:", f"http://127.0.0.1:8000/recuperacao/redefinir/{recuperacao.token}")
            print("⏰ EXPIRA EM: 15 minutos")
            print("=" * 60)
            print("\n📋 PRÓXIMOS PASSOS:")
            print("1. Verifique sua caixa de entrada em vpcapanema@der.sp.gov.br")
            print("2. Procure o email com assunto '🔐 Recuperação de Senha - FAD'")
            print("3. Se não aparecer, verifique a pasta de spam/lixo eletrônico")
            print("4. Clique no botão 'Redefinir Minha Senha' no email")
            print("5. Digite sua nova senha")
            print("6. Confirme a nova senha")
            print("7. Clique em 'Redefinir Senha'")
            
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
    print("🚀 RECUPERAÇÃO DE SENHA VIA EMAIL REAL")
    print("   Para: Vinicius do Prado Capanema")
    print("   Email: vpcapanema@der.sp.gov.br")
    print("   De: fadgeoteste@gmail.com (FAD Sistema)")
    print()
    
    if enviar_recuperacao_real():
        print("\n✅ EMAIL ENVIADO COM SUCESSO!")
        print("   Verifique sua caixa de entrada.")
    else:
        print("\n❌ FALHA NO ENVIO")
        print("   Verifique os logs acima.")

if __name__ == "__main__":
    main()
