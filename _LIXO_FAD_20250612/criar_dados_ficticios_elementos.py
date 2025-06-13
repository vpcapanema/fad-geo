"""
Script para criar dados fictícios nas tabelas de elementos rodoviários
"""
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import get_db, engine
from app.models.cd_trecho_estadualizacao import TrechoEstadualizacao
from app.models.cd_rodovia_estadualizacao import RodoviaEstadualizacao
from app.models.cd_dispositivo_estadualizacao import DispositivoEstadualizacao
from app.models.cd_obra_arte_estadualizacao import ObraArteEstadualizacao

def verificar_tabelas_existem():
    """Verifica se as tabelas existem no banco de dados"""
    inspector = inspect(engine)
    
    # Tabelas esperadas
    tabelas_esperadas = [
        'trecho_rodoviario',
        'rodovia_estadualizacao', 
        'dispositivo_estadualizacao',
        'obra_arte_estadualizacao'
    ]
    
    print("=== VERIFICAÇÃO DE TABELAS ===")
    
    # Verificar no schema 'public'
    tabelas_public = inspector.get_table_names(schema='public')
    print(f"Tabelas no schema 'public': {tabelas_public}")
    
    # Verificar no schema 'Elementos_rodoviarios'
    try:
        tabelas_elementos = inspector.get_table_names(schema='Elementos_rodoviarios')
        print(f"Tabelas no schema 'Elementos_rodoviarios': {tabelas_elementos}")
    except Exception as e:
        print(f"Erro ao acessar schema 'Elementos_rodoviarios': {e}")
        tabelas_elementos = []
    
    # Verificar todas as tabelas disponíveis
    schemas = inspector.get_schema_names()
    print(f"Schemas disponíveis: {schemas}")
    
    for schema in schemas:
        try:
            tabelas = inspector.get_table_names(schema=schema)
            if tabelas:
                print(f"Schema '{schema}': {tabelas}")
        except Exception as e:
            print(f"Erro ao acessar schema '{schema}': {e}")
    
    return tabelas_public + tabelas_elementos

def criar_dados_trecho_rodoviario():
    """Cria dados fictícios para a tabela trecho_rodoviario"""
    print("\n=== CRIANDO DADOS FICTÍCIOS - TRECHO RODOVIÁRIO ===")
    
    db = next(get_db())
    
    try:
        # Verificar se já existem dados
        count = db.query(TrechoEstadualizacao).count()
        print(f"Registros existentes em trecho_rodoviario: {count}")
        
        if count == 0:
            trechos_ficticios = [
                TrechoEstadualizacao(
                    codigo="TR-001",
                    denominacao="Trecho SP-001 - Km 0 ao Km 10",
                    tipo="principal",
                    municipio="São Paulo",
                    extensao=10.0,
                    material="asfalto",
                    criado_em=datetime.now()
                ),
                TrechoEstadualizacao(
                    codigo="TR-002", 
                    denominacao="Trecho SP-002 - Km 10 ao Km 25",
                    tipo="secundario",
                    municipio="Guarulhos",
                    extensao=15.0,
                    material="concreto",
                    criado_em=datetime.now()
                ),
                TrechoEstadualizacao(
                    codigo="TR-003",
                    denominacao="Trecho SP-003 - Km 25 ao Km 40", 
                    tipo="marginal",
                    municipio="São Caetano do Sul",
                    extensao=15.0,
                    material="asfalto",
                    criado_em=datetime.now()
                )
            ]
            
            for trecho in trechos_ficticios:
                db.add(trecho)
            
            db.commit()
            print(f"✅ Criados {len(trechos_ficticios)} trechos rodoviários fictícios")
        else:
            print("✅ Trechos rodoviários já existem")
            
    except Exception as e:
        print(f"❌ Erro ao criar trechos rodoviários: {e}")
        db.rollback()
    finally:
        db.close()

def criar_dados_rodovia():
    """Cria dados fictícios para a tabela rodovia_estadualizacao"""
    print("\n=== CRIANDO DADOS FICTÍCIOS - RODOVIA ===")
    
    db = next(get_db())
    
    try:
        # Verificar se já existem dados
        count = db.query(RodoviaEstadualizacao).count()
        print(f"Registros existentes em rodovia_estadualizacao: {count}")
        
        if count == 0:
            rodovias_ficticias = [
                RodoviaEstadualizacao(
                    codigo="RO-001",
                    nome="Rodovia Presidente Dutra",
                    tipo="federal",
                    uf="SP",
                    municipio="São Paulo",
                    extensao_km=402.0
                ),
                RodoviaEstadualizacao(
                    codigo="RO-002",
                    nome="Rodovia Anhanguera", 
                    tipo="estadual",
                    uf="SP",
                    municipio="São Paulo",
                    extensao_km=331.0
                ),
                RodoviaEstadualizacao(
                    codigo="RO-003",
                    nome="Rodovia Bandeirantes",
                    tipo="estadual",
                    uf="SP", 
                    municipio="São Paulo",
                    extensao_km=201.0
                )
            ]
            
            for rodovia in rodovias_ficticias:
                db.add(rodovia)
            
            db.commit()
            print(f"✅ Criadas {len(rodovias_ficticias)} rodovias fictícias")
        else:
            print("✅ Rodovias já existem")
            
    except Exception as e:
        print(f"❌ Erro ao criar rodovias: {e}")
        db.rollback()
    finally:
        db.close()

def criar_dados_dispositivo():
    """Cria dados fictícios para a tabela dispositivo_estadualizacao"""
    print("\n=== CRIANDO DADOS FICTÍCIOS - DISPOSITIVO ===")
    
    db = next(get_db())
    
    try:
        # Verificar se já existem dados
        count = db.query(DispositivoEstadualizacao).count()
        print(f"Registros existentes em dispositivo_estadualizacao: {count}")
        
        if count == 0:
            dispositivos_ficticios = [
                DispositivoEstadualizacao(
                    codigo="DI-001",
                    denominacao="Dispositivo de Acesso Norte",
                    tipo="acesso",
                    municipio="São Paulo",
                    localizacao="Km 10"
                ),
                DispositivoEstadualizacao(
                    codigo="DI-002",
                    denominacao="Dispositivo de Retorno Sul",
                    tipo="retorno",
                    municipio="Guarulhos", 
                    localizacao="Km 25"
                ),
                DispositivoEstadualizacao(
                    codigo="DI-003",
                    denominacao="Dispositivo de Interseção Leste",
                    tipo="intersecao",
                    municipio="São Caetano do Sul",
                    localizacao="Km 40"
                )
            ]
            
            for dispositivo in dispositivos_ficticios:
                db.add(dispositivo)
            
            db.commit()
            print(f"✅ Criados {len(dispositivos_ficticios)} dispositivos fictícios")
        else:
            print("✅ Dispositivos já existem")
            
    except Exception as e:
        print(f"❌ Erro ao criar dispositivos: {e}")
        db.rollback()
    finally:
        db.close()

def criar_dados_obra_arte():
    """Cria dados fictícios para a tabela obra_arte_estadualizacao"""
    print("\n=== CRIANDO DADOS FICTÍCIOS - OBRA DE ARTE ===")
    
    db = next(get_db())
    
    try:
        # Verificar se já existem dados
        count = db.query(ObraArteEstadualizacao).count()
        print(f"Registros existentes em obra_arte_estadualizacao: {count}")
        
        if count == 0:
            obras_ficticias = [
                ObraArteEstadualizacao(
                    codigo="OA-001",
                    denominacao="Ponte sobre Rio Tietê",
                    tipo="ponte",
                    municipio="São Paulo",
                    extensao_m=120.0
                ),
                ObraArteEstadualizacao(
                    codigo="OA-002", 
                    denominacao="Viaduto do Ibirapuera",
                    tipo="viaduto",
                    municipio="São Paulo",
                    extensao_m=85.0
                ),
                ObraArteEstadualizacao(
                    codigo="OA-003",
                    denominacao="Túnel Ayrton Senna",
                    tipo="tunel",
                    municipio="São Paulo", 
                    extensao_m=200.0
                ),
                ObraArteEstadualizacao(
                    codigo="OA-004",
                    denominacao="Passarela Pedestre Centro",
                    tipo="passarela",
                    municipio="São Paulo",
                    extensao_m=45.0
                )
            ]
            
            for obra in obras_ficticias:
                db.add(obra)
            
            db.commit()
            print(f"✅ Criadas {len(obras_ficticias)} obras de arte fictícias")
        else:
            print("✅ Obras de arte já existem")
            
    except Exception as e:
        print(f"❌ Erro ao criar obras de arte: {e}")
        db.rollback()
    finally:
        db.close()

def verificar_dados_criados():
    """Verifica se os dados foram criados corretamente"""
    print("\n=== VERIFICAÇÃO FINAL DOS DADOS ===")
    
    db = next(get_db())
    
    try:
        # Contar registros em cada tabela
        count_trechos = db.query(TrechoEstadualizacao).count()
        count_rodovias = db.query(RodoviaEstadualizacao).count()
        count_dispositivos = db.query(DispositivoEstadualizacao).count()
        count_obras = db.query(ObraArteEstadualizacao).count()
        
        print(f"📊 Trechos Rodoviários: {count_trechos} registros")
        print(f"📊 Rodovias: {count_rodovias} registros")
        print(f"📊 Dispositivos: {count_dispositivos} registros") 
        print(f"📊 Obras de Arte: {count_obras} registros")
        
        # Mostrar alguns exemplos
        if count_trechos > 0:
            trecho = db.query(TrechoEstadualizacao).first()
            print(f"   Exemplo trecho: {trecho.codigo} - {trecho.denominacao}")
            
        if count_rodovias > 0:
            rodovia = db.query(RodoviaEstadualizacao).first()
            print(f"   Exemplo rodovia: {rodovia.codigo} - {rodovia.denominacao}")
            
        if count_dispositivos > 0:
            dispositivo = db.query(DispositivoEstadualizacao).first()
            print(f"   Exemplo dispositivo: {dispositivo.codigo} - {dispositivo.denominacao}")
            
        if count_obras > 0:
            obra = db.query(ObraArteEstadualizacao).first()
            print(f"   Exemplo obra: {obra.codigo} - {obra.denominacao}")
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
    finally:
        db.close()

def main():
    """Função principal"""
    print("🚀 INICIANDO CRIAÇÃO DE DADOS FICTÍCIOS PARA ELEMENTOS RODOVIÁRIOS")
    print("=" * 80)
    
    try:
        # Verificar tabelas
        tabelas = verificar_tabelas_existem()
        
        # Criar dados fictícios
        criar_dados_trecho_rodoviario()
        criar_dados_rodovia()
        criar_dados_dispositivo()
        criar_dados_obra_arte()
        
        # Verificar resultados
        verificar_dados_criados()
        
        print("\n" + "=" * 80)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("✅ Dados fictícios criados para todos os elementos rodoviários")
        print("✅ Agora você pode executar os testes novamente")
        
    except Exception as e:
        print(f"\n❌ ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
