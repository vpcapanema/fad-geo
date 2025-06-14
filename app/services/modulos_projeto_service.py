from sqlalchemy.orm import Session
from app.models.pr_projeto import Projeto
from app.models.pr_relatorio_modulo import RelatorioModulo
from app.models.pr_modulo_configuracao import ModuloConfiguracao
from typing import Dict, Any, List
from datetime import datetime
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class ModulosProjetoService:
    """Serviço para gerenciar os 5 módulos/formulários de cada projeto"""
    
    # Configuração dos 5 módulos
    MODULOS_CONFIG = {
        1: {
            "nome": "Cadastro do Projeto",
            "descricao": "Informações básicas, responsáveis e dados gerais",
            "template": "pr_modulo_cadastro.html",
            "endpoint": "/modulos/cadastro",
            "campos_obrigatorios": ["nome_projeto", "responsavel_tecnico", "pessoa_juridica"]
        },
        2: {
            "nome": "Conformidade Ambiental", 
            "descricao": "Análise de impactos e licenças ambientais",
            "template": "pr_modulo_ambiental.html",
            "endpoint": "/modulos/ambiental",
            "campos_obrigatorios": ["licenca_ambiental", "impactos_identificados"]
        },
        3: {
            "nome": "Favorabilidade Multicritério",
            "descricao": "Análise multicritério dos fatores relevantes",
            "template": "pr_modulo_multicriterio.html", 
            "endpoint": "/modulos/multicriterio",
            "campos_obrigatorios": ["criterios_selecionados", "pesos_atribuidos"]
        },
        4: {
            "nome": "Favorabilidade Socioeconômica",
            "descricao": "Análise dos impactos socioeconômicos",
            "template": "pr_modulo_socioeconomico.html",
            "endpoint": "/modulos/socioeconomico", 
            "campos_obrigatorios": ["impacto_social", "beneficios_economicos"]
        },
        5: {
            "nome": "Favorabilidade Infraestrutural",
            "descricao": "Análise da infraestrutura existente e necessária",
            "template": "pr_modulo_infraestrutura.html",
            "endpoint": "/modulos/infraestrutura",
            "campos_obrigatorios": ["infraestrutura_existente", "obras_necessarias"]
        }
    }
    
    def __init__(self, db: Session):
        self.db = db

    def inicializar_modulos_projeto(self, projeto_id: int) -> Dict[str, Any]:
        """
        Inicializa todos os 5 módulos para um projeto novo
        """
        try:
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if not projeto:
                raise ValueError(f"Projeto {projeto_id} não encontrado")

            modulos_criados = []
            
            for numero, config in self.MODULOS_CONFIG.items():
                # Verifica se já existe
                relatorio_existente = self.db.query(RelatorioModulo).filter(
                    RelatorioModulo.projeto_id == projeto_id,
                    RelatorioModulo.modulo_numero == numero
                ).first()
                
                if not relatorio_existente:
                    relatorio = RelatorioModulo(
                        projeto_id=projeto_id,
                        modulo_numero=numero,
                        modulo_nome=config["nome"],
                        status='pendente',
                        pode_executar=(numero == 1),  # Apenas o primeiro pode ser executado
                        dependencias_ok=(numero == 1),
                        criado_em=datetime.now(),
                        dados_extras={
                            "template": config["template"],
                            "endpoint": config["endpoint"],
                            "campos_obrigatorios": config["campos_obrigatorios"],
                            "dados_formulario": {}
                        }
                    )
                    
                    self.db.add(relatorio)
                    modulos_criados.append({
                        "numero": numero,
                        "nome": config["nome"],
                        "pode_executar": (numero == 1)
                    })

            self.db.commit()
            
            logger.info(f"Módulos inicializados para projeto {projeto_id}")
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'modulos_criados': modulos_criados
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao inicializar módulos do projeto {projeto_id}: {str(e)}")
            raise

    def salvar_dados_modulo(self, projeto_id: int, modulo_numero: int, 
                           dados_formulario: Dict, usuario_id: int) -> Dict[str, Any]:
        """
        Salva os dados de um módulo específico
        """
        try:
            # Busca o relatório do módulo
            relatorio = self.db.query(RelatorioModulo).filter(
                RelatorioModulo.projeto_id == projeto_id,
                RelatorioModulo.modulo_numero == modulo_numero
            ).first()
            
            if not relatorio:
                raise ValueError(f"Módulo {modulo_numero} não encontrado para projeto {projeto_id}")
                
            if not relatorio.pode_executar:
                raise ValueError(f"Módulo {modulo_numero} não pode ser executado ainda")

            # Valida campos obrigatórios
            config = self.MODULOS_CONFIG[modulo_numero]
            self._validar_campos_obrigatorios(dados_formulario, config["campos_obrigatorios"])
            
            # Atualiza dados
            if not relatorio.dados_extras:
                relatorio.dados_extras = {}
                
            relatorio.dados_extras["dados_formulario"] = dados_formulario
            relatorio.dados_extras["preenchido_em"] = datetime.now().isoformat()
            relatorio.dados_extras["preenchido_por"] = usuario_id
            
            relatorio.status = 'em_preenchimento'
            relatorio.atualizado_em = datetime.now()
            
            self.db.commit()
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'modulo_numero': modulo_numero,
                'status': 'em_preenchimento'
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar dados do módulo {modulo_numero}: {str(e)}")
            raise

    def validar_modulo(self, projeto_id: int, modulo_numero: int, usuario_id: int) -> Dict[str, Any]:
        """
        Valida um módulo e libera o próximo para preenchimento
        """
        try:
            relatorio = self.db.query(RelatorioModulo).filter(
                RelatorioModulo.projeto_id == projeto_id,
                RelatorioModulo.modulo_numero == modulo_numero
            ).first()
            
            if not relatorio:
                raise ValueError(f"Módulo {modulo_numero} não encontrado")
                
            if relatorio.status != 'em_preenchimento':
                raise ValueError(f"Módulo deve estar em preenchimento para ser validado")

            # Valida se todos os dados necessários estão preenchidos
            dados = relatorio.dados_extras.get("dados_formulario", {})
            config = self.MODULOS_CONFIG[modulo_numero]
            self._validar_campos_obrigatorios(dados, config["campos_obrigatorios"])
            
            # Marca como validado
            relatorio.status = 'validado'
            relatorio.validado_em = datetime.now()
            relatorio.validado_por = usuario_id
            
            # Libera próximo módulo se existir
            if modulo_numero < 5:
                proximo_relatorio = self.db.query(RelatorioModulo).filter(
                    RelatorioModulo.projeto_id == projeto_id,
                    RelatorioModulo.modulo_numero == modulo_numero + 1
                ).first()
                
                if proximo_relatorio:
                    proximo_relatorio.pode_executar = True
                    proximo_relatorio.dependencias_ok = True

            # Verifica se todos os módulos estão validados
            modulos_validados = self.db.query(RelatorioModulo).filter(
                RelatorioModulo.projeto_id == projeto_id,
                RelatorioModulo.status == 'validado'
            ).count()
            
            # Atualiza projeto
            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            if modulos_validados == 5:
                projeto.todos_modulos_concluidos = True
                projeto.pronto_para_pdf = True
                projeto.modulo_atual = 5
            else:
                projeto.modulo_atual = modulo_numero + 1
            
            self.db.commit()
            
            return {
                'success': True,
                'projeto_id': projeto_id,
                'modulo_validado': modulo_numero,
                'proximo_liberado': modulo_numero + 1 if modulo_numero < 5 else None,
                'todos_concluidos': modulos_validados == 5
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao validar módulo {modulo_numero}: {str(e)}")
            raise

    def gerar_html_modulo(self, projeto_id: int, modulo_numero: int) -> str:
        """
        Gera HTML completo do módulo para visualização/PDF
        """
        try:
            relatorio = self.db.query(RelatorioModulo).filter(
                RelatorioModulo.projeto_id == projeto_id,
                RelatorioModulo.modulo_numero == modulo_numero
            ).first()
            
            if not relatorio:
                raise ValueError(f"Módulo {modulo_numero} não encontrado")

            projeto = self.db.query(Projeto).filter(Projeto.id == projeto_id).first()
            config = self.MODULOS_CONFIG[modulo_numero]
            dados = relatorio.dados_extras.get("dados_formulario", {})
            
            # Template HTML básico
            html_content = f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>FAD-GEO - {config['nome']} - {projeto.nome}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .header {{ text-align: center; margin-bottom: 30px; }}
                    .secao {{ margin: 20px 0; padding: 15px; border: 1px solid #ccc; }}
                    .campo {{ margin: 10px 0; }}
                    .label {{ font-weight: bold; }}
                    .rodape {{ margin-top: 40px; font-size: 12px; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>FAD - Ferramenta de Análise Dinamizada</h1>
                    <h2>{config['nome']}</h2>
                    <h3>Projeto: {projeto.nome}</h3>
                </div>
                
                <div class="secao">
                    <h3>Informações do Módulo</h3>
                    <div class="campo">
                        <span class="label">Módulo:</span> {modulo_numero} - {config['nome']}
                    </div>
                    <div class="campo">
                        <span class="label">Descrição:</span> {config['descricao']}
                    </div>
                    <div class="campo">
                        <span class="label">Status:</span> {relatorio.status}
                    </div>
                    <div class="campo">
                        <span class="label">Preenchido em:</span> {relatorio.dados_extras.get('preenchido_em', 'N/A')}
                    </div>
                </div>
                
                <div class="secao">
                    <h3>Dados do Formulário</h3>
                    {self._gerar_html_campos(dados)}
                </div>
                
                <div class="rodape">
                    <p>Documento gerado automaticamente pelo sistema FAD-GEO em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
                </div>
            </body>
            </html>
            """
            
            # Salva o HTML no registro
            relatorio.html_conteudo = html_content
            relatorio.html_arquivo = f"modulo_{modulo_numero}_projeto_{projeto_id}.html"
            self.db.commit()
            
            return html_content
            
        except Exception as e:
            logger.error(f"Erro ao gerar HTML do módulo {modulo_numero}: {str(e)}")
            raise

    def get_status_modulos_projeto(self, projeto_id: int) -> Dict[str, Any]:
        """
        Retorna o status completo de todos os módulos de um projeto
        """
        try:
            relatorios = self.db.query(RelatorioModulo).filter(
                RelatorioModulo.projeto_id == projeto_id
            ).order_by(RelatorioModulo.modulo_numero).all()
            
            status_modulos = []
            for relatorio in relatorios:
                config = self.MODULOS_CONFIG[relatorio.modulo_numero]
                
                status_modulos.append({
                    "numero": relatorio.modulo_numero,
                    "nome": relatorio.modulo_nome,
                    "descricao": config["descricao"],
                    "status": relatorio.status,
                    "pode_executar": relatorio.pode_executar,
                    "validado_em": relatorio.validado_em,
                    "tem_dados": bool(relatorio.dados_extras and relatorio.dados_extras.get("dados_formulario")),
                    "progresso": self._calcular_progresso_modulo(relatorio)
                })
            
            # Cálculos gerais
            modulos_validados = sum(1 for s in status_modulos if s["status"] == "validado")
            progresso_geral = int((modulos_validados / 5) * 100)
            
            return {
                'projeto_id': projeto_id,
                'modulos': status_modulos,
                'modulos_validados': modulos_validados,
                'progresso_geral': progresso_geral,
                'todos_concluidos': modulos_validados == 5
            }
            
        except Exception as e:
            logger.error(f"Erro ao buscar status dos módulos: {str(e)}")
            raise

    def _validar_campos_obrigatorios(self, dados: Dict, campos_obrigatorios: List[str]):
        """Valida se todos os campos obrigatórios estão preenchidos"""
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                raise ValueError(f"Campo obrigatório '{campo}' não preenchido")

    def _gerar_html_campos(self, dados: Dict) -> str:
        """Gera HTML para exibir os campos do formulário"""
        if not dados:
            return "<p>Nenhum dado preenchido</p>"
            
        html = ""
        for campo, valor in dados.items():
            html += f"""
            <div class="campo">
                <span class="label">{campo.replace('_', ' ').title()}:</span> {valor}
            </div>
            """
        return html

    def _calcular_progresso_modulo(self, relatorio: RelatorioModulo) -> int:
        """Calcula o progresso de preenchimento de um módulo"""
        if relatorio.status == 'validado':
            return 100
        elif relatorio.status == 'em_preenchimento':
            # Poderia verificar quantos campos estão preenchidos
            return 50
        else:
            return 0
