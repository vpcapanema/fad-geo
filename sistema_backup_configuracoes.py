"""
Sistema de Backup das Configurações - FAD
Realiza backup automático das configurações de email e do sistema
"""

import os
import shutil
import json
import datetime
import sqlite3
import zipfile
from pathlib import Path
import logging
from typing import Dict, List, Optional

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backup_configuracoes.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SistemaBackupConfiguracoes:
    def __init__(self, diretorio_fad: str = "c:\\Users\\vinic\\fad-geo"):
        self.diretorio_fad = Path(diretorio_fad)
        self.diretorio_backup = self.diretorio_fad / "backups_configuracao"
        self.criar_diretorio_backup()
        
    def criar_diretorio_backup(self):
        """Cria diretório de backup se não existir"""
        try:
            self.diretorio_backup.mkdir(exist_ok=True)
            logger.info(f"✅ Diretório de backup criado: {self.diretorio_backup}")
        except Exception as e:
            logger.error(f"❌ Erro ao criar diretório de backup: {e}")
            
    def obter_timestamp(self) -> str:
        """Retorna timestamp formatado para arquivos"""
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def backup_arquivo_env(self) -> Optional[str]:
        """Faz backup do arquivo .env"""
        try:
            arquivo_env = self.diretorio_fad / ".env"
            
            if not arquivo_env.exists():
                logger.warning("⚠️ Arquivo .env não encontrado")
                return None
                
            timestamp = self.obter_timestamp()
            nome_backup = f"env_backup_{timestamp}.env"
            caminho_backup = self.diretorio_backup / nome_backup
            
            shutil.copy2(arquivo_env, caminho_backup)
            logger.info(f"✅ Backup do .env criado: {nome_backup}")
            
            return str(caminho_backup)
            
        except Exception as e:
            logger.error(f"❌ Erro ao fazer backup do .env: {e}")
            return None
            
    def backup_logs_email(self) -> Optional[str]:
        """Faz backup do banco de dados de logs de email"""
        try:
            arquivo_logs = self.diretorio_fad / "email_logs.db"
            
            if not arquivo_logs.exists():
                logger.warning("⚠️ Arquivo de logs email_logs.db não encontrado")
                return None
                
            timestamp = self.obter_timestamp()
            nome_backup = f"email_logs_backup_{timestamp}.db"
            caminho_backup = self.diretorio_backup / nome_backup
            
            shutil.copy2(arquivo_logs, caminho_backup)
            logger.info(f"✅ Backup dos logs de email criado: {nome_backup}")
            
            return str(caminho_backup)
            
        except Exception as e:
            logger.error(f"❌ Erro ao fazer backup dos logs: {e}")
            return None
            
    def backup_configuracoes_sistema(self) -> Optional[str]:
        """Faz backup das configurações do sistema"""
        try:
            timestamp = self.obter_timestamp()
            
            # Coleta informações das configurações
            configuracoes = {
                "timestamp": datetime.datetime.now().isoformat(),
                "versao_backup": "1.0",
                "ambiente": os.getenv("ENVIRONMENT", "development"),
                "configuracoes_smtp": {
                    "servidor": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
                    "porta": os.getenv("SMTP_PORT", "587"),
                    "usuario": os.getenv("SMTP_USERNAME", ""),
                    "remetente": os.getenv("SMTP_FROM_EMAIL", ""),
                    "nome_remetente": os.getenv("SMTP_FROM_NAME", ""),
                    "senha_configurada": bool(os.getenv("SMTP_PASSWORD"))
                },
                "estrutura_projeto": self._obter_estrutura_projeto(),
                "estatisticas_logs": self._obter_estatisticas_logs()
            }
            
            nome_backup = f"configuracoes_sistema_{timestamp}.json"
            caminho_backup = self.diretorio_backup / nome_backup
            
            with open(caminho_backup, 'w', encoding='utf-8') as f:
                json.dump(configuracoes, f, indent=2, ensure_ascii=False)
                
            logger.info(f"✅ Backup das configurações do sistema criado: {nome_backup}")
            return str(caminho_backup)
            
        except Exception as e:
            logger.error(f"❌ Erro ao fazer backup das configurações: {e}")
            return None
            
    def _obter_estrutura_projeto(self) -> Dict:
        """Obtém informações sobre a estrutura do projeto"""
        try:
            estrutura = {
                "arquivos_principais": [],
                "templates_criados": [],
                "scripts_utilitarios": []
            }
            
            # Verifica arquivos principais
            arquivos_principais = [
                "app/api/endpoints/au_recuperacao_senha.py",
                "app/services/email_service.py",
                "app/api/endpoints/cd_cadastro_usuario_sistema.py"
            ]
            
            for arquivo in arquivos_principais:
                caminho = self.diretorio_fad / arquivo
                if caminho.exists():
                    estrutura["arquivos_principais"].append({
                        "arquivo": arquivo,
                        "existe": True,
                        "tamanho": caminho.stat().st_size,
                        "modificado": datetime.datetime.fromtimestamp(
                            caminho.stat().st_mtime
                        ).isoformat()
                    })
                else:
                    estrutura["arquivos_principais"].append({
                        "arquivo": arquivo,
                        "existe": False
                    })
            
            # Verifica templates
            templates_dir = self.diretorio_fad / "app" / "templates"
            if templates_dir.exists():
                for template in templates_dir.glob("au_*.html"):
                    estrutura["templates_criados"].append({
                        "nome": template.name,
                        "tamanho": template.stat().st_size
                    })
            
            # Verifica scripts utilitários
            scripts = [
                "monitorar_emails.py",
                "testar_recuperacao_senha.py",
                "configurar_gmail.py",
                "recuperar_minha_senha.py"
            ]
            
            for script in scripts:
                caminho = self.diretorio_fad / script
                if caminho.exists():
                    estrutura["scripts_utilitarios"].append({
                        "nome": script,
                        "existe": True,
                        "tamanho": caminho.stat().st_size
                    })
                    
            return estrutura
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter estrutura do projeto: {e}")
            return {}
            
    def _obter_estatisticas_logs(self) -> Dict:
        """Obtém estatísticas dos logs de email"""
        try:
            arquivo_logs = self.diretorio_fad / "email_logs.db"
            
            if not arquivo_logs.exists():
                return {"erro": "Banco de logs não encontrado"}
                
            conn = sqlite3.connect(arquivo_logs)
            cursor = conn.cursor()
            
            # Total de emails enviados
            cursor.execute("SELECT COUNT(*) FROM envios_email")
            total_envios = cursor.fetchone()[0]
            
            # Emails por tipo
            cursor.execute("""
                SELECT tipo_email, COUNT(*) 
                FROM envios_email 
                GROUP BY tipo_email
            """)
            por_tipo = dict(cursor.fetchall())
            
            # Emails por status
            cursor.execute("""
                SELECT status, COUNT(*) 
                FROM envios_email 
                GROUP BY status
            """)
            por_status = dict(cursor.fetchall())
            
            # Últimos 7 dias
            cursor.execute("""
                SELECT DATE(data_envio) as dia, COUNT(*) 
                FROM envios_email 
                WHERE data_envio >= datetime('now', '-7 days')
                GROUP BY DATE(data_envio)
                ORDER BY dia
            """)
            ultimos_7_dias = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                "total_envios": total_envios,
                "por_tipo": por_tipo,
                "por_status": por_status,
                "ultimos_7_dias": ultimos_7_dias
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas dos logs: {e}")
            return {"erro": str(e)}
            
    def backup_completo(self) -> Optional[str]:
        """Realiza backup completo de todas as configurações"""
        try:
            timestamp = self.obter_timestamp()
            nome_zip = f"backup_completo_fad_{timestamp}.zip"
            caminho_zip = self.diretorio_backup / nome_zip
            
            logger.info("🔄 Iniciando backup completo...")
            
            with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                
                # Backup do .env
                env_backup = self.backup_arquivo_env()
                if env_backup:
                    zipf.write(env_backup, f"env_backup_{timestamp}.env")
                    
                # Backup dos logs
                logs_backup = self.backup_logs_email()
                if logs_backup:
                    zipf.write(logs_backup, f"email_logs_backup_{timestamp}.db")
                    
                # Backup das configurações
                config_backup = self.backup_configuracoes_sistema()
                if config_backup:
                    zipf.write(config_backup, f"configuracoes_sistema_{timestamp}.json")
                    
                # Adiciona arquivos importantes do projeto
                arquivos_importantes = [
                    "app/api/endpoints/au_recuperacao_senha.py",
                    "app/api/endpoints/cd_cadastro_usuario_sistema.py",
                    "monitorar_emails.py",
                    "testar_recuperacao_senha.py",
                    "configurar_gmail.py"
                ]
                
                for arquivo in arquivos_importantes:
                    caminho_arquivo = self.diretorio_fad / arquivo
                    if caminho_arquivo.exists():
                        zipf.write(caminho_arquivo, arquivo)
                        
                # Adiciona templates
                templates_dir = self.diretorio_fad / "app" / "templates"
                if templates_dir.exists():
                    for template in templates_dir.glob("au_*.html"):
                        zipf.write(template, f"templates/{template.name}")
                        
            logger.info(f"✅ Backup completo criado: {nome_zip}")
            logger.info(f"📁 Tamanho: {self._formatar_tamanho(caminho_zip.stat().st_size)}")
            
            return str(caminho_zip)
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar backup completo: {e}")
            return None
            
    def _formatar_tamanho(self, tamanho_bytes: int) -> str:
        """Formata tamanho em bytes para formato legível"""
        for unidade in ['B', 'KB', 'MB', 'GB']:
            if tamanho_bytes < 1024.0:
                return f"{tamanho_bytes:.1f} {unidade}"
            tamanho_bytes /= 1024.0
        return f"{tamanho_bytes:.1f} TB"
        
    def listar_backups(self) -> List[Dict]:
        """Lista todos os backups disponíveis"""
        try:
            backups = []
            
            for arquivo in self.diretorio_backup.glob("*"):
                if arquivo.is_file():
                    info = {
                        "nome": arquivo.name,
                        "caminho": str(arquivo),
                        "tamanho": self._formatar_tamanho(arquivo.stat().st_size),
                        "data_criacao": datetime.datetime.fromtimestamp(
                            arquivo.stat().st_ctime
                        ).strftime("%d/%m/%Y %H:%M:%S"),
                        "tipo": self._identificar_tipo_backup(arquivo.name)
                    }
                    backups.append(info)
                    
            # Ordena por data de criação (mais recente primeiro)
            backups.sort(key=lambda x: x["data_criacao"], reverse=True)
            
            return backups
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar backups: {e}")
            return []
            
    def _identificar_tipo_backup(self, nome_arquivo: str) -> str:
        """Identifica o tipo de backup pelo nome do arquivo"""
        if "backup_completo" in nome_arquivo:
            return "Backup Completo (ZIP)"
        elif "env_backup" in nome_arquivo:
            return "Configurações ENV"
        elif "email_logs_backup" in nome_arquivo:
            return "Logs de Email"
        elif "configuracoes_sistema" in nome_arquivo:
            return "Configurações Sistema"
        else:
            return "Desconhecido"
            
    def restaurar_env(self, caminho_backup: str) -> bool:
        """Restaura arquivo .env de um backup"""
        try:
            if not Path(caminho_backup).exists():
                logger.error(f"❌ Arquivo de backup não encontrado: {caminho_backup}")
                return False
                
            arquivo_env_atual = self.diretorio_fad / ".env"
            
            # Faz backup do arquivo atual antes de restaurar
            if arquivo_env_atual.exists():
                timestamp = self.obter_timestamp()
                backup_atual = self.diretorio_backup / f"env_backup_pre_restauracao_{timestamp}.env"
                shutil.copy2(arquivo_env_atual, backup_atual)
                logger.info(f"📋 Backup do .env atual criado: {backup_atual.name}")
                
            # Restaura o backup
            shutil.copy2(caminho_backup, arquivo_env_atual)
            logger.info(f"✅ Arquivo .env restaurado de: {Path(caminho_backup).name}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao restaurar .env: {e}")
            return False
            
    def limpar_backups_antigos(self, dias: int = 30) -> int:
        """Remove backups mais antigos que o número de dias especificado"""
        try:
            data_limite = datetime.datetime.now() - datetime.timedelta(days=dias)
            removidos = 0
            
            for arquivo in self.diretorio_backup.glob("*"):
                if arquivo.is_file():
                    data_arquivo = datetime.datetime.fromtimestamp(arquivo.stat().st_ctime)
                    
                    if data_arquivo < data_limite:
                        arquivo.unlink()
                        logger.info(f"🗑️ Backup removido: {arquivo.name}")
                        removidos += 1
                        
            logger.info(f"✅ Limpeza concluída: {removidos} backups removidos")
            return removidos
            
        except Exception as e:
            logger.error(f"❌ Erro ao limpar backups antigos: {e}")
            return 0
            
    def relatorio_backups(self) -> Dict:
        """Gera relatório completo dos backups"""
        try:
            backups = self.listar_backups()
            
            relatorio = {
                "data_relatorio": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "total_backups": len(backups),
                "espaco_utilizado": "0 B",
                "backup_mais_recente": None,
                "backup_mais_antigo": None,
                "tipos_backup": {},
                "backups_detalhados": backups
            }
            
            if backups:
                # Calcula espaço total utilizado
                espaco_total = sum(
                    Path(backup["caminho"]).stat().st_size 
                    for backup in backups
                )
                relatorio["espaco_utilizado"] = self._formatar_tamanho(espaco_total)
                
                # Backup mais recente e mais antigo
                relatorio["backup_mais_recente"] = backups[0]["data_criacao"]
                relatorio["backup_mais_antigo"] = backups[-1]["data_criacao"]
                
                # Conta tipos de backup
                for backup in backups:
                    tipo = backup["tipo"]
                    relatorio["tipos_backup"][tipo] = relatorio["tipos_backup"].get(tipo, 0) + 1
                    
            return relatorio
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório: {e}")
            return {"erro": str(e)}


def main():
    """Função principal para execução do sistema de backup"""
    print("=" * 70)
    print("🔄 SISTEMA DE BACKUP DAS CONFIGURAÇÕES - FAD")
    print("=" * 70)
    
    backup_system = SistemaBackupConfiguracoes()
    
    while True:
        print("\n📋 MENU DE OPÇÕES:")
        print("1. 📦 Backup Completo")
        print("2. 💾 Backup do .env")
        print("3. 🗃️  Backup dos Logs de Email")
        print("4. ⚙️  Backup das Configurações do Sistema")
        print("5. 📋 Listar Backups")
        print("6. 🔙 Restaurar .env")
        print("7. 🗑️  Limpar Backups Antigos")
        print("8. 📊 Relatório de Backups")
        print("0. ❌ Sair")
        
        opcao = input("\n🔹 Escolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n🔄 Realizando backup completo...")
            resultado = backup_system.backup_completo()
            if resultado:
                print(f"✅ Backup completo criado: {Path(resultado).name}")
            else:
                print("❌ Falha ao criar backup completo")
                
        elif opcao == "2":
            print("\n🔄 Realizando backup do .env...")
            resultado = backup_system.backup_arquivo_env()
            if resultado:
                print(f"✅ Backup do .env criado: {Path(resultado).name}")
            else:
                print("❌ Falha ao criar backup do .env")
                
        elif opcao == "3":
            print("\n🔄 Realizando backup dos logs de email...")
            resultado = backup_system.backup_logs_email()
            if resultado:
                print(f"✅ Backup dos logs criado: {Path(resultado).name}")
            else:
                print("❌ Falha ao criar backup dos logs")
                
        elif opcao == "4":
            print("\n🔄 Realizando backup das configurações...")
            resultado = backup_system.backup_configuracoes_sistema()
            if resultado:
                print(f"✅ Backup das configurações criado: {Path(resultado).name}")
            else:
                print("❌ Falha ao criar backup das configurações")
                
        elif opcao == "5":
            print("\n📋 BACKUPS DISPONÍVEIS:")
            backups = backup_system.listar_backups()
            if backups:
                for i, backup in enumerate(backups, 1):
                    print(f"{i:2d}. {backup['nome']}")
                    print(f"     Tipo: {backup['tipo']}")
                    print(f"     Tamanho: {backup['tamanho']}")
                    print(f"     Data: {backup['data_criacao']}")
                    print()
            else:
                print("❌ Nenhum backup encontrado")
                
        elif opcao == "6":
            backups = backup_system.listar_backups()
            env_backups = [b for b in backups if "env_backup" in b["nome"]]
            
            if not env_backups:
                print("❌ Nenhum backup de .env encontrado")
                continue
                
            print("\n📋 BACKUPS DE .env DISPONÍVEIS:")
            for i, backup in enumerate(env_backups, 1):
                print(f"{i}. {backup['nome']} - {backup['data_criacao']}")
                
            try:
                escolha = int(input("\n🔹 Escolha o backup para restaurar (0 para cancelar): "))
                if escolha == 0:
                    continue
                if 1 <= escolha <= len(env_backups):
                    backup_escolhido = env_backups[escolha - 1]
                    if backup_system.restaurar_env(backup_escolhido["caminho"]):
                        print("✅ Restauração concluída com sucesso!")
                    else:
                        print("❌ Falha na restauração")
                else:
                    print("❌ Opção inválida")
            except ValueError:
                print("❌ Entrada inválida")
                
        elif opcao == "7":
            try:
                dias = int(input("\n🔹 Remover backups mais antigos que quantos dias? (padrão: 30): ") or "30")
                removidos = backup_system.limpar_backups_antigos(dias)
                print(f"✅ {removidos} backups removidos")
            except ValueError:
                print("❌ Número inválido")
                
        elif opcao == "8":
            print("\n📊 RELATÓRIO DE BACKUPS:")
            relatorio = backup_system.relatorio_backups()
            
            if "erro" in relatorio:
                print(f"❌ Erro: {relatorio['erro']}")
            else:
                print(f"📅 Data do Relatório: {relatorio['data_relatorio']}")
                print(f"📦 Total de Backups: {relatorio['total_backups']}")
                print(f"💾 Espaço Utilizado: {relatorio['espaco_utilizado']}")
                
                if relatorio["backup_mais_recente"]:
                    print(f"🔄 Backup Mais Recente: {relatorio['backup_mais_recente']}")
                    print(f"📅 Backup Mais Antigo: {relatorio['backup_mais_antigo']}")
                    
                if relatorio["tipos_backup"]:
                    print("\n📋 Tipos de Backup:")
                    for tipo, quantidade in relatorio["tipos_backup"].items():
                        print(f"  • {tipo}: {quantidade}")
                        
        elif opcao == "0":
            print("\n👋 Saindo do sistema de backup...")
            break
            
        else:
            print("❌ Opção inválida")
            
        input("\n⏸️  Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
