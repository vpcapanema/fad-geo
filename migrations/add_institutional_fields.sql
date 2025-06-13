-- Script para adicionar campos institucionais à tabela usuario_sistema
-- Data: 2025-06-12

-- Adicionar campo sede_assistencia_direta se não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'Cadastro' 
        AND table_name = 'usuario_sistema' 
        AND column_name = 'sede_assistencia_direta'
    ) THEN
        ALTER TABLE "Cadastro"."usuario_sistema" 
        ADD COLUMN sede_assistencia_direta VARCHAR;
        
        RAISE NOTICE 'Coluna sede_assistencia_direta adicionada com sucesso';
    ELSE
        RAISE NOTICE 'Coluna sede_assistencia_direta já existe';
    END IF;
END $$;

-- Verificar se as outras colunas já existem (devem estar no modelo atual)
DO $$
BEGIN
    -- Verificar email_institucional
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'Cadastro' 
        AND table_name = 'usuario_sistema' 
        AND column_name = 'email_institucional'
    ) THEN
        ALTER TABLE "Cadastro"."usuario_sistema" 
        ADD COLUMN email_institucional VARCHAR;
        
        RAISE NOTICE 'Coluna email_institucional adicionada com sucesso';
    ELSE
        RAISE NOTICE 'Coluna email_institucional já existe';
    END IF;
    
    -- Verificar telefone_institucional
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'Cadastro' 
        AND table_name = 'usuario_sistema' 
        AND column_name = 'telefone_institucional'
    ) THEN
        ALTER TABLE "Cadastro"."usuario_sistema" 
        ADD COLUMN telefone_institucional VARCHAR;
        
        RAISE NOTICE 'Coluna telefone_institucional adicionada com sucesso';
    ELSE
        RAISE NOTICE 'Coluna telefone_institucional já existe';
    END IF;
    
    -- Verificar ramal
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'Cadastro' 
        AND table_name = 'usuario_sistema' 
        AND column_name = 'ramal'
    ) THEN
        ALTER TABLE "Cadastro"."usuario_sistema" 
        ADD COLUMN ramal VARCHAR;
        
        RAISE NOTICE 'Coluna ramal adicionada com sucesso';
    ELSE
        RAISE NOTICE 'Coluna ramal já existe';
    END IF;
END $$;

-- Verificar estrutura final da tabela
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_schema = 'Cadastro' 
AND table_name = 'usuario_sistema' 
ORDER BY ordinal_position;
