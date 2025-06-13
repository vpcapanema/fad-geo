"""
Diagnóstico do Sistema de Cadastro - Verificação de PDFs
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.getcwd())

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("🔧 VERIFICANDO DEPENDÊNCIAS...")
    print("=" * 50)
    
    dependencias = {
        'pdfkit': 'Geração de PDF',
        'reportlab': 'Criação de PDF (alternativa)',
        'jinja2': 'Templates HTML'
    }
    
    instaladas = []
    faltando = []
    
    for dep, desc in dependencias.items():
        try:
            __import__(dep)
            print(f"✅ {dep} - {desc}")
            instaladas.append(dep)
        except ImportError:
            print(f"❌ {dep} - {desc} (NÃO INSTALADO)")
            faltando.append(dep)
    
    print(f"\n📊 Resumo: {len(instaladas)} instaladas, {len(faltando)} faltando")
    
    if faltando:
        print("\n💡 Para instalar dependências faltando:")
        for dep in faltando:
            print(f"   pip install {dep}")
    
    return len(faltando) == 0

def verificar_wkhtmltopdf():
    """Verifica se wkhtmltopdf está instalado (necessário para pdfkit)"""
    print("\n🔧 VERIFICANDO WKHTMLTOPDF...")
    print("=" * 50)
    
    try:
        import pdfkit
        config = pdfkit.configuration()
        
        # Tenta encontrar wkhtmltopdf
        wkhtml_path = None
        possible_paths = [
            r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
            r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
            "wkhtmltopdf"  # Se estiver no PATH
        ]
        
        for path in possible_paths:
            if os.path.exists(path) or path == "wkhtmltopdf":
                try:
                    # Testa se funciona
                    test_config = pdfkit.configuration(wkhtmltopdf=path if path != "wkhtmltopdf" else None)
                    wkhtml_path = path
                    print(f"✅ wkhtmltopdf encontrado: {path}")
                    break
                except:
                    continue
        
        if not wkhtml_path:
            print("❌ wkhtmltopdf NÃO ENCONTRADO")
            print("\n💡 Para instalar wkhtmltopdf:")
            print("   1. Baixe de: https://wkhtmltopdf.org/downloads.html")
            print("   2. Instale o executável")
            print("   3. Adicione ao PATH do sistema")
            return False
        
        return True
        
    except ImportError:
        print("❌ pdfkit não instalado")
        return False

def verificar_diretorio_formularios():
    """Verifica diretório onde os formulários são salvos"""
    print("\n📁 VERIFICANDO DIRETÓRIO DE FORMULÁRIOS...")
    print("=" * 50)
    
    base_dir = Path("formularios_cadastro")
    
    print(f"📍 Diretório base: {base_dir.absolute()}")
    
    if base_dir.exists():
        print("✅ Diretório existe")
        
        # Lista arquivos existentes
        arquivos = list(base_dir.rglob("*"))
        pdfs = [f for f in arquivos if f.suffix.lower() == '.pdf']
        htmls = [f for f in arquivos if f.suffix.lower() == '.html']
        
        print(f"📊 Arquivos encontrados:")
        print(f"   📄 HTMLs: {len(htmls)}")
        print(f"   📑 PDFs: {len(pdfs)}")
        
        # Mostra os 5 mais recentes
        if pdfs:
            print(f"\n📑 PDFs mais recentes:")
            pdfs_sorted = sorted(pdfs, key=lambda x: x.stat().st_mtime, reverse=True)
            for i, pdf in enumerate(pdfs_sorted[:5], 1):
                tamanho = pdf.stat().st_size
                print(f"   {i}. {pdf.name} ({tamanho} bytes)")
        
        return True
    else:
        print("⚠️ Diretório não existe (será criado no primeiro cadastro)")
        return True

def verificar_template_cadastro():
    """Verifica se o template de cadastro existe"""
    print("\n📄 VERIFICANDO TEMPLATE DE CADASTRO...")
    print("=" * 50)
    
    template_path = Path("app/templates/formularios_cadastro_usuarios/cadastro_usuario_template.html")
    
    print(f"📍 Template: {template_path}")
    
    if template_path.exists():
        print("✅ Template existe")
        tamanho = template_path.stat().st_size
        print(f"📏 Tamanho: {tamanho} bytes")
        
        # Verifica se tem conteúdo básico
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if '{{usuario' in content and '{{pessoa_fisica' in content:
                print("✅ Template tem variáveis necessárias")
            else:
                print("⚠️ Template pode estar incompleto")
                
        except Exception as e:
            print(f"❌ Erro ao ler template: {e}")
            
        return True
    else:
        print("❌ Template NÃO ENCONTRADO")
        print("💡 O template é necessário para gerar o HTML do comprovante")
        return False

def testar_geracao_pdf_simples():
    """Testa geração de PDF simples"""
    print("\n🧪 TESTANDO GERAÇÃO DE PDF...")
    print("=" * 50)
    
    try:
        import pdfkit
        import tempfile
        
        # HTML de teste
        html_teste = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Teste PDF</title>
        </head>
        <body>
            <h1>Teste de Geração de PDF</h1>
            <p>Este é um teste para verificar se o pdfkit está funcionando.</p>
            <p>Data: 10/06/2025</p>
        </body>
        </html>
        """
        
        # Cria arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_teste)
            html_path = f.name
        
        # Tenta gerar PDF
        pdf_path = html_path.replace('.html', '.pdf')
        
        options = {
            'page-size': 'A4',
            'encoding': "UTF-8",
            'no-outline': None
        }
        
        pdfkit.from_file(html_path, pdf_path, options=options)
        
        if os.path.exists(pdf_path):
            tamanho = os.path.getsize(pdf_path)
            print(f"✅ PDF gerado com sucesso")
            print(f"📏 Tamanho: {tamanho} bytes")
            
            # Limpeza
            os.unlink(html_path)
            os.unlink(pdf_path)
            
            return True
        else:
            print("❌ PDF não foi criado")
            return False
            
    except Exception as e:
        print(f"❌ Erro na geração de PDF: {e}")
        print("\n💡 Possíveis soluções:")
        print("   1. Instalar wkhtmltopdf")
        print("   2. Verificar PATH do sistema")
        print("   3. Reinstalar pdfkit: pip install pdfkit")
        return False

def main():
    """Função principal de diagnóstico"""
    print("🔬 DIAGNÓSTICO DO SISTEMA DE CADASTRO - PDFs")
    print("=" * 60)
    
    resultados = {}
    
    # Executa todos os testes
    resultados['dependencias'] = verificar_dependencias()
    resultados['wkhtmltopdf'] = verificar_wkhtmltopdf()
    resultados['diretorio'] = verificar_diretorio_formularios()
    resultados['template'] = verificar_template_cadastro()
    resultados['geracao_pdf'] = testar_geracao_pdf_simples()
    
    # Resumo final
    print("\n🎯 RESUMO DO DIAGNÓSTICO")
    print("=" * 60)
    
    for teste, resultado in resultados.items():
        status = "✅ OK" if resultado else "❌ PROBLEMA"
        print(f"{teste.capitalize():15} {status}")
    
    testes_ok = sum(resultado for resultado in resultados.values())
    total_testes = len(resultados)
    
    print(f"\n📊 RESULTADO: {testes_ok}/{total_testes} testes passaram")
    
    if testes_ok == total_testes:
        print("\n🎉 SISTEMA DE PDFs ESTÁ FUNCIONANDO!")
        print("✅ O problema pode estar em outro lugar:")
        print("   - Verificar logs do sistema de cadastro")
        print("   - Verificar se o email está chegando completo")
        print("   - Verificar configurações do cliente de email")
    else:
        print("\n⚠️ PROBLEMAS ENCONTRADOS")
        print("🔧 Corrija os itens marcados como PROBLEMA")
        
        if not resultados['wkhtmltopdf']:
            print("\n🚨 PROBLEMA CRÍTICO: wkhtmltopdf")
            print("   Sem wkhtmltopdf, os PDFs não podem ser gerados")
            print("   Baixe e instale de: https://wkhtmltopdf.org/downloads.html")

if __name__ == "__main__":
    main()
