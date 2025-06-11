"""
Teste do Sistema Completo de Recuperação de Senha - FAD
Verifica todos os componentes do sistema
"""

import os
import sys
import time
import logging
from pathlib import Path

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def verificar_arquivos_sistema():
    """Verifica se todos os arquivos necessários existem"""
    print("\n🔍 VERIFICANDO ARQUIVOS DO SISTEMA...")
    print("=" * 60)
    
    arquivos_obrigatorios = [
        "app/api/endpoints/au_recuperacao_senha.py",
        "app/services/email_service.py",
        "app/api/endpoints/cd_cadastro_usuario_sistema.py",
        "monitorar_emails.py",
        "sistema_backup_configuracoes.py",
        ".env"
    ]
    
    templates_obrigatorios = [
        "app/templates/au_recuperar_senha.html",
        "app/templates/au_redefinir_senha.html", 
        "app/templates/au_email_enviado.html",
        "app/templates/au_senha_alterada.html",
        "app/templates/au_token_invalido.html"
    ]
    
    todos_ok = True
    
    for arquivo in arquivos_obrigatorios:
        caminho = Path(arquivo)
        if caminho.exists():
            tamanho = caminho.stat().st_size
            print(f"✅ {arquivo} - {tamanho} bytes")
        else:
            print(f"❌ {arquivo} - ARQUIVO FALTANDO!")
            todos_ok = False
    
    print("\n📄 TEMPLATES HTML:")
    for template in templates_obrigatorios:
        caminho = Path(template)
        if caminho.exists():
            tamanho = caminho.stat().st_size
            print(f"✅ {template} - {tamanho} bytes")
        else:
            print(f"❌ {template} - TEMPLATE FALTANDO!")
            todos_ok = False
    
    return todos_ok

def verificar_configuracoes_env():
    """Verifica configurações do arquivo .env"""
    print("\n⚙️ VERIFICANDO CONFIGURAÇÕES DO .env...")
    print("=" * 60)
    
    configuracoes_necessarias = [
        "SMTP_SERVER",
        "SMTP_PORT", 
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
        "SMTP_FROM_EMAIL",
        "SMTP_FROM_NAME",
        "ENVIRONMENT"
    ]
    
    todas_ok = True
    
    for config in configuracoes_necessarias:
        valor = os.getenv(config)
        if valor:
            if config == "SMTP_PASSWORD":
                if valor in ["", "sua_senha_de_app_aqui", "Malditas131533*", "DESENVOLVIMENTO"]:
                    print(f"⚠️ {config} = VALOR PADRÃO (configure senha real)")
                else:
                    print(f"✅ {config} = {'*' * len(valor)} (configurado)")
            else:
                print(f"✅ {config} = {valor}")
        else:
            print(f"❌ {config} = NÃO CONFIGURADO")
            todas_ok = False
    
    return todas_ok

def testar_importacoes():
    """Testa se todos os módulos podem ser importados"""
    print("\n📦 TESTANDO IMPORTAÇÕES...")
    print("=" * 60)
    
    imports_ok = True
    
    try:
        # Adiciona o diretório atual ao path
        sys.path.insert(0, os.getcwd())
        
        # Testa importação do email service
        from app.services.email_service import email_service
        print("✅ EmailService importado com sucesso")
        
        # Testa configuração do email service
        if email_service.testar_configuracao():
            print("✅ Configuração de email válida")
        else:
            print("⚠️ Configuração de email com problemas (modo desenvolvimento ativo)")
            
    except Exception as e:
        print(f"❌ Erro ao importar EmailService: {e}")
        imports_ok = False
    
    try:
        # Testa importação do monitor
        from monitorar_emails import email_monitor
        print("✅ Monitor de emails importado com sucesso")
        
    except Exception as e:
        print(f"❌ Erro ao importar Monitor: {e}")
        imports_ok = False
    
    try:
        # Testa importação do sistema de backup
        from sistema_backup_configuracoes import SistemaBackupConfiguracoes
        backup_system = SistemaBackupConfiguracoes()
        print("✅ Sistema de backup importado com sucesso")
        
    except Exception as e:
        print(f"❌ Erro ao importar Sistema de Backup: {e}")
        imports_ok = False
    
    return imports_ok

def testar_envio_email_simulado():
    """Testa envio de email em modo simulado"""
    print("\n📧 TESTANDO ENVIO DE EMAIL (SIMULADO)...")
    print("=" * 60)
    
    try:
        sys.path.insert(0, os.getcwd())
        from app.services.email_service import email_service
        
        # Testa email de recuperação
        print("🔄 Testando email de recuperação de senha...")
        resultado = email_service.enviar_email_recuperacao_senha(
            destinatario_email="vpcapanema@der.sp.gov.br",
            destinatario_nome="Vinícius Capanema",
            token_recuperacao="abc123",
            base_url="http://localhost:8000",
            ip_origem="127.0.0.1",
            user_agent="TestAgent"
        )
        
        if resultado:
            print("✅ Email de recuperação testado com sucesso")
        else:
            print("❌ Falha no teste de email de recuperação")
            return False
        
        # Testa email de confirmação
        print("\n🔄 Testando email de confirmação de cadastro...")
        resultado = email_service.enviar_email_confirmacao_cadastro(
            destinatario_email="vpcapanema@der.sp.gov.br",
            destinatario_nome="Vinícius Capanema",
            comprovante_pdf_path="teste.pdf",
            dados_cadastro={"nome": "Vinícius Capanema", "tipo": "administrador", "cpf": "123.456.789-00"},
            ip_origem="127.0.0.1",
            user_agent="TestAgent"
        )
        
        if resultado:
            print("✅ Email de confirmação testado com sucesso")
        else:
            print("❌ Falha no teste de email de confirmação")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de email: {e}")
        return False

def testar_sistema_backup():
    """Testa sistema de backup"""
    print("\n💾 TESTANDO SISTEMA DE BACKUP...")
    print("=" * 60)
    
    try:
        from sistema_backup_configuracoes import SistemaBackupConfiguracoes
        
        backup_system = SistemaBackupConfiguracoes()
        
        # Testa criação de backup das configurações
        print("🔄 Testando backup das configurações...")
        resultado = backup_system.backup_configuracoes_sistema()
        
        if resultado:
            print(f"✅ Backup das configurações criado: {Path(resultado).name}")
        else:
            print("❌ Falha ao criar backup das configurações")
            return False
        
        # Testa listagem de backups
        print("\n🔄 Testando listagem de backups...")
        backups = backup_system.listar_backups()
        print(f"✅ {len(backups)} backups encontrados")
        
        # Testa relatório
        print("\n🔄 Testando relatório de backups...")
        relatorio = backup_system.relatorio_backups()
        
        if "erro" not in relatorio:
            print("✅ Relatório de backups gerado com sucesso")
            print(f"   Total de backups: {relatorio['total_backups']}")
            print(f"   Espaço utilizado: {relatorio['espaco_utilizado']}")
        else:
            print(f"❌ Erro no relatório: {relatorio['erro']}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de backup: {e}")
        return False

def testar_monitor_emails():
    """Testa sistema de monitoramento de emails"""
    print("\n📊 TESTANDO MONITOR DE EMAILS...")
    print("=" * 60)
    
    try:
        from monitorar_emails import email_monitor
        
        # Testa registro de envio
        print("🔄 Testando registro de envio...")
        email_monitor.registrar_envio(
            tipo_email="teste",
            destinatario="teste@example.com",
            remetente="sistema@test.com",
            assunto="Teste de Sistema",
            status="teste",
            tempo_processamento_ms=100
        )
        print("✅ Registro de envio testado com sucesso")
        
        # Testa geração de relatório
        print("\n🔄 Testando relatório de emails...")
        relatorio = email_monitor.gerar_relatorio()
        
        if relatorio:
            print("✅ Relatório de emails gerado com sucesso")
            print(f"   Total de envios: {relatorio.get('total_envios', 0)}")
        else:
            print("❌ Falha ao gerar relatório")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de monitor: {e}")
        return False

def gerar_relatorio_final():
    """Gera relatório final do teste"""
    print("\n📋 RELATÓRIO FINAL DO SISTEMA")
    print("=" * 60)
    
    # Informações do ambiente
    print(f"🔧 Ambiente: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🔌 SMTP Configurado: {'Sim' if os.getenv('SMTP_PASSWORD') else 'Não'}")
    print(f"📁 Diretório: {os.getcwd()}")
    print(f"🐍 Python: {sys.version}")
    
    # Estatísticas dos arquivos
    total_arquivos = 0
    tamanho_total = 0
    
    arquivos_projeto = [
        "app/api/endpoints/au_recuperacao_senha.py",
        "app/services/email_service.py", 
        "app/api/endpoints/cd_cadastro_usuario_sistema.py",
        "monitorar_emails.py",
        "sistema_backup_configuracoes.py"
    ]
    
    for arquivo in arquivos_projeto:
        caminho = Path(arquivo)
        if caminho.exists():
            total_arquivos += 1
            tamanho_total += caminho.stat().st_size
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Arquivos principais: {total_arquivos}")
    print(f"   Tamanho total: {tamanho_total:,} bytes")
    
    # Verifica se há logs
    if Path("email_logs.db").exists():
        tamanho_logs = Path("email_logs.db").stat().st_size
        print(f"   Banco de logs: {tamanho_logs:,} bytes")
    
    # Verifica backups
    diretorio_backup = Path("backups_configuracao")
    if diretorio_backup.exists():
        backups = list(diretorio_backup.glob("*"))
        print(f"   Backups disponíveis: {len(backups)}")

def main():
    """Função principal de teste"""
    print("🧪 TESTE COMPLETO DO SISTEMA DE RECUPERAÇÃO DE SENHA - FAD")
    print("=" * 70)
    print(f"⏰ Iniciado em: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    
    resultados = {}
    
    # Executa todos os testes
    resultados["arquivos"] = verificar_arquivos_sistema()
    resultados["configuracoes"] = verificar_configuracoes_env()
    resultados["importacoes"] = testar_importacoes()
    resultados["email"] = testar_envio_email_simulado()
    resultados["backup"] = testar_sistema_backup()
    resultados["monitor"] = testar_monitor_emails()
    
    # Calcula resultados
    total_testes = len(resultados)
    testes_ok = sum(1 for resultado in resultados.values() if resultado)
    
    print("\n🎯 RESUMO DOS TESTES")
    print("=" * 60)
    
    for nome, resultado in resultados.items():
        status = "✅ APROVADO" if resultado else "❌ REPROVADO"
        print(f"{nome.capitalize():15} {status}")
    
    print(f"\n📊 RESULTADO GERAL: {testes_ok}/{total_testes} testes aprovados")
    
    if testes_ok == total_testes:
        print("🎉 SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("\n✅ Próximos passos:")
        print("   1. Configure SMTP_PASSWORD para produção")
        print("   2. Execute o sistema em ambiente de produção")
        print("   3. Monitore os logs de email")
        print("   4. Faça backups regulares")
    else:
        print("⚠️ SISTEMA COM PROBLEMAS - Verifique os itens reprovados")
    
    gerar_relatorio_final()
    
    print(f"\n⏰ Concluído em: {time.strftime('%d/%m/%Y %H:%M:%S')}")

if __name__ == "__main__":
    main()
