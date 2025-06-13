// cd_usuario_barra_progresso.js
// Barra de progresso para o cadastro de usuário FAD
// Este script controla a barra de progresso e status das etapas do cadastro

export function iniciarBarraProgresso() {
  const progressBarContainer = document.getElementById('progressBarContainer');
  const progressBarFill = document.getElementById('progressBarFill');
  const progressBarPercent = document.getElementById('progressBarPercent');
  const progressBarStatus = document.getElementById('progressBarStatus');
  progressBarContainer.style.display = 'block';
  atualizarBarraProgresso(1, 'Iniciando cadastro...');
}

export function atualizarBarraProgresso(porcentagem, status) {
  const progressBarFill = document.getElementById('progressBarFill');
  const progressBarPercent = document.getElementById('progressBarPercent');
  const progressBarStatus = document.getElementById('progressBarStatus');
  progressBarFill.style.width = porcentagem + '%';
  progressBarPercent.textContent = porcentagem + '%';
  if (status) progressBarStatus.textContent = status;
}

export async function executarFluxoCadastroUsuario(form, btnCadastrar) {
  iniciarBarraProgresso();
  btnCadastrar.disabled = true;
  
  // Abre conexão WebSocket apenas para mostrar progresso cosmético
  const ws = new WebSocket("ws://localhost:8000/ws/cadastro-usuario");
  ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.erro) {
      atualizarBarraProgresso(data.progresso || 0, `Erro [${data.codigo}]: ${data.mensagem}`);
      document.getElementById('erroBox').style.display = 'block';
      document.getElementById('erroBox').textContent = data.mensagem;
      ws.close();
      btnCadastrar.disabled = false;
      return;
    }
    atualizarBarraProgresso(data.progresso, data.status);
    if (data.progresso === 100) {
      document.getElementById('sucessoBox').style.display = 'block';
      ws.close();
      btnCadastrar.disabled = false;
    }
  };
  ws.onerror = function() {
    atualizarBarraProgresso(0, 'Erro de conexão com o servidor.');
    btnCadastrar.disabled = false;
  };
  
  // NÃO faz submit do formulário aqui - o envio é feito via fetch no script principal
  // form.submit(); // REMOVIDO
}
