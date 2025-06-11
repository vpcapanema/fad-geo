#!/usr/bin/env python3
"""
Teste direto do endpoint de cadastro - CPF sem formatação
"""

import requests
import json
import random

def testar_endpoint_direto():
    """Testa o endpoint diretamente com CPF sem formatação"""
    print("🎯 TESTE DIRETO - ENDPOINT CADASTRO")
    print("=" * 50)
    
    # CPF apenas com números (11 dígitos)
    cpf_numerico = str(11111111000 + random.randint(1, 999))
    
    dados = {
        'nome': 'Teste CPF Sem Formatação',
        'cpf': cpf_numerico,  # Apenas números
        'email': 'teste.cpf@example.com',
        'telefone': '(11) 99999-8888',
        'senha': 'MinhaSenh@123',
        'tipo': 'administrador',
        'instituicao': 'DER-SP',
        'tipo_lotacao': 'sede',
        'email_institucional': 'vpcapanema@der.sp.gov.br',
        'telefone_institucional': '(11) 3311-1234',
        'ramal': '1234',
        'sede_hierarquia': 'VPC',
        'sede_coordenadoria': 'GEOSER',
        'sede_setor': 'Análise de Dados'
    }
    
    print(f"👤 Nome: {dados['nome']}")
    print(f"🆔 CPF (números): {dados['cpf']}")
    print(f"📧 Email: {dados['email_institucional']}")
    print()
    
    url = 'http://localhost:8000/api/cd/cadastro-usuario-sistema'
    
    try:
        print(f"🌐 Testando: {url}")
        response = requests.post(
            url,
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 201:
            resultado = response.json()
            print("✅ SUCESSO!")
            print(f"🆔 ID Usuario: {resultado.get('id')}")
            print(f"📄 PDF gerado: {'✅' if resultado.get('comprovante_gerado') else '❌'}")
            print(f"📧 Email enviado: {'✅' if resultado.get('email_enviado') else '❌'}")
            if resultado.get('caminho_pdf'):
                print(f"📁 Arquivo PDF: {resultado['caminho_pdf']}")
            return True
            
        elif response.status_code == 422:
            erro = response.json()
            print("❌ Erro de validação:")
            for detail in erro.get('detail', []):
                campo = detail.get('loc', ['?'])[-1]
                mensagem = detail.get('msg', 'Erro desconhecido')
                valor = detail.get('input', 'N/A')
                print(f"   • Campo: {campo}")
                print(f"   • Erro: {mensagem}")
                print(f"   • Valor: {valor}")
                
        else:
            print(f"❌ Erro {response.status_code}")
            try:
                erro = response.json()
                print(f"📄 Detalhes: {erro.get('detail', 'N/A')}")
            except:
                print(f"📄 Resposta: {response.text[:300]}...")
                
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        
    return False

if __name__ == "__main__":
    sucesso = testar_endpoint_direto()
    
    print("\n" + "=" * 50)
    if sucesso:
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("✅ Sistema funcionando com CPF sem formatação")
    else:
        print("❌ TESTE FALHOU")
        print("🔧 Verifique os erros acima")
    print("=" * 50)
