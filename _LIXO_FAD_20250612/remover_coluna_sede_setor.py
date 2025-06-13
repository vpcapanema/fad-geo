#!/usr/bin/env python3
"""
Script para remover a coluna sede_setor da tabela usuario_sistema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import get_db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)

def remover_coluna_sede_setor():
    """Remove a coluna sede_setor da tabela usuario_sistema"""
    
    # Conexão com o banco
    db = next(get_db())

    try:
        print("🔍 Verificando se a coluna sede_setor existe...")
        
        # Verifica se a coluna existe antes de remover
        check_query = text('''
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'Cadastro' 
            AND table_name = 'usuario_sistema' 
            AND column_name = 'sede_setor'
        ''')
        
        result = db.execute(check_query).fetchone()
        
        if result:
            print('🔍 Coluna sede_setor encontrada no banco. Removendo...')
            
            # Remove a coluna sede_setor
            alter_query = text('ALTER TABLE "Cadastro".usuario_sistema DROP COLUMN sede_setor')
            db.execute(alter_query)
            db.commit()
            
            print('✅ Coluna sede_setor removida com sucesso!')
            return True
        else:
            print('✅ Coluna sede_setor já não existe no banco de dados')
            return True
            
    except Exception as e:
        print(f'❌ Erro ao remover coluna: {e}')
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 REMOVENDO COLUNA SEDE_SETOR DO BANCO DE DADOS")
    print("=" * 60)
    
    sucesso = remover_coluna_sede_setor()
    
    if sucesso:
        print("\n✅ Operação concluída com sucesso!")
        print("🔄 Agora o sistema deve funcionar sem erros relacionados à coluna sede_setor")
    else:
        print("\n❌ Falha na operação!")
        print("🔧 Verifique os logs de erro acima")
