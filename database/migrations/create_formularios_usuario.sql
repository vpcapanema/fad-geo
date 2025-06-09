-- Tabela para controle dos formulários de usuário
CREATE TABLE formularios_usuario (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    arquivo_nome VARCHAR(255) NOT NULL,
    caminho_completo TEXT NOT NULL,
    data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    versao INTEGER DEFAULT 1,
    ativo BOOLEAN DEFAULT TRUE,
    hash_conteudo VARCHAR(64),
    tamanho_arquivo INTEGER,
    status VARCHAR(20) DEFAULT 'ativo', -- ativo, arquivado, erro
    observacoes TEXT,
    
    -- Índices para performance
    CONSTRAINT unique_usuario_ativo UNIQUE (usuario_id, ativo) DEFERRABLE INITIALLY DEFERRED
);

-- Índices para otimização
CREATE INDEX idx_formularios_usuario_id ON formularios_usuario(usuario_id);
CREATE INDEX idx_formularios_ativo ON formularios_usuario(ativo) WHERE ativo = TRUE;
CREATE INDEX idx_formularios_data_geracao ON formularios_usuario(data_geracao);

-- Comentários para documentação
COMMENT ON TABLE formularios_usuario IS 'Controle de formulários de comprovante de cadastro dos usuários';
COMMENT ON COLUMN formularios_usuario.hash_conteudo IS 'Hash MD5 do conteúdo para detectar mudanças';
COMMENT ON COLUMN formularios_usuario.versao IS 'Versão incremental do formulário do usuário';
COMMENT ON COLUMN formularios_usuario.ativo IS 'Apenas um formulário ativo por usuário (constraint unique)';