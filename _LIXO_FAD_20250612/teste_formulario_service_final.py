#!/usr/bin/env python3
"""
Teste do FormularioService após correções para usar apenas tabela Cadastro.usuario_sistema
"""

import sys
import os
import logging
from pathlib import Path

# Adiciona o diretório do projeto ao path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.services.formulario_service import FormularioService

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def teste_formulario_service():
    """Testa o FormularioService com dados reais da base"""
    
    try:
        logger.info("🔧 Iniciando teste do FormularioService")
        
        # 1. Conecta ao banco
        engine = create_engine("sqlite:///c:/Users/vinic/fad-geo/database.db")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        logger.info("✅ Conexão com banco estabelecida")
        
        # 2. Verifica se há usuários na tabela Cadastro.usuario_sistema
        result = db.execute(text("""
            SELECT 
                id, nome, email, email_institucional, cpf, telefone, tipo, status, ativo
            FROM "Cadastro.usuario_sistema" 
            WHERE email_institucional IS NOT NULL 
            LIMIT 5
        """))
        
        usuarios = result.fetchall()
        
        if not usuarios:
            logger.error("❌ Nenhum usuário encontrado na tabela Cadastro.usuario_sistema")
            return False
            
        logger.info(f"📋 Encontrados {len(usuarios)} usuários na base:")
        for usuario in usuarios:
            logger.info(f"   ID: {usuario[0]}, Nome: {usuario[1]}, Email Inst: {usuario[3]}, Tipo: {usuario[6]}")
        
        # 3. Pega o primeiro usuário para teste
        usuario_teste = usuarios[0]
        usuario_id = usuario_teste[0]
        
        logger.info(f"🎯 Testando com usuário ID: {usuario_id}")
        
        # 4. Instancia o FormularioService
        formulario_service = FormularioService()
        
        # 5. Gera o formulário HTML
        logger.info("🔧 Gerando formulário HTML...")
        caminho_arquivo = formulario_service.gerar_formulario_html(db, usuario_id)
        
        # 6. Verifica se o arquivo foi criado
        if os.path.exists(caminho_arquivo):
            tamanho = os.path.getsize(caminho_arquivo)
            logger.info(f"✅ SUCESSO! Formulário gerado:")
            logger.info(f"   📁 Arquivo: {caminho_arquivo}")
            logger.info(f"   📊 Tamanho: {tamanho} bytes")
            
            # Mostra as primeiras linhas do HTML gerado
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                primeiras_linhas = f.read(500)
            logger.info(f"   📄 Primeiras linhas:\n{primeiras_linhas}...")
            
            return True
        else:
            logger.error(f"❌ Arquivo não foi criado: {caminho_arquivo}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro no teste: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return False
    finally:
        if 'db' in locals():
            db.close()

def teste_estrutura_tabela():
    """Verifica a estrutura da tabela Cadastro.usuario_sistema"""
    
    try:
        logger.info("🔍 Verificando estrutura da tabela Cadastro.usuario_sistema")
        
        engine = create_engine("sqlite:///c:/Users/vinic/fad-geo/database.db")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Verifica as colunas da tabela
        result = db.execute(text('PRAGMA table_info("Cadastro.usuario_sistema")'))
        colunas = result.fetchall()
        
        logger.info("📋 Colunas da tabela Cadastro.usuario_sistema:")
        for coluna in colunas:
            logger.info(f"   - {coluna[1]} ({coluna[2]})")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar estrutura: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DO FORMULARIO SERVICE - VERSÃO CORRIGIDA")
    print("=" * 60)
    
    # Primeiro verifica a estrutura da tabela
    print("\n1. VERIFICANDO ESTRUTURA DA TABELA")
    if not teste_estrutura_tabela():
        print("❌ Falha ao verificar estrutura da tabela")
        sys.exit(1)
    
    # Depois testa a geração do formulário
    print("\n2. TESTANDO GERAÇÃO DE FORMULÁRIO")
    if teste_formulario_service():
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("O FormularioService está funcionando corretamente.")
    else:
        print("\n❌ TESTE FALHOU!")
        print("Há problemas no FormularioService.")
        sys.exit(1)
