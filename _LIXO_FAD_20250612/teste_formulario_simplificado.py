"""
Teste do FormularioService simplificado (apenas dados da tabela usuario_sistema)
"""
import sys
sys.path.append('c:/Users/vinic/fad-geo')

from app.database.session import get_db
from app.services.formulario_service import formulario_service
import logging

# Configura logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def teste_formulario_simplificado():
    """Testa a geração de formulário usando apenas dados da tabela usuario_sistema"""
    
    # Conecta com o banco
    db = next(get_db())
    
    try:
        # Testa com um usuário existente (ID 1 se existir)
        usuario_id = 1
        logger.info(f"🧪 Testando geração de formulário para usuário {usuario_id}")
        
        # Gera o formulário HTML
        caminho_formulario = formulario_service.gerar_formulario_html(db, usuario_id)
        
        logger.info(f"✅ Formulário gerado com sucesso!")
        logger.info(f"📁 Caminho: {caminho_formulario}")
        
        # Verifica se o arquivo existe
        from pathlib import Path
        arquivo = Path(caminho_formulario)
        if arquivo.exists():
            tamanho = arquivo.stat().st_size
            logger.info(f"📊 Arquivo criado - Tamanho: {tamanho} bytes")
            
            # Lê e verifica o conteúdo
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                
            if 'pessoa_fisica' not in conteudo.lower():
                logger.info("✅ Template não contém referências a pessoa_fisica - CORRETO!")
            else:
                logger.warning("⚠️ Template ainda contém referências a pessoa_fisica")
                
            return True
        else:
            logger.error("❌ Arquivo não foi criado")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro no teste: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    sucesso = teste_formulario_simplificado()
    if sucesso:
        print("\n🎉 TESTE PASSOU - FormularioService simplificado funcionando!")
    else:
        print("\n❌ TESTE FALHOU - Verificar logs acima")
