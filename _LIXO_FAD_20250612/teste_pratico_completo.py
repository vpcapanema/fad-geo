#!/usr/bin/env python3
"""
🎯 TESTE PRÁTICO COMPLETO DO FLUXO DE CADASTRO
Teste real do endpoint completo com email válido do usuário
"""

import requests
import json
import sys
import os
import time
from datetime import datetime

def verificar_servidor():
    """Verifica se o servidor está rodando"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Servidor está rodando (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"❌ Servidor não está rodando: {e}")
        return False

def testar_fluxo_completo():
    """Testa o fluxo completo de cadastro com dados reais"""
    print("=" * 80)
    print("🎯 TESTE PRÁTICO COMPLETO DO FLUXO DE CADASTRO")
    print("=" * 80)    # Dados reais do teste
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Gera um CPF único baseado no timestamp atual (só para teste)
    import time
    timestamp_num = str(int(time.time()))[-9:]  # Últimos 9 dígitos do timestamp
    cpf_unico = f"11{timestamp_num}"  # CPF fictício único para o teste (11 dígitos)
    
    dados_teste = {
        "nome": f"Vinícius Capanema - Teste Completo {timestamp}",
        "cpf": cpf_unico,  # CPF único baseado no timestamp
        "email": "vpcapanema@der.sp.gov.br",  # Email real do usuário
        "telefone": "11987654321",
        "senha": "senha123",
        "tipo": "coordenador",
        "instituicao": "DER-SP",
        "tipo_lotacao": "sede",
        "email_institucional": "vpcapanema@der.sp.gov.br",
        "telefone_institucional": "1133334444",
        "ramal": "4321",
        "sede_hierarquia": "Diretoria de Engenharia",
        "sede_coordenadoria": "Coordenadoria de Projetos Especiais",
        "sede_setor": "Setor de Desenvolvimento de Sistemas"
    }
    
    print(f"📤 DADOS DO TESTE:")
    print(f"   📧 Email real: {dados_teste['email']}")
    print(f"   👤 Nome: {dados_teste['nome']}")
    print(f"   🏢 Instituição: {dados_teste['instituicao']}")
    print(f"   📋 Tipo: {dados_teste['tipo']}")
    print(f"   🏛️ Lotação: {dados_teste['tipo_lotacao']}")
    
    # URL do endpoint
    url = "http://localhost:8000/api/cd/cadastro-usuario-sistema"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    print(f"\n📡 FAZENDO REQUISIÇÃO PARA: {url}")
    
    try:
        # Registra tempo de início
        inicio = time.time()
        
        # Fazer a requisição POST
        response = requests.post(url, json=dados_teste, headers=headers, timeout=60)
        
        # Calcula tempo de resposta
        tempo_resposta = time.time() - inicio
        
        print(f"\n📊 RESPOSTA RECEBIDA:")
        print(f"   ⏱️ Tempo de resposta: {tempo_resposta:.2f}s")
        print(f"   📈 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            # SUCESSO!
            resposta = response.json()
            
            print(f"\n🎉 CADASTRO REALIZADO COM SUCESSO!")
            print(f"   🆔 ID do usuário: {resposta.get('id')}")
            print(f"   👤 Nome: {resposta.get('nome')}")
            print(f"   📊 Status: {resposta.get('status')}")
            print(f"   📧 Email enviado: {resposta.get('email_enviado')}")
            print(f"   📄 PDF gerado: {resposta.get('comprovante_gerado')}")
            
            # VERIFICAÇÃO DO FORMULÁRIO HTML
            formulario_html = resposta.get('formulario_html')
            print(f"\n📋 FORMULÁRIO HTML:")
            if formulario_html:
                print(f"   ✅ Campo formulario_html retornado: {formulario_html}")
                
                # Verifica se o arquivo existe
                if os.path.exists(formulario_html):
                    tamanho = os.path.getsize(formulario_html)
                    print(f"   ✅ Arquivo existe: {tamanho} bytes")
                    
                    # Lê algumas linhas do arquivo para verificar conteúdo
                    try:
                        with open(formulario_html, 'r', encoding='utf-8') as f:
                            linhas = f.readlines()[:10]  # Primeiras 10 linhas
                            print(f"   📖 Primeiras linhas do HTML:")
                            for i, linha in enumerate(linhas, 1):
                                print(f"      {i:2d}: {linha.strip()[:80]}...")
                    except Exception as e:
                        print(f"   ⚠️ Erro ao ler arquivo: {e}")
                        
                else:
                    print(f"   ❌ Arquivo não encontrado: {formulario_html}")
            else:
                print(f"   ❌ Campo formulario_html retorna None")
            
            # VERIFICAÇÃO DO PDF
            caminho_pdf = resposta.get('caminho_pdf')
            print(f"\n📄 PDF GERADO:")
            if caminho_pdf:
                print(f"   📁 Caminho: {caminho_pdf}")
                
                if os.path.exists(caminho_pdf):
                    tamanho_pdf = os.path.getsize(caminho_pdf)
                    print(f"   ✅ PDF existe: {tamanho_pdf} bytes")
                else:
                    print(f"   ❌ PDF não encontrado: {caminho_pdf}")
            else:
                print(f"   ❌ Caminho do PDF não retornado")
            
            # VERIFICAÇÃO DO EMAIL
            email_enviado = resposta.get('email_enviado', False)
            print(f"\n📧 EMAIL:")
            if email_enviado:
                print(f"   ✅ Email enviado com sucesso para: {dados_teste['email']}")
                print(f"   📮 Verifique sua caixa de entrada em: {dados_teste['email_institucional']}")
                print(f"   ⚠️ Pode estar na pasta SPAM/Lixo Eletrônico")
            else:
                print(f"   ❌ Falha no envio do email")
            
            # RESUMO FINAL
            print(f"\n" + "="*60)
            print(f"🎯 RESUMO DO TESTE COMPLETO:")
            print(f"   ✅ Usuário cadastrado: ID {resposta.get('id')}")
            print(f"   {'✅' if formulario_html else '❌'} Formulário HTML: {'OK' if formulario_html else 'FALHA'}")
            print(f"   {'✅' if caminho_pdf else '❌'} PDF gerado: {'OK' if caminho_pdf else 'FALHA'}")
            print(f"   {'✅' if email_enviado else '❌'} Email enviado: {'OK' if email_enviado else 'FALHA'}")
            print(f"="*60)
            
            if formulario_html and caminho_pdf and email_enviado:
                print(f"🏆 TESTE COMPLETO: TODOS OS COMPONENTES FUNCIONARAM!")
            else:
                print(f"⚠️ TESTE PARCIAL: Alguns componentes falharam")
                
            return True
            
        else:
            # ERRO
            print(f"\n❌ ERRO NA REQUISIÇÃO:")
            print(f"   📈 Status: {response.status_code}")
            print(f"   📝 Resposta: {response.text}")
            
            # Tenta parsear JSON de erro
            try:
                erro_json = response.json()
                print(f"   💬 Detalhe: {erro_json.get('detail', 'Não especificado')}")
            except:
                pass
                
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERRO DE CONEXÃO:")
        print(f"   Não foi possível conectar ao servidor")
        print(f"   Verifique se a API está rodando")
        return False
        
    except requests.exceptions.Timeout:
        print(f"\n❌ TIMEOUT:")
        print(f"   A requisição demorou mais de 60 segundos")
        return False
        
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def main():
    """Função principal do teste"""
    print("🔍 Verificando se o servidor está rodando...")
    
    if not verificar_servidor():
        print("\n💡 COMO INICIAR A API:")
        print("   1. Abra um terminal PowerShell")
        print("   2. Navegue para: c:\\Users\\vinic\\fad-geo")
        print("   3. Execute: python main.py")
        print("   4. Aguarde a mensagem 'Uvicorn running on...'")
        print("   5. Execute este teste novamente")
        return False
    
    print("\n🚀 Iniciando teste prático completo...")
    resultado = testar_fluxo_completo()
    
    if resultado:
        print(f"\n✅ TESTE CONCLUÍDO COM SUCESSO!")
        print(f"📧 IMPORTANTE: Verifique seu email {dados_teste['email']} para confirmar o recebimento!")
    else:
        print(f"\n❌ TESTE FALHOU!")
        
    input("\n👆 Pressione ENTER para finalizar...")
    return resultado

if __name__ == "__main__":
    # Define dados globais para acesso em main()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dados_teste = {
        "email": "vpcapanema@der.sp.gov.br",
        "email_institucional": "vpcapanema@der.sp.gov.br"
    }
    
    main()
