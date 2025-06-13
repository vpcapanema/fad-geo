
# Caminhos base
$jsRoot = "C:\Users\vinic\fad_espacial\app\static\js"
$cssRoot = "C:\Users\vinic\fad_espacial\app\static\css"

# Apagar estrutura antiga
Remove-Item "$jsRoot\cadastro_projeto" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$cssRoot\cadastro_projeto" -Recurse -Force -ErrorAction SilentlyContinue

# Nova estrutura
$modulos = @(
    "01.Cadastro_Projeto",
    "02.Conformidade_Ambiental",
    "03.Multicriterio",
    "04.Socioeconomico",
    "05.Infraestrutura"
)

$submodulosCadastro = @(
    "01.Cadastro",
    "02.Validacao_geometria",
    "03.Croqui_projeto",
    "04.Selecao_modulos",
    "05.Finalizar_cadastro"
)

# Criar diretórios JS e CSS
foreach ($mod in $modulos) {
    New-Item -ItemType Directory -Force -Path "$jsRoot\modulos\$mod" | Out-Null
    New-Item -ItemType Directory -Force -Path "$cssRoot\modulos\$mod" | Out-Null
}

foreach ($sub in $submodulosCadastro) {
    New-Item -ItemType Directory -Force -Path "$jsRoot\modulos\01.Cadastro_Projeto\$sub" | Out-Null
    New-Item -ItemType Directory -Force -Path "$cssRoot\modulos\01.Cadastro_Projeto\$sub" | Out-Null
}

# Gerar JS principal em Cadastro
Set-Content "$jsRoot\modulos\01.Cadastro_Projeto\01.Cadastro\01.Cadastrar_Projeto.js" @'
function confirmarProjeto() {
  const tipo = document.getElementById("tipo_projeto");
  const nome = document.getElementById("nomeProjeto");
  const texto = `✅ <strong>Tipo de projeto:</strong> ${tipo.options[tipo.selectedIndex].text}<br>✅ <strong>Nome do projeto:</strong> ${nome.value}`;
  document.getElementById("resumoProjetoTexto").innerHTML = texto;
  tipo.disabled = true;
  nome.readOnly = true;
  document.getElementById("containerConfirmarProjeto").style.display = "none";
  document.getElementById("resumoProjeto").classList.remove("hidden");
  verificarGravacao();
}

function editarProjeto() {
  const tipo = document.getElementById("tipo_projeto");
  const nome = document.getElementById("nomeProjeto");
  tipo.disabled = false;
  nome.readOnly = false;
  document.getElementById("containerConfirmarProjeto").style.display = "block";
  document.getElementById("resumoProjeto").classList.add("hidden");
  verificarGravacao();
}

function confirmarPJ() {
  const select = document.getElementById("pjSelect");
  const texto = select.options[select.selectedIndex].textContent;
  const [razao, cnpj] = texto.split(' (');
  document.getElementById("pjResumoTexto").innerHTML = `✅ <strong>Interessado:</strong> ${razao}<br>✅ <strong>CNPJ:</strong> ${cnpj.replace(')', '')}`;
  document.getElementById("pjInputFinal").value = select.value;
  document.getElementById("boxPJ").classList.add("hidden");
  document.getElementById("resumoPJ").classList.remove("hidden");
  verificarGravacao();
}

function editarPJ() {
  document.getElementById("resumoPJ").classList.add("hidden");
  document.getElementById("boxPJ").classList.remove("hidden");
  document.getElementById("pjSelect").value = "";
}

function confirmarPF() {
  const select = document.getElementById("pfSelect");
  const texto = select.options[select.selectedIndex].textContent;
  const [nome, cpf] = texto.split(' (');
  document.getElementById("pfResumoTexto").innerHTML = `✅ <strong>Nome:</strong> ${nome}<br>✅ <strong>CPF:</strong> ${cpf.replace(')', '')}`;
  document.getElementById("pfInputFinal").value = select.value;
  document.getElementById("boxPF").classList.add("hidden");
  document.getElementById("resumoPF").classList.remove("hidden");
  verificarGravacao();
}

function editarPF() {
  document.getElementById("resumoPF").classList.add("hidden");
  document.getElementById("boxPF").classList.remove("hidden");
  document.getElementById("pfSelect").value = "";
}

function confirmarTrecho() {
  const select = document.getElementById("trechoSelect");
  const texto = select.options[select.selectedIndex].textContent;
  const partes = texto.split(" - ");
  const codigo = partes[0];
  const [nome, municipio] = partes[1].split(" (");
  document.getElementById("trechoResumoTexto").innerHTML = `✅ <strong>Código:</strong> ${codigo}<br>✅ <strong>Nome:</strong> ${nome}<br>✅ <strong>Município/UF:</strong> ${municipio.replace(")", "")}`;
  document.getElementById("trechoInputFinal").value = select.value;
  document.getElementById("boxTrecho").classList.add("hidden");
  document.getElementById("resumoTrecho").classList.remove("hidden");
  verificarGravacao();
}

function editarTrecho() {
  document.getElementById("resumoTrecho").classList.add("hidden");
  document.getElementById("boxTrecho").classList.remove("hidden");
  document.getElementById("trechoSelect").value = "";
}

function verificarGravacao() {
  const nome = document.querySelector("input[name='nome']").value.trim();
  const pfOk = document.getElementById("pfInputFinal")?.value;
  const pjOk = document.getElementById("pjInputFinal")?.value;
  const trechoOk = document.getElementById("trechoInputFinal")?.value;
  const botao = document.getElementById("btnGravarProjeto");
  const pronto = nome && pfOk && pjOk && trechoOk;
  if (pronto) {
    botao.classList.add("ativo");
    botao.disabled = false;
  } else {
    botao.classList.remove("ativo");
    botao.disabled = true;
  }
}
'@

# Criar CSS vazio correspondente
Set-Content "$cssRoot\modulos\01.Cadastro_Projeto\01.Cadastro\01.Cadastrar_Projeto.css" "/* Estilos reservados */"
