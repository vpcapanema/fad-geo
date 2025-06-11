#!/usr/bin/env python3
"""
Script de debug para teste de elemento rodoviário
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from app.database.session import get_db
from app.models.cd_trecho_estadualizacao import TrechoEstadualizacao
from sqlalchemy.exc import IntegrityError

def testar_elemento_rodoviario():
    """Testa criação de elemento rodoviário diretamente no banco"""
    
    print("🔍 Testando criação de elemento rodoviário...")
    
    db = next(get_db())
    
    try:
        # Dados de teste
        dados = {
            'codigo': 'SP-999-TEST',
            'denominacao': 'Rodovia de Teste Debug', 
            'municipio': 'São Paulo'
        }
        
        print(f"📝 Dados: {dados}")
        
        # Verifica se já existe um elemento com este código
        existente = db.query(TrechoEstadualizacao).filter(
            TrechoEstadualizacao.codigo == dados['codigo']
        ).first()
        
        if existente:
            print(f"⚠️  Elemento já existe: ID {existente.id}")
            # Remove o existente para o teste
            db.delete(existente)
            db.commit()
            print("🗑️  Elemento existente removido")
        
        # Cria novo elemento
        novo_elemento = TrechoEstadualizacao(
            codigo=dados['codigo'],
            denominacao=dados['denominacao'],
            municipio=dados['municipio']
        )
        
        print("💾 Adicionando elemento ao banco...")
        db.add(novo_elemento)
        
        print("💾 Fazendo commit...")
        db.commit()
        
        print("🔄 Atualizando objeto...")
        db.refresh(novo_elemento)
        
        print(f"✅ Elemento criado com sucesso! ID: {novo_elemento.id}")
        
        return {
            "success": True,
            "id": novo_elemento.id,
            "codigo": novo_elemento.codigo
        }
        
    except IntegrityError as e:
        db.rollback()
        print(f"❌ Erro de integridade: {e}")
        return {"success": False, "error": f"Integridade: {e}"}
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro geral: {type(e).__name__}: {e}")
        return {"success": False, "error": f"{type(e).__name__}: {e}"}
        
    finally:
        db.close()

if __name__ == "__main__":
    resultado = testar_elemento_rodoviario()
    print(f"\n🎯 Resultado final: {resultado}")
