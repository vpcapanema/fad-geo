# Diretórios base
$diretorios = @("app/static", "app/templates")

# Substituições mapeadas para fetch, href e action
$substituicoes = @{
    '/upload'                   = '/shape/upload'
    '/geometria/validar'        = '/shape/validar'
    '/geometria/relatorio'      = '/shape/relatorio-validacao'
    '/delete-uploaded-file'     = '/shape/limpeza/delete-uploaded-file'
    '/projetos/status'          = '/projeto/status'
    '/cadastrar-projeto'        = '/projeto'
    '/cadastrar-pessoa-fisica'  = '/pessoa-fisica'
    '/cadastrar-pessoa-juridica'= '/pessoa-juridica'
    '/cadastrar-usuario'        = '/usuario'
    '/aprovar-usuarios'         = '/usuario/aprovacao'
}

foreach ($dir in $diretorios) {
    Get-ChildItem -Path $dir -Include *.js, *.html -Recurse | ForEach-Object {
        $filePath = $_.FullName
        $conteudo = Get-Content $filePath -Raw

        foreach ($chave in $substituicoes.Keys) {
            $valor = $substituicoes[$chave]
            $conteudo = $conteudo -replace [regex]::Escape($chave), $valor
        }

        # Backup automático
        Copy-Item -Path $filePath -Destination ($filePath + ".bak") -Force

        # Salva o conteúdo atualizado
        Set-Content -Path $filePath -Value $conteudo -Encoding UTF8

        Write-Host "✅ Atualizado JS/HTML: $filePath"
    }
}
