#!/usr/bin/env python3
"""
Teste do fluxo completo de recuperação de senha via interface web
"""

import requests
import json
import time

def testar_fluxo_recuperacao_web():
    """Testa o fluxo completo via requisições HTTP"""
    print("🌐 TESTE DO FLUXO COMPLETO VIA INTERFACE WEB")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    # 1. Testa página de solicitação
    print("1️⃣  Testando página de solicitação...")
    try:
        response = requests.get(f"{base_url}/recuperacao/solicitar")
        if response.status_code == 200:
            print("✅ Página de solicitação carregada")
        else:
            print(f"❌ Erro ao carregar página: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    
    # 2. Testa solicitação de recuperação
    print("\n2️⃣  Testando solicitação de recuperação...")
    try:
        data = {
            "email": "vpcapanema@der.sp.gov.br",
            "tipo": "master"
        }
        
        response = requests.post(f"{base_url}/recuperacao/solicitar", data=data)
        
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code == 200:
            resposta = response.json()
            if resposta.get("success"):
                print("✅ Solicitação processada com sucesso")
                print(f"📧 Mensagem: {resposta.get('message')}")
                return True
            else:
                print(f"❌ Falha na solicitação: {resposta.get('message')}")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def verificar_servidor_ativo():
    """Verifica se o servidor está rodando"""
    print("🔍 VERIFICANDO SERVIDOR...")
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print("✅ Servidor FAD está ativo")
        return True
    except:
        print("❌ Servidor FAD não está ativo")
        print("💡 Execute: python start.ps1 ou inicie o servidor")
        return False

def main():
    print("🚀 TESTE COMPLETO DO SISTEMA DE RECUPERAÇÃO")
    print("   Via Interface Web (HTTP)")
    print()
    
    # Verifica se servidor está ativo
    if not verificar_servidor_ativo():
        return
    
    # Testa fluxo completo
    print()
    sucesso = testar_fluxo_recuperacao_web()
    
    print("\n" + "=" * 60)
    if sucesso:
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("   O sistema de recuperação está funcionando via web.")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("   1. Acesse: http://127.0.0.1:8000/recuperacao/solicitar")
        print("   2. Digite seu email: vpcapanema@der.sp.gov.br")
        print("   3. Selecione tipo: master")
        print("   4. Veja o link no console do servidor")
        print("   5. Acesse o link para redefinir sua senha")
    else:
        print("❌ TESTE FALHOU")
        print("   Verifique os logs acima para identificar o problema.")

if __name__ == "__main__":
    main()
