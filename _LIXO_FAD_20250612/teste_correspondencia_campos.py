#!/usr/bin/env python3
"""
Teste de Correspondência de Campos - Sistema de Cadastro de Usuário
================================================================

Este script verifica a correspondência entre:
1. Campos do formulário de interface (cd_cadastro_usuario.html)
2. Campos do formulário de envio oculto (cd_cadastro_usuario_envio.html)  
3. Campos do modelo de banco de dados (UsuarioSistema)
4. Campos do schema Pydantic (UsuarioCreate)
5. Lógica JavaScript de cópia de campos

"""

import re
import json
from pathlib import Path

def extrair_campos_html(arquivo_html, tipo_form="interface"):
    """Extrai campos de um arquivo HTML"""
    try:
        with open(arquivo_html, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        campos = set()
        
        if tipo_form == "interface":
            # Campos de interface (não ocultos)
            patterns = [
                r'<input[^>]*name="([^"]+)"[^>]*(?!type="hidden")',
                r'<select[^>]*name="([^"]+)"',
                r'<textarea[^>]*name="([^"]+)"'
            ]
        else:
            # Campos de envio (todos os campos)
            patterns = [
                r'<input[^>]*name="([^"]+)"',
                r'<select[^>]*name="([^"]+)"',
                r'<textarea[^>]*name="([^"]+)"'
            ]
        
        for pattern in patterns:
            matches = re.findall(pattern, conteudo, re.IGNORECASE)
            campos.update(matches)
            
        return campos
    except Exception as e:
        print(f"❌ Erro ao ler {arquivo_html}: {e}")
        return set()

def extrair_campos_javascript(arquivo_html):
    """Extrai campos da lógica JavaScript de cópia"""
    try:
        with open(arquivo_html, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Busca a lista de campos no JavaScript
        match = re.search(r'const campos = \[(.*?)\];', conteudo, re.DOTALL)
        if match:
            campos_str = match.group(1)
            # Extrai strings entre aspas
            campos = re.findall(r"'([^']+)'", campos_str)
            return set(campos)
        return set()
    except Exception as e:
        print(f"❌ Erro ao extrair campos JavaScript: {e}")
        return set()

def extrair_campos_modelo():
    """Extrai campos do modelo UsuarioSistema"""
    try:
        with open('app/models/cd_usuario_sistema.py', 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        campos = set()
        # Busca definições de colunas
        matches = re.findall(r'(\w+)\s*=\s*Column\(', conteudo)
        campos.update(matches)
        
        return campos
    except Exception as e:
        print(f"❌ Erro ao ler modelo: {e}")
        return set()

def extrair_campos_schema():
    """Extrai campos do schema UsuarioCreate"""
    try:
        with open('app/schemas/usuario.py', 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Busca a classe UsuarioCreate
        match = re.search(r'class UsuarioCreate\(BaseModel\):(.*?)(?=class|\Z)', conteudo, re.DOTALL)
        if match:
            classe_conteudo = match.group(1)
            # Extrai campos (nome: tipo)
            campos = re.findall(r'^\s*(\w+)\s*:', classe_conteudo, re.MULTILINE)
            return set(campos)
        return set()
    except Exception as e:
        print(f"❌ Erro ao ler schema: {e}")
        return set()

def extrair_campos_envio_oculto(arquivo_html):
    """Extrai especificamente os campos de envio oculto (inputs hidden)"""
    try:
        with open(arquivo_html, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        campos = set()
        # Busca inputs hidden com id="envio_*"
        matches = re.findall(r'<input[^>]*type="hidden"[^>]*name="([^"]+)"', conteudo)
        campos.update(matches)
        
        return campos
    except Exception as e:
        print(f"❌ Erro ao extrair campos de envio oculto: {e}")
        return set()

def main():
    print("🔍 TESTE DE CORRESPONDÊNCIA DE CAMPOS")
    print("=" * 50)
    
    # Extrair campos de cada fonte
    print("\n📋 Extraindo campos de cada fonte...")
    
    # 1. Formulário de interface
    campos_interface = extrair_campos_html('app/templates/cd_cadastro_usuario.html', 'interface')
    print(f"✅ Interface: {len(campos_interface)} campos")
    
    # 2. Formulário de envio
    campos_envio_form = extrair_campos_html('app/templates/cd_cadastro_usuario_envio.html', 'envio')
    print(f"✅ Envio (form): {len(campos_envio_form)} campos")
    
    # 3. Campos de envio oculto
    campos_envio_oculto = extrair_campos_envio_oculto('app/templates/cd_cadastro_usuario.html')
    print(f"✅ Envio (oculto): {len(campos_envio_oculto)} campos")
    
    # 4. JavaScript
    campos_javascript = extrair_campos_javascript('app/templates/cd_cadastro_usuario.html')
    print(f"✅ JavaScript: {len(campos_javascript)} campos")
    
    # 5. Modelo de banco
    campos_modelo = extrair_campos_modelo()
    print(f"✅ Modelo BD: {len(campos_modelo)} campos")
    
    # 6. Schema Pydantic
    campos_schema = extrair_campos_schema()
    print(f"✅ Schema: {len(campos_schema)} campos")
    
    print("\n📊 ANÁLISE DE CORRESPONDÊNCIA")
    print("=" * 50)
    
    # Todos os campos únicos
    todos_campos = campos_interface | campos_envio_form | campos_envio_oculto | campos_javascript | campos_modelo | campos_schema
    
    print(f"\n🔢 Total de campos únicos encontrados: {len(todos_campos)}")
    
    # Análise detalhada
    print("\n📋 CAMPOS POR FONTE:")
    print("-" * 30)
    
    print(f"\n🎯 Interface ({len(campos_interface)}):")
    for campo in sorted(campos_interface):
        print(f"   - {campo}")
    
    print(f"\n📤 Envio Form ({len(campos_envio_form)}):")
    for campo in sorted(campos_envio_form):
        print(f"   - {campo}")
        
    print(f"\n🔒 Envio Oculto ({len(campos_envio_oculto)}):")
    for campo in sorted(campos_envio_oculto):
        print(f"   - {campo}")
    
    print(f"\n⚙️ JavaScript ({len(campos_javascript)}):")
    for campo in sorted(campos_javascript):
        print(f"   - {campo}")
    
    print(f"\n🗄️ Modelo BD ({len(campos_modelo)}):")
    for campo in sorted(campos_modelo):
        print(f"   - {campo}")
    
    print(f"\n📋 Schema ({len(campos_schema)}):")
    for campo in sorted(campos_schema):
        print(f"   - {campo}")
    
    # Verificação de inconsistências
    print("\n🚨 VERIFICAÇÃO DE INCONSISTÊNCIAS")
    print("=" * 50)
    
    problemas = 0
    
    # 1. JavaScript vs Envio Oculto
    js_vs_oculto = campos_javascript - campos_envio_oculto
    if js_vs_oculto:
        problemas += 1
        print(f"\n❌ Campos no JS mas não no envio oculto: {js_vs_oculto}")
    
    oculto_vs_js = campos_envio_oculto - campos_javascript
    if oculto_vs_js:
        problemas += 1
        print(f"\n❌ Campos no envio oculto mas não no JS: {oculto_vs_js}")
    
    # 2. Interface vs JavaScript
    interface_vs_js = campos_interface - campos_javascript
    if interface_vs_js:
        problemas += 1
        print(f"\n⚠️ Campos na interface mas não no JS: {interface_vs_js}")
    
    # 3. Schema vs Modelo
    schema_vs_modelo = campos_schema - campos_modelo
    if schema_vs_modelo:
        problemas += 1
        print(f"\n❌ Campos no schema mas não no modelo: {schema_vs_modelo}")
    
    modelo_vs_schema = campos_modelo - campos_schema
    if modelo_vs_schema:
        problemas += 1
        print(f"\n⚠️ Campos no modelo mas não no schema: {modelo_vs_schema}")
    
    # 4. Campos essenciais ausentes
    campos_essenciais = {'nome', 'cpf', 'email', 'tipo', 'senha'}
    ausentes = campos_essenciais - campos_schema
    if ausentes:
        problemas += 1
        print(f"\n❌ Campos essenciais ausentes do schema: {ausentes}")
    
    # Resultado final
    print(f"\n🎯 RESULTADO FINAL")
    print("=" * 30)
    
    if problemas == 0:
        print("✅ TODOS OS CAMPOS ESTÃO CONSISTENTES!")
        print("🎉 Sistema pronto para teste de funcionalidade!")
    else:
        print(f"❌ Encontrados {problemas} problemas de inconsistência.")
        print("🔧 Corrija os problemas antes de testar a funcionalidade.")
    
    # Estatísticas finais
    print(f"\n📊 ESTATÍSTICAS FINAIS:")
    print(f"   • Total de campos únicos: {len(todos_campos)}")
    print(f"   • Campos na interface: {len(campos_interface)}")
    print(f"   • Campos no envio: {len(campos_envio_oculto)}")
    print(f"   • Campos no JS: {len(campos_javascript)}")
    print(f"   • Campos no modelo: {len(campos_modelo)}")
    print(f"   • Campos no schema: {len(campos_schema)}")

if __name__ == "__main__":
    main()
