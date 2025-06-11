"""
Gerador de PDF alternativo usando reportlab
Para casos onde wkhtmltopdf não está disponível
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, blue, green
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

def gerar_comprovante_cadastro_pdf(usuario_dados, pessoa_fisica_dados, caminho_arquivo):
    """
    Gera comprovante de cadastro em PDF usando reportlab
    
    Args:
        usuario_dados: Dados do usuário
        pessoa_fisica_dados: Dados da pessoa física
        caminho_arquivo: Caminho onde salvar o PDF
    
    Returns:
        bool: True se gerado com sucesso
    """
    try:
        # Cria documento
        doc = SimpleDocTemplate(
            caminho_arquivo,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=blue,
            spaceAfter=30,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=black,
            spaceAfter=12
        )
        
        normal_style = styles['Normal']
        
        # Conteúdo do documento
        story = []
        
        # Cabeçalho
        story.append(Paragraph("FAD - FERRAMENTA DE ANÁLISE DINAMIZADA", title_style))
        story.append(Paragraph("COMPROVANTE DE CADASTRO DE USUÁRIO", title_style))
        story.append(Spacer(1, 20))
        
        # Informações do usuário
        story.append(Paragraph("DADOS DO USUÁRIO", heading_style))
        
        dados_usuario = [
            ["Nome Completo:", usuario_dados.get('nome', 'N/A')],
            ["CPF:", usuario_dados.get('cpf', 'N/A')],
            ["Tipo de Usuário:", usuario_dados.get('tipo', 'N/A').title()],
            ["Email Pessoal:", usuario_dados.get('email', 'N/A')],
            ["Telefone:", usuario_dados.get('telefone', 'N/A')],
            ["Status:", usuario_dados.get('status', 'Aguardando Aprovação')],
        ]
        
        table_usuario = Table(dados_usuario, colWidths=[2*inch, 3.5*inch])
        table_usuario.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), '#f0f0f0'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(table_usuario)
        story.append(Spacer(1, 20))
        
        # Informações institucionais (se disponíveis)
        if usuario_dados.get('email_institucional'):
            story.append(Paragraph("DADOS INSTITUCIONAIS", heading_style))
            
            dados_institucionais = [
                ["Instituição:", usuario_dados.get('instituicao', 'N/A')],
                ["Email Institucional:", usuario_dados.get('email_institucional', 'N/A')],
                ["Telefone Institucional:", usuario_dados.get('telefone_institucional', 'N/A')],
                ["Ramal:", usuario_dados.get('ramal', 'N/A')],
                ["Tipo de Lotação:", usuario_dados.get('tipo_lotacao', 'N/A')],
            ]
            
            # Adiciona dados de sede se disponível
            if usuario_dados.get('sede_hierarquia'):
                dados_institucionais.extend([
                    ["Sede - Hierarquia:", usuario_dados.get('sede_hierarquia', 'N/A')],
                    ["Sede - Coordenadoria:", usuario_dados.get('sede_coordenadoria', 'N/A')],
                    ["Sede - Setor:", usuario_dados.get('sede_setor', 'N/A')],
                ])
            
            # Adiciona dados regionais se disponível
            if usuario_dados.get('regional_nome'):
                dados_institucionais.extend([
                    ["Regional - Nome:", usuario_dados.get('regional_nome', 'N/A')],
                    ["Regional - Coordenadoria:", usuario_dados.get('regional_coordenadoria', 'N/A')],
                    ["Regional - Setor:", usuario_dados.get('regional_setor', 'N/A')],
                ])
            
            table_institucional = Table(dados_institucionais, colWidths=[2*inch, 3.5*inch])
            table_institucional.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), '#f0f0f0'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(table_institucional)
            story.append(Spacer(1, 20))
        
        # Informações da pessoa física vinculada (se disponível)
        if pessoa_fisica_dados:
            story.append(Paragraph("PESSOA FÍSICA VINCULADA", heading_style))
            
            dados_pf = [
                ["ID:", str(pessoa_fisica_dados.get('id', 'N/A'))],
                ["Nome:", pessoa_fisica_dados.get('nome', 'N/A')],
            ]
            
            table_pf = Table(dados_pf, colWidths=[2*inch, 3.5*inch])
            table_pf.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), '#f0f0f0'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(table_pf)
            story.append(Spacer(1, 20))
        
        # Informações de geração
        story.append(Paragraph("INFORMAÇÕES DE GERAÇÃO", heading_style))
        
        dados_geracao = [
            ["Data de Cadastro:", datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
            ["Sistema:", "FAD - Ferramenta de Análise Dinamizada"],
            ["Versão do Documento:", "1.0"],
            ["ID do Usuário:", str(usuario_dados.get('id', 'N/A'))],
        ]
        
        table_geracao = Table(dados_geracao, colWidths=[2*inch, 3.5*inch])
        table_geracao.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), '#f0f0f0'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(table_geracao)
        story.append(Spacer(1, 30))
        
        # Observações
        story.append(Paragraph("OBSERVAÇÕES", heading_style))
        observacoes = [
            "• Este comprovante confirma o cadastro no sistema FAD.",
            "• O cadastro está sujeito à aprovação do administrador.",
            "• Guarde este documento para seus registros.",
            "• Em caso de dúvidas, entre em contato com o suporte técnico."
        ]
        
        for obs in observacoes:
            story.append(Paragraph(obs, normal_style))
        
        story.append(Spacer(1, 20))
        
        # Rodapé
        story.append(Paragraph("_" * 50, normal_style))
        story.append(Paragraph(
            "FAD - Ferramenta de Análise Dinamizada<br/>"
            "Departamento de Estradas de Rodagem do Estado de São Paulo<br/>"
            f"Documento gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}",
            ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=black,
                alignment=1  # Center
            )
        ))
        
        # Gera o PDF
        doc.build(story)
        
        print(f"✅ PDF gerado com sucesso: {caminho_arquivo}")
        print(f"📏 Tamanho: {os.path.getsize(caminho_arquivo)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")
        return False

def testar_geracao_pdf():
    """Testa a geração de PDF"""
    print("🧪 TESTANDO GERAÇÃO DE PDF COM REPORTLAB")
    print("=" * 50)
    
    # Dados de teste
    usuario_teste = {
        'id': 1,
        'nome': 'Vinícius Capanema (TESTE)',
        'cpf': '123.456.789-00',
        'email': 'vpcapanema@der.sp.gov.br',
        'telefone': '(11) 99999-9999',
        'tipo': 'administrador',
        'status': 'Aguardando Aprovação',
        'instituicao': 'DER-SP',
        'email_institucional': 'vpcapanema@der.sp.gov.br',
        'telefone_institucional': '(11) 3311-1234',
        'ramal': '1234',
        'tipo_lotacao': 'sede',
        'sede_hierarquia': 'VPC',
        'sede_coordenadoria': 'GEOSER',
        'sede_setor': 'Análise de Dados'
    }
    
    pessoa_fisica_teste = {
        'id': 1,
        'nome': 'Vinícius Capanema'
    }
    
    # Gera PDF de teste
    caminho_teste = "teste_comprovante_reportlab.pdf"
    
    resultado = gerar_comprovante_cadastro_pdf(
        usuario_teste, 
        pessoa_fisica_teste, 
        caminho_teste
    )
    
    if resultado and os.path.exists(caminho_teste):
        print("🎉 Teste concluído com sucesso!")
        print(f"📄 Arquivo gerado: {caminho_teste}")
        
        # Pergunta se quer testar envio por email
        enviar = input("\nDeseja testar envio por email? (s/N): ").lower().strip()
        if enviar == 's':
            testar_envio_email(caminho_teste)
    else:
        print("❌ Teste falhou")

def testar_envio_email(caminho_pdf):
    """Testa envio do PDF por email"""
    print("\n📧 TESTANDO ENVIO POR EMAIL...")
    
    try:
        import sys
        sys.path.insert(0, os.getcwd())
        
        from app.services.email_service import email_service
        
        resultado = email_service.enviar_email_confirmacao_cadastro(
            destinatario_email="vpcapanema@der.sp.gov.br",
            destinatario_nome="Vinícius Capanema",
            comprovante_pdf_path=caminho_pdf,
            dados_cadastro={
                'nome': 'Vinícius Capanema (TESTE REPORTLAB)',
                'tipo': 'administrador',
                'status': 'Teste de PDF com ReportLab'
            }
        )
        
        if resultado:
            print("✅ Email enviado com sucesso!")
            print("📧 Verifique seu email institucional")
        else:
            print("❌ Falha no envio do email")
            
    except Exception as e:
        print(f"❌ Erro no teste de email: {e}")

if __name__ == "__main__":
    testar_geracao_pdf()
