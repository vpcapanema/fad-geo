async function finalizarProjeto() {
  const botao = document.getElementById("btnGravarProjeto");
  botao.disabled = true;
  botao.textContent = "Gravando...";

  const dados = {
    tipo_projeto: document.getElementById("tipo_projeto").value,
    nome: document.getElementById("nomeProjeto").value.trim(),
    interessado_id: document.getElementById("pjInputFinal").value,
    representante_id: document.getElementById("pfInputFinal").value,
    trecho_id: document.getElementById("trechoInputFinal").value
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/projeto/criar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(dados)
    });

    const resultado = await response.json();

    if (response.ok) {
      alert("✅ Projeto salvo com sucesso!");
      // Redirecionar ou desbloquear próxima etapa
    } else {
      alert("❌ Erro ao salvar projeto:\\n" + (resultado.detail || "Erro desconhecido"));
    }
  } catch (erro) {
    console.error("Erro na requisição:", erro);
    alert("❌ Falha na comunicação com o servidor");
  } finally {
    botao.disabled = false;
    botao.textContent = "Salvar e Continuar";
  }
}
