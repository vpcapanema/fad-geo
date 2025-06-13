#!/usr/bin/env python3
"""
Teste do FormularioService após correções
- Remove dependência de PessoaFisica
- Usa APENAS dados da tabela Cadastro.usuario_sistema
- Valida geração de formulário HTML completo
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from datetime import datetime
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.formulario_service import FormularioService
from app.models.cd_usuario_sistema import UsuarioSistema

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('teste_formulario_corrigido.log')
    ]
)
logger = logging.getLogger(__name__)

def testar_formulario_service():
    """Testa o FormularioService com dados reais do banco"""
    try:
        # 1. Conecta ao banco
        engine = create_engine('sqlite:///database.db')
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        logger.info("🔗 Conectado ao banco de dados")
        
        # 2. Busca um usuário real no banco
        usuario = db.query(UsuarioSistema).filter(
            UsuarioSistema.email_institucional.isnot(None)
        ).first()
        
        if not usuario:
            logger.error("❌ Nenhum usuário com email institucional encontrado")
            return False
            
        logger.info(f"✅ Usuário encontrado - ID: {usuario.id}, Tipo: {usuario.tipo}")
        logger.info(f"   📧 Email: {usuario.email_institucional}")
        logger.info(f"   👤 Nome: {usuario.nome}")
        
        # 3. Instancia o FormularioService
        formulario_service = FormularioService()
        
        # 4. Testa geração do formulário HTML
        logger.info("🔧 Iniciando teste de geração de formulário...")
        
        caminho_arquivo = formulario_service.gerar_formulario_html(db, usuario.id)
        
        # 5. Valida resultado
        if caminho_arquivo and os.path.exists(caminho_arquivo):
            logger.info(f"✅ SUCESSO! Formulário gerado em: {caminho_arquivo}")
            
            # Verifica tamanho do arquivo
            tamanho = os.path.getsize(caminho_arquivo)
            logger.info(f"📊 Tamanho do arquivo: {tamanho} bytes")
            
            # Lê o conteúdo para verificar se foi preenchido
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                
            # Verifica se dados do usuário estão no HTML
            campos_obrigatorios = [
                usuario.nome,
                usuario.email_institucional,
                str(usuario.id),
                usuario.tipo
            ]
            
            campos_encontrados = 0
            for campo in campos_obrigatorios:
                if campo and campo in conteudo:
                    campos_encontrados += 1
                    logger.info(f"✅ Campo encontrado no HTML: {campo}")
                else:
                    logger.warning(f"⚠️ Campo não encontrado: {campo}")
            
            if campos_encontrados == len(campos_obrigatorios):
                logger.info("🎉 TESTE COMPLETO COM SUCESSO!")
                logger.info("   ✅ Formulário gerado corretamente")
                logger.info("   ✅ Dados do usuário populados")
                logger.info("   ✅ Estrutura de diretórios criada")
                return True
            else:
                logger.error(f"❌ Apenas {campos_encontrados}/{len(campos_obrigatorios)} campos encontrados")
                return False
                
        else:
            logger.error("❌ FALHA! Arquivo não foi criado")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro no teste: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return False
    finally:
        if 'db' in locals():
            db.close()

def testar_endpoint_http():
    """Testa o endpoint HTTP após as correções"""
    try:
        import requests
        import json
        
        logger.info("🌐 Testando endpoint HTTP...")
        
        # Dados de teste
        dados_usuario = {
            "nome": "Teste Formulario Corrigido",
            "cpf": "12345678901",
            "telefone": "(61) 99999-9999",
            "email": "teste.formulario@fad.df.gov.br",
            "email_institucional": "teste.formulario@fad.df.gov.br",
            "telefone_institucional": "(61) 3333-4444",
            "ramal": "1234",
            "instituicao": "FAD",
            "tipo_lotacao": "Sede",
            "sede_hierarquia": "SUAG",
            "sede_coordenadoria": "COGEO",
            "sede_setor": "SEGER",
            "sede_assistencia": "ASGEO",
            "regional_nome": "",
            "regional_coordenadoria": "",
            "regional_setor": "",
            "tipo": "coordenador",
            "status": "ativo",
            "ativo": True,
            "pessoa_fisica_id": None
        }
        
        # Faz requisição para o endpoint
        response = requests.post(
            "http://localhost:8000/api/cadastro-usuario-sistema/",
            json=dados_usuario,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            resultado = response.json()
            logger.info("✅ Endpoint respondeu com sucesso")
            
            # Verifica se formulario_html não é None
            formulario_html = resultado.get('formulario_html')
            if formulario_html and formulario_html != "None":
                logger.info(f"✅ Campo formulario_html preenchido: {formulario_html}")
                logger.info("🎉 ENDPOINT TESTE COM SUCESSO!")
                return True
            else:
                logger.error(f"❌ Campo formulario_html ainda é None: {formulario_html}")
                return False
        else:
            logger.error(f"❌ Endpoint falhou - Status: {response.status_code}")
            logger.error(f"❌ Resposta: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro no teste do endpoint: {e}")
        return False

if __name__ == "__main__":
    logger.info("🧪 Iniciando testes do FormularioService corrigido")
    logger.info("=" * 60)
    
    # Teste 1: FormularioService isolado
    logger.info("📝 TESTE 1: FormularioService isolado")
    sucesso_service = testar_formulario_service()
    
    # Teste 2: Endpoint HTTP
    logger.info("\n📝 TESTE 2: Endpoint HTTP")
    sucesso_endpoint = testar_endpoint_http()
    
    # Resultado final
    logger.info("\n" + "=" * 60)
    logger.info("📊 RESULTADO FINAL DOS TESTES:")
    logger.info(f"   FormularioService: {'✅ PASSOU' if sucesso_service else '❌ FALHOU'}")
    logger.info(f"   Endpoint HTTP: {'✅ PASSOU' if sucesso_endpoint else '❌ FALHOU'}")
    
    if sucesso_service and sucesso_endpoint:
        logger.info("🎉 TODOS OS TESTES PASSARAM! Sistema corrigido.")
    else:
        logger.info("❌ Alguns testes falharam. Verifique os logs acima.")
