#!/usr/bin/env python3
"""
Script para verificar e criar tabelas necessárias para o sistema FAD-GEO
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import engine
from app.database.base import Base

def verificar_criar_tabelas():
    """Verifica e cria as tabelas necessárias"""
    try:
        print("🔍 Verificando tabelas no banco de dados...")
        
        # Importa todos os modelos para registrar no Base.metadata
        try:
            from app.models.cd_usuario_sistema import UsuarioSistema
            from app.models.cd_pessoa_fisica import PessoaFisica
            from app.models.cd_pessoa_juridica import PessoaJuridica
            from app.models.pr_projeto import Projeto
            from app.models.pr_relatorio_modulo import RelatorioModulo
            from app.models.pr_modulo_configuracao import ModuloConfiguracao
            print("✅ Modelos importados com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao importar alguns modelos: {e}")
        
        # Cria todas as tabelas
        print("📦 Criando tabelas (se não existirem)...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tabelas verificadas/criadas com sucesso!")
        
        # Lista algumas tabelas importantes
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        tabelas_importantes = [
            "projeto",
            "relatorio_modulo", 
            "modulo_configuracao",
            "usuario_sistema",
            "pessoa_fisica"
        ]
        
        print("\n📋 Status das tabelas importantes:")
        for tabela in tabelas_importantes:
            try:
                existe = inspector.has_table(tabela, schema="public")
                status = "✅" if existe else "❌"
                print(f"  {status} {tabela}")
            except:
                # Tenta sem schema
                try:
                    existe = inspector.has_table(tabela)
                    status = "✅" if existe else "❌"
                    print(f"  {status} {tabela} (sem schema)")
                except:
                    print(f"  ❓ {tabela} (erro ao verificar)")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar/criar tabelas: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verificar_criar_tabelas()
