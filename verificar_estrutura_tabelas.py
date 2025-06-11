"""
Script para verificar a estrutura das tabelas de elementos rodoviários
"""
import sys
import os
from sqlalchemy import create_engine, text, inspect

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import engine

def verificar_estrutura_tabelas():
    """Verifica a estrutura das tabelas de elementos rodoviários"""
    inspector = inspect(engine)
    
    tabelas = ['trecho_rodoviario', 'rodovia', 'dispositivo', 'obra_arte']
    schema = 'Elementos_rodoviarios'
    
    print("=== ESTRUTURA DAS TABELAS ===")
    
    for tabela in tabelas:
        print(f"\n📋 Tabela: {schema}.{tabela}")
        print("-" * 60)
        
        try:
            columns = inspector.get_columns(tabela, schema=schema)
            
            if columns:
                print("Colunas encontradas:")
                for col in columns:
                    nullable = "NULL" if col['nullable'] else "NOT NULL"
                    default = f" DEFAULT {col['default']}" if col['default'] else ""
                    print(f"  - {col['name']}: {col['type']} {nullable}{default}")
            else:
                print("  ❌ Nenhuma coluna encontrada")
                
        except Exception as e:
            print(f"  ❌ Erro ao acessar tabela: {e}")

def main():
    """Função principal"""
    print("🔍 VERIFICANDO ESTRUTURA DAS TABELAS DE ELEMENTOS RODOVIÁRIOS")
    print("=" * 80)
    
    try:
        verificar_estrutura_tabelas()
        
        print("\n" + "=" * 80)
        print("✅ VERIFICAÇÃO CONCLUÍDA")
        
    except Exception as e:
        print(f"\n❌ ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
