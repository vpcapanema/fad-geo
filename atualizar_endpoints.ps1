$basePath = "app/api/endpoints"

$routers = @{
    "au_autenticacao.py"                     = @("/login", "Login")
    "cd_cadastro_usuario_sistema.py"         = @("/usuario", "Cadastro de Usuário")
    "cd_aprovar_usuario.py"                  = @("/usuario/aprovacao", "Aprovação de Usuários")
    "cd_cadastro_pessoa_fisica.py"           = @("/pessoa-fisica", "Cadastro de Pessoa Física")
    "cd_cadastro_pessoa_juridica.py"         = @("/pessoa-juridica", "Cadastro de Pessoa Jurídica")
    "cd_cadastro_trechos_estadualizacao.py"  = @("/trecho", "Cadastro de Trechos")
    "pr_gravar_projeto.py"                   = @("/projeto", "Cadastro de Projeto")
    "pr_salvar_projeto.py"                   = @("/projeto/salvar", "Gravação de Projeto")
    "pr_upload_zip.py"                       = @("/shape/upload", "Upload de Shape")
    "pr_validacao_geometria.py"              = @("/shape/validacao", "Validação de Geometria")
    "pr_salvar_geometria_validada.py"        = @("/shape/salvar", "Salvar Geometria Validada")
    "pr_delete_upload.py"                    = @("/shape/limpeza", "Limpeza de Geometrias")
    "pr_relatorio_validacao.py"              = @("/shape/relatorio-validacao", "Relatório de Validação")
    "pr_relatorio_upload.py"                 = @("/shape/relatorio-upload", "Relatório de Upload")
    "pr_status_projeto.py"                   = @("/projeto/status", "Status de Projetos")
    "ca_endpoint.py"                         = @("/analise/conformidade", "Conformidade Ambiental")
    "pn_painel_usuario_comum.py"             = @("/painel/usuario", "Painel do Usuário")
    "pn_painel_usuario_administrador.py"     = @("/painel/administrador", "Painel do Administrador")
    "pn_painel_usuario_master.py"            = @("/painel/master", "Painel Master")
    "vw_painel_administrador.py"             = @("/view/administrador", "View Painel Administrador")
    "vw_projetos_usuario_comum.py"           = @("/view/usuario", "View Projetos Usuário")
    "au_redirecionamento_login_cd_usuario.py"= @("/login/redirecionamento", "Redirecionamento Pós-Login")
}

foreach ($file in $routers.Keys) {
    $fullPath = Join-Path $basePath $file

    if (Test-Path $fullPath) {
        $prefix = $routers[$file][0]
        $tag = $routers[$file][1]

        $original = Get-Content $fullPath
        $importIndex = ($original | Select-String -Pattern "from .* import .*" -AllMatches).Count

        $bloco = @"
# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='$prefix',
    tags=['$tag']
)
"@

        # Inserir logo após os imports
        $before = $original[0..($importIndex)]
        $after = $original[($importIndex+1)..($original.Length - 1)]

        $novoConteudo = $before + $bloco + $after
        $novoConteudo | Set-Content $fullPath -Encoding UTF8

        Write-Host "✅ Atualizado: $file"
    }
    else {
        Write-Host "⚠️ Arquivo não encontrado: $file"
    }
}
