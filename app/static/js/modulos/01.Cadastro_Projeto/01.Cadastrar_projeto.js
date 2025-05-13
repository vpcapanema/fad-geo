// ==================== INICIALIZAÇÃO GERAL DO FORMULÁRIO ====================

// Espera o DOM carregar totalmente antes de executar
document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ JS carregado e executando");

  // Referências aos campos do subcontainer Projeto
  const tipoProjeto = document.getElementById("tipo_projeto");
  const nomeProjeto = document.getElementById("nomeProjeto");
  const btnConfirmar = document.getElementById("btnConfirmarProjeto");

  // Atualiza o estado de habilitação do botão Confirmar Projeto
  function atualizarEstadoBotao() {
    const tipoSelecionado = tipoProjeto.value !== "";
    const nomeValido = nomeProjeto.value.trim().length >= 5;

    if (tipoSelecionado) {
      btnConfirmar.classList.remove("hidden");
    } else {
      btnConfirmar.classList.add("hidden");
    }

    btnConfirmar.disabled = !(tipoSelecionado && nomeValido);
  }

  tipoProjeto.addEventListener("change", atualizarEstadoBotao);
  nomeProjeto.addEventListener("input", atualizarEstadoBotao);

  btnConfirmar.addEventListener("click", confirmarProjeto);
});

// Confirma as informações do subcontainer Projeto
function confirmarProjeto() {
  const tipo = document.getElementById("tipo_projeto");
  const nome = document.getElementById("nomeProjeto");
  const texto = `✅ <strong>Tipo:</strong> ${tipo.options[tipo.selectedIndex].text}<br />✅ <strong>Nome:</strong> ${nome.value}`;

  document.getElementById("resumoProjetoTexto").innerHTML = texto;
  tipo.disabled = true;
  nome.readOnly = true;
  document.getElementById("btnConfirmarProjeto").classList.add("hidden");
  document.getElementById("resumoProjeto").classList.remove("hidden");

  if (typeof verificarGravacao === 'function') verificarGravacao();
}

// Permite editar novamente o Projeto
function editarProjeto() {
  const tipo = document.getElementById("tipo_projeto");
  const nome = document.getElementById("nomeProjeto");

  tipo.disabled = false;
  nome.readOnly = false;

  document.getElementById("resumoProjeto").classList.add("hidden");
  document.getElementById("btnConfirmarProjeto").classList.remove("hidden");

  if (typeof verificarGravacao === 'function') verificarGravacao();
}

// ==================== FUNÇÃO GENÉRICA: ATUALIZAR LISTAS DE SELECT ====================

// Atualiza dinamicamente selects usando dados JSON
async function atualizarLista(url, selectId, tipo) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    const select = document.getElementById(selectId);
    select.innerHTML = '<option value="">Selecione...</option>';

    data.forEach(item => {
      const option = document.createElement("option");
      option.value = item.id;

      if (tipo === "pf") {
        option.textContent = `${item.nome} (${item.cpf})`;
      } else if (tipo === "pj") {
        option.textContent = `${item.razao_social} (${item.cnpj})`;
      } else if (tipo === "trecho") {
        option.textContent = `${item.codigo} - ${item.denominacao} (${item.municipio})`;
      } else if (tipo === "rodovia") {
        option.textContent = `${item.codigo} - ${item.nome} (${item.uf})`;
      }

      select.appendChild(option);
    });
  } catch (error) {
    console.error("Erro ao atualizar a lista de", tipo);
  }
}

// ==================== LÓGICA DO SUBCONTAINER 2: INTERESSADO (PJ) ====================

document.addEventListener("DOMContentLoaded", function () {
  const opcaoPJ = document.getElementById("opcaoPJ");
  const boxPJ = document.getElementById("boxPJ");
  const atualizarPJBtn = document.getElementById("atualizarPJBtn");

  // Controla se abre ou não a caixa de seleção de PJ
  opcaoPJ.addEventListener("change", function () {
    const valor = opcaoPJ.value;

    if (valor === "cadastrar") {
      window.open("/cadastro-interessado-pj", "_blank");
      boxPJ.classList.add("hidden");
    } else if (valor === "associar") {
      boxPJ.classList.remove("hidden");
    } else {
      boxPJ.classList.add("hidden");
    }
  });

  // Atualiza a lista de PJs cadastrados
  atualizarPJBtn?.addEventListener("click", function () {
    atualizarLista("/cadastro/pjs/json", "pjSelect", "pj");
  });
});

// Confirma a seleção de PJ
function confirmarPJ() {
  const select = document.getElementById("pjSelect");
  const texto = select.options[select.selectedIndex].textContent;

  const match = texto.match(/^(.*?) \((\d{14})\)$/);
  const razao = match ? match[1] : texto;
  const cnpj = match ? match[2].replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, "$1.$2.$3/$4-$5") : "";

  document.getElementById("pjResumoRazao").textContent = razao;
  document.getElementById("pjResumoCNPJ").textContent = cnpj;
  document.getElementById("pjInputFinal").value = select.value;

  document.getElementById("boxPJ").classList.add("hidden");
  document.getElementById("resumoPJ").classList.remove("hidden");

  verificarGravacao();
}

// Permite editar novamente o PJ
function editarPJ() {
  document.getElementById("resumoPJ").classList.add("hidden");
  document.getElementById("boxPJ").classList.remove("hidden");
  document.getElementById("pjSelect").value = "";

  verificarGravacao();
}

// ==================== LÓGICA DO SUBCONTAINER 3: REPRESENTANTE LEGAL (PF) ====================

document.getElementById("opcaoPF").addEventListener("change", function () {
  const box = document.getElementById("boxPF");
  if (this.value === "cadastrar") {
    window.open("/cadastro-interessado-pf", "_blank");
  } else if (this.value === "associar") {
    box.classList.remove("hidden");
  } else {
    box.classList.add("hidden");
  }
});

// Atualiza lista de PFs
document.getElementById("atualizarPFBtn")?.addEventListener("click", () => {
  atualizarLista("/cadastro/pfs/json", "pfSelect", "pf");
});

// Controla habilitação do botão Confirmar PF
document.getElementById("pfSelect").addEventListener("change", function () {
  const botao = document.querySelector("button[onclick='confirmarPF()']");
  botao.disabled = !this.value;
});

// Confirma a PF selecionada
function confirmarPF() {
  const select = document.getElementById("pfSelect");
  const texto = select.options[select.selectedIndex].textContent;

  const match = texto.match(/^(.*?) \((\d{11})\)$/);
  const nome = match ? match[1] : texto;
  const cpf = match ? match[2].replace(/^(\d{3})(\d{3})(\d{3})(\d{2})$/, "$1.$2.$3-$4") : "";

  document.getElementById("pfResumoNome").textContent = nome;
  document.getElementById("pfResumoCPF").textContent = cpf;
  document.getElementById("pfInputFinal").value = select.value;

  document.getElementById("boxPF").classList.add("hidden");
  document.getElementById("resumoPF").classList.remove("hidden");

  verificarGravacao();
}

// Permite editar novamente a PF
function editarPF() {
  document.getElementById("resumoPF").classList.add("hidden");
  document.getElementById("boxPF").classList.remove("hidden");

  const select = document.getElementById("pfSelect");
  select.value = "";

  const botao = document.querySelector("button[onclick='confirmarPF()']");
  botao.disabled = true;

  verificarGravacao();
}

// ==================== LÓGICA DO SUBCONTAINER 4: ELEMENTO RODOVIÁRIO ====================

// Exibe Rodovia ou Trecho conforme o tipo selecionado
// Mostra as opções de associar/cadastrar dependendo do tipo selecionado
document.getElementById("tipo_elemento").addEventListener("change", function () {
  const valor = this.value;
  const opcao = document.getElementById("opcaoElemento");
  const container = document.getElementById("opcaoElementoContainer");

  // Oculta todas as caixas
  document.getElementById("boxRodovia").classList.add("hidden");
  document.getElementById("boxTrecho").classList.add("hidden");

  // Limpa a seleção anterior
  opcao.value = "";
  container.classList.toggle("hidden", valor === "");
});

// Quando usuário seleciona "associar" ou "cadastrar"
document.getElementById("opcaoElemento").addEventListener("change", function () {
  const tipo = document.getElementById("tipo_elemento").value;
  const valor = this.value;

  // Oculta as duas caixas
  document.getElementById("boxRodovia").classList.add("hidden");
  document.getElementById("boxTrecho").classList.add("hidden");

  if (valor === "cadastrar") {
    // Sempre redireciona para a mesma página
    window.open("/cadastro-trecho", "_blank");
  } else if (valor === "associar") {
    if (tipo === "rodovia") {
      document.getElementById("boxRodovia").classList.remove("hidden");
    } else if (tipo === "trecho") {
      document.getElementById("boxTrecho").classList.remove("hidden");
    }
  }
});

// Atualiza listas de rodovias e trechos
document.getElementById("atualizarRodoviaBtn")?.addEventListener("click", () => {
  atualizarLista("/cadastro/trechos/json", "trechoSelect", "trecho");
});

document.getElementById("atualizarTrechoBtn")?.addEventListener("click", () => {
  atualizarLista("/cadastro/trechos/json", "trechoSelect", "trecho");
});

// Controle do botão confirmar rodovia
document.getElementById("rodoviaSelect")?.addEventListener("change", function () {
  const botao = document.querySelector("button[onclick='confirmarRodovia()']");
  botao.disabled = !this.value;
});

// Controle do botão confirmar trecho
document.getElementById("trechoSelect")?.addEventListener("change", function () {
  const botao = document.querySelector("button[onclick='confirmarTrecho()']");
  botao.disabled = !this.value;
});

// Confirma rodovia selecionada
function confirmarRodovia() {
  const select = document.getElementById("rodoviaSelect");
  const texto = select.options[select.selectedIndex].textContent;

  const match = texto.match(/^(.+?)\s*-\s*(.+?)\s*\((.+?)\)$/);
  const codigo = match ? match[1] : "";
  const nome = match ? match[2] : texto;
  const uf = match ? match[3] : "";

  document.getElementById("trechoResumoTipo").textContent = "Rodovia";
  document.getElementById("trechoResumoCodigo").textContent = codigo;
  document.getElementById("trechoResumoDenominacao").textContent = nome;
  document.getElementById("trechoResumoMunicipio").textContent = uf;

  document.getElementById("trechoInputFinal").value = select.value;
  document.getElementById("boxRodovia").classList.add("hidden");
  document.getElementById("resumoTrecho").classList.remove("hidden");

  verificarGravacao();
}

// Confirma trecho selecionado
function confirmarTrecho() {
  const tipo = document.getElementById("tipo_elemento");
  const select = document.getElementById("trechoSelect");
  const texto = select.options[select.selectedIndex].textContent;

  const tipoSelecionado = tipo.options[tipo.selectedIndex].text;
  const match = texto.match(/^(\w+)\s*-\s*(.*?) \((.*?)\)$/);

  const codigo = match ? match[1] : "";
  const denominacao = match ? match[2] : texto;
  const municipio = match ? match[3] : "";

  document.getElementById("trechoResumoTipo").textContent = tipoSelecionado;
  document.getElementById("trechoResumoCodigo").textContent = codigo;
  document.getElementById("trechoResumoDenominacao").textContent = denominacao;
  document.getElementById("trechoResumoMunicipio").textContent = municipio;

  document.getElementById("trechoInputFinal").value = select.value;
  document.getElementById("boxTrecho").classList.add("hidden");
  document.getElementById("resumoTrecho").classList.remove("hidden");

  verificarGravacao();
}

// ==================== VERIFICAÇÃO FINAL DE GRAVAÇÃO ====================

// Habilita ou desabilita botão Gravar Projeto
function verificarGravacao() {
  const nome = document.querySelector("input[name='nome']")?.value.trim();
  const pfOk = document.getElementById("pfInputFinal")?.value;
  const pjOk = document.getElementById("pjInputFinal")?.value;
  const trechoOk = document.getElementById("trechoInputFinal")?.value;
  const botao = document.getElementById("btnGravarProjeto");

  if (!botao) return; // evita erro se o botão não existir

  const pronto = nome && pfOk && pjOk && trechoOk;
  if (pronto) {
    botao.classList.add("ativo");
    botao.disabled = false;
  } else {
    botao.classList.remove("ativo");
    botao.disabled = true;
  }
}
