# Diagnóstico Completo da Plataforma FAD-GEO
# Script para testar todas as funcionalidades principais

Write-Host "===================================" -ForegroundColor Green
Write-Host "🔍 DIAGNÓSTICO DA PLATAFORMA FAD-GEO" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

$BaseUrl = "http://127.0.0.1:8000"
$resultados = @()

# Função para testar uma URL
function Test-Endpoint {
    param($url, $descricao, $metodo = "GET")
    try {
        if ($metodo -eq "GET") {
            $response = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 10 -ErrorAction Stop
        }
        $status = "✅ OK"
        $detalhes = "Status: $($response.StatusCode)"
        if ($response.Content.Length -gt 0) {
            $detalhes += " | Tamanho: $($response.Content.Length) bytes"
        }
    } catch {
        $status = "❌ ERRO"
        $detalhes = $_.Exception.Message
        if ($_.Exception.Response) {
            $detalhes = "Status: $($_.Exception.Response.StatusCode) - $detalhes"
        }
    }
    
    $resultado = [PSCustomObject]@{
        Categoria = ""
        Endpoint = $url -replace $BaseUrl, ""
        Descricao = $descricao
        Status = $status
        Detalhes = $detalhes
    }
    return $resultado
}

Write-Host "`n1. TESTANDO ROTAS PRINCIPAIS..." -ForegroundColor Yellow

# Rotas principais
$resultados += Test-Endpoint "$BaseUrl/" "Página inicial"
$resultados[-1].Categoria = "Páginas Principais"

$resultados += Test-Endpoint "$BaseUrl/login" "Página de login"
$resultados[-1].Categoria = "Páginas Principais"

$resultados += Test-Endpoint "$BaseUrl/boas-vindas" "Página de boas-vindas"
$resultados[-1].Categoria = "Páginas Principais"

$resultados += Test-Endpoint "$BaseUrl/cadastro-usuario" "Formulário de cadastro"
$resultados[-1].Categoria = "Páginas Principais"

Write-Host "`n2. TESTANDO PAINÉIS DE USUÁRIO..." -ForegroundColor Yellow

# Painéis (sem autenticação)
$resultados += Test-Endpoint "$BaseUrl/painel-analista" "Painel do Analista"
$resultados[-1].Categoria = "Painéis"

$resultados += Test-Endpoint "$BaseUrl/painel-coordenador" "Painel do Coordenador"
$resultados[-1].Categoria = "Painéis"

$resultados += Test-Endpoint "$BaseUrl/painel-master" "Painel Master"
$resultados[-1].Categoria = "Painéis"

Write-Host "`n3. TESTANDO ARQUIVOS ESTÁTICOS..." -ForegroundColor Yellow

# Arquivos estáticos
$resultados += Test-Endpoint "$BaseUrl/static/css/componentes/fad_header.css" "CSS do cabeçalho"
$resultados[-1].Categoria = "Arquivos Estáticos"

$resultados += Test-Endpoint "$BaseUrl/static/js/componentes/fad_header.js" "JavaScript do cabeçalho"
$resultados[-1].Categoria = "Arquivos Estáticos"

$resultados += Test-Endpoint "$BaseUrl/static/images/fad_logo_banco_completo1.png" "Logo da FAD"
$resultados[-1].Categoria = "Arquivos Estáticos"

Write-Host "`n4. TESTANDO ENDPOINTS DE API..." -ForegroundColor Yellow

# Endpoints de API
$resultados += Test-Endpoint "$BaseUrl/debug" "Endpoint de debug"
$resultados[-1].Categoria = "API"

$resultados += Test-Endpoint "$BaseUrl/docs" "Documentação da API"
$resultados[-1].Categoria = "API"

$resultados += Test-Endpoint "$BaseUrl/painel/master/usuarios" "Lista de usuários (Master)"
$resultados[-1].Categoria = "API"

$resultados += Test-Endpoint "$BaseUrl/cadastro/pfs/json" "Lista de PF (JSON)"
$resultados[-1].Categoria = "API"

Write-Host "`n5. TESTANDO FORMULÁRIOS..." -ForegroundColor Yellow

# Formulários específicos
$resultados += Test-Endpoint "$BaseUrl/cadastro-interessado-pf" "Cadastro Pessoa Física"
$resultados[-1].Categoria = "Formulários"

$resultados += Test-Endpoint "$BaseUrl/cadastro-interessado-pj" "Cadastro Pessoa Jurídica"
$resultados[-1].Categoria = "Formulários"

$resultados += Test-Endpoint "$BaseUrl/cadastro-projeto" "Cadastro de Projeto"
$resultados[-1].Categoria = "Formulários"

Write-Host "`n6. TESTANDO MÓDULOS ESPECIALIZADOS..." -ForegroundColor Yellow

# Módulos especializados
$resultados += Test-Endpoint "$BaseUrl/conformidade" "Módulo Conformidade Ambiental"
$resultados[-1].Categoria = "Módulos"

$resultados += Test-Endpoint "$BaseUrl/importar" "Módulo Importação"
$resultados[-1].Categoria = "Módulos"

$resultados += Test-Endpoint "$BaseUrl/validar" "Módulo Validação"
$resultados[-1].Categoria = "Módulos"

Write-Host "`n===================================" -ForegroundColor Green
Write-Host "📊 RELATÓRIO DO DIAGNÓSTICO" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

# Agrupando por categoria
$categorias = $resultados | Group-Object Categoria

foreach ($categoria in $categorias) {
    Write-Host "`n$($categoria.Name):" -ForegroundColor Cyan
    foreach ($item in $categoria.Group) {
        $cor = if ($item.Status -like "*OK*") { "Green" } else { "Red" }
        Write-Host "  $($item.Status) $($item.Endpoint) - $($item.Descricao)" -ForegroundColor $cor
        if ($item.Status -like "*ERRO*") {
            Write-Host "      → $($item.Detalhes)" -ForegroundColor Red
        }
    }
}

# Estatísticas
$total = $resultados.Count
$sucessos = ($resultados | Where-Object { $_.Status -like "*OK*" }).Count
$erros = $total - $sucessos
$percentualSucesso = [math]::Round(($sucessos / $total) * 100, 1)

Write-Host "`n===================================" -ForegroundColor Green
Write-Host "📈 ESTATÍSTICAS" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host "Total de testes: $total" -ForegroundColor White
Write-Host "Sucessos: $sucessos" -ForegroundColor Green
Write-Host "Erros: $erros" -ForegroundColor Red
Write-Host "Taxa de sucesso: $percentualSucesso%" -ForegroundColor White

if ($percentualSucesso -ge 90) {
    Write-Host "`n✅ PLATAFORMA FUNCIONANDO ADEQUADAMENTE" -ForegroundColor Green
} elseif ($percentualSucesso -ge 70) {
    Write-Host "`n⚠️ PLATAFORMA COM PROBLEMAS MENORES" -ForegroundColor Yellow
} else {
    Write-Host "`n❌ PLATAFORMA COM PROBLEMAS SIGNIFICATIVOS" -ForegroundColor Red
}

# Salvar resultados em arquivo
$resultados | Export-Csv -Path "diagnostico_resultado.csv" -NoTypeInformation -Encoding UTF8
Write-Host "`n📄 Resultados salvos em: diagnostico_resultado.csv" -ForegroundColor Cyan

Write-Host "`n===================================" -ForegroundColor Green
Write-Host "🔍 DIAGNÓSTICO CONCLUÍDO" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
