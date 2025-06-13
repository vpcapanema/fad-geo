#!/usr/bin/env python3
"""
Teste para verificar schema Cadastro no PostgreSQL e testar FormularioService
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.services.formulario_service import FormularioService

# String de conexão PostgreSQL AWS RDS
SQLALCHEMY_DATABASE_URL = (
    "postgresql://vinicius:Malditas131533*@fad-db.c7cu4eq2gc56.us-east-2.rds.amazonaws.com:5432/fad_db"
)

def main():
    print("🔍 TESTE: Verificando schema Cadastro no PostgreSQL AWS RDS")
    
    # Conecta ao PostgreSQL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:    
        print("🔗 Conexão estabelecida com o banco de dados")
        
        # Verifica se o schema Cadastro existe
        result = db.execute(text("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name = 'Cadastro'
        """)).fetchall()
        
        if result:
            print("✅ Schema Cadastro encontrado!")
        else:
            print("❌ Schema Cadastro NÃO encontrado")
            return
    except Exception as e:
        print(f"❌ Erro ao verificar schema Cadastro: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return

    print("\n1. ============ VERIFICANDO SCHEMA CADASTRO ============")
    
    # Lista tabelas no schema Cadastro (PostgreSQL)
    result = db.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'Cadastro' 
        AND table_name LIKE '%usuario%'
    """)).fetchall()
    
    print(f"📋 Tabelas no schema Cadastro com 'usuario': {[r[0] for r in result]}")
    
    # Verifica se existe especificamente Cadastro.usuario_sistema
    result = db.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'Cadastro' 
        AND table_name = 'usuario_sistema'
    """)).fetchall()
    
    if result:
        print(f"✅ Tabela Cadastro.usuario_sistema encontrada!")
    else:
        print("❌ Tabela Cadastro.usuario_sistema NÃO encontrada")
        
    print("\n2. ============ VERIFICANDO ESTRUTURA DA TABELA ============")
    
    # Verifica estrutura da tabela
    try:
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_schema = 'Cadastro' 
            AND table_name = 'usuario_sistema' 
            ORDER BY ordinal_position
        """)).fetchall()
        print("📋 Estrutura da tabela Cadastro.usuario_sistema:")
        for col in result:
            print(f"   - {col[0]} ({col[1]}) - Nullable: {col[2]}")
    except Exception as e:
        print(f"❌ Erro ao verificar estrutura: {e}")
        
    print("\n3. ============ VERIFICANDO DADOS EXISTENTES ============")
    
    # Conta registros
    try:
        result = db.execute(text('SELECT COUNT(*) FROM "Cadastro".usuario_sistema')).fetchone()
        total_usuarios = result[0] if result else 0
        print(f"📊 Total de usuários na tabela: {total_usuarios}")
        
        if total_usuarios > 0:
            # Pega o primeiro usuário
            result = db.execute(text("""
                SELECT id, nome, email_institucional, tipo 
                FROM "Cadastro".usuario_sistema 
                LIMIT 1
            """)).fetchone()
            
            if result:
                user_id, nome, email, tipo = result
                print(f"👤 Primeiro usuário encontrado:")
                print(f"   - ID: {user_id}")
                print(f"   - Nome: {nome}")
                print(f"   - Email: {email}")
                print(f"   - Tipo: {tipo}")
                
                print("\n4. ============ TESTANDO FORMULARIO SERVICE ============")
                
                # Testa o FormularioService
                formulario_service = FormularioService()
                
                try:
                    caminho_formulario = formulario_service.gerar_formulario_html(db, user_id)
                    print(f"✅ SUCESSO! Formulário gerado em: {caminho_formulario}")
                    
                    # Verifica se o arquivo foi criado
                    if os.path.exists(caminho_formulario):
                        tamanho = os.path.getsize(caminho_formulario)
                        print(f"📄 Arquivo criado com {tamanho} bytes")
                    else:
                        print(f"❌ Arquivo não foi criado: {caminho_formulario}")
                        
                except Exception as e:
                    print(f"❌ ERRO no FormularioService: {e}")
                    import traceback
                    print(f"❌ Traceback: {traceback.format_exc()}")
                    
        else:
            print("❌ Nenhum usuário encontrado na tabela para testar")
            
    except Exception as e:
        print(f"❌ Erro ao verificar dados: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")

    finally:
        db.close()

if __name__ == "__main__":
    main()
