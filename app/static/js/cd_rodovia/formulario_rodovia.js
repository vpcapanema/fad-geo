// Validação e formatação para formulário de Rodovia
// Sistema FAD - Módulo individualizado

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById("rodoviaForm");
  const sucessoBox = document.getElementById("sucessoBox");
  const erroBox = document.getElementById("erroBox");
  const codigoInput = document.getElementById("codigo");
  const denominacaoInput = document.getElementById("denominacao");
  const tipoInput = document.getElementById("tipo");
  const municipioSelect = document.getElementById("municipio");
  const extensaoInput = document.getElementById("extensao_km");

  // Utilitários de formatação
  function capitalizarNome(str) {
    if (!str) return str;
    const preposicoes = new Set(["da", "de", "do", "das", "dos", "e", "em", "na", "no"]);
    return str.toLowerCase().split(' ').map(palavra => 
      preposicoes.has(palavra) ? palavra : palavra.charAt(0).toUpperCase() + palavra.slice(1)
    ).join(' ');
  }

  function formatarCodigo(valor) {
    return valor.toUpperCase().replace(/[^A-Z0-9-]/g, '');
  }

  function validarCodigo(codigo) {
    const regex = /^[A-Z]{2,}-\d{3,}$/;
    return regex.test(codigo);
  }

  function validarExtensao(extensao) {
    if (!extensao) return true; // Campo opcional
    const num = parseFloat(extensao);
    return !isNaN(num) && num > 0;
  }

  // Feedback visual e mensagens de erro
  function updateFieldValidation(input, isValid) {
    const field = input.closest('.form-field');
    if (!field) return;
    field.classList.remove('campo-validado', 'campo-erro');
    input.classList.remove('erro-campo');
    if (input.value.trim()) {
      if (isValid) {
        field.classList.add('campo-validado');
      } else {
        field.classList.add('campo-erro');
        input.classList.add('erro-campo');
      }
    }
  }
  function showFieldError(input, message) {
    let errorDiv = input.parentNode.querySelector('.error-message') || input.parentNode.querySelector('[id$="-erro"]');
    if (!errorDiv) {
      errorDiv = document.createElement('div');
      errorDiv.className = 'error-message';
      errorDiv.style.color = 'red';
      errorDiv.style.fontSize = '13px';
      errorDiv.style.marginTop = '2px';
      input.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
  }
  function hideFieldError(input) {
    const errorDiv = input.parentNode.querySelector('.error-message') || input.parentNode.querySelector('[id$="-erro"]');
    if (errorDiv) {
      errorDiv.textContent = '';
      errorDiv.style.display = 'none';
    }
  }

  // Validação em tempo real
  if (codigoInput) {
    codigoInput.addEventListener("input", function() {
      this.value = formatarCodigo(this.value);
      const isValid = validarCodigo(this.value);
      updateFieldValidation(this, isValid);
      if (this.value && !isValid) {
        showFieldError(this, "Formato: duas letras maiúsculas, hífen, três números (ex: RO-123)");
      } else {
        hideFieldError(this);
      }
    });
  }
  if (denominacaoInput) {
    denominacaoInput.addEventListener("input", function() {
      this.value = capitalizarNome(this.value);
      const isValid = this.value.trim().length >= 2;
      updateFieldValidation(this, isValid);
      if (this.value && !isValid) {
        showFieldError(this, "Denominação deve ter pelo menos 2 caracteres");
      } else {
        hideFieldError(this);
      }
    });
  }
  if (tipoInput) {
    tipoInput.addEventListener("input", function() {
      this.value = capitalizarNome(this.value);
      updateFieldValidation(this, true); // tipo é opcional
      hideFieldError(this);
    });
  }
  if (municipioSelect) {
    municipioSelect.addEventListener("change", function() {
      updateFieldValidation(this, true); // municipio é opcional
      hideFieldError(this);
    });
  }
  if (extensaoInput) {
    extensaoInput.addEventListener("input", function() {
      const isValid = validarExtensao(this.value);
      updateFieldValidation(this, isValid);
      if (this.value && !isValid) {
        showFieldError(this, "Extensão deve ser um número maior que zero");
      } else {
        hideFieldError(this);
      }
    });
  }

  // Carregar municípios SP
  async function carregarMunicipios() {
    try {
      const response = await fetch('/static/municipios_sp.json');
      const municipios = await response.json();
      if (municipioSelect) {
        municipios.forEach(municipio => {
          const option = document.createElement('option');
          option.value = municipio;
          option.textContent = municipio;
          municipioSelect.appendChild(option);
        });
      }
    } catch (error) {
      console.error('Erro ao carregar municípios:', error);
    }
  }

  // Validação do formulário
  function validarFormulario() {
    const dados = new FormData(form);
    const formData = Object.fromEntries(dados);
    if (!formData.codigo || !formData.denominacao) {
      return { valid: false, message: "Preencha os campos obrigatórios: código e denominação." };
    }
    if (!validarCodigo(formData.codigo)) {
      return { valid: false, message: "Código deve seguir o formato RO-123." };
    }
    if (formData.denominacao.trim().length < 2) {
      return { valid: false, message: "Denominação deve ter pelo menos 2 caracteres." };
    }
    if (formData.extensao_km && !validarExtensao(formData.extensao_km)) {
      return { valid: false, message: "Extensão deve ser um número válido maior que zero." };
    }
    return { valid: true };
  }

  // Envio do formulário
  if (form) {
    form.addEventListener("submit", async function(event) {
      event.preventDefault();
      sucessoBox.style.display = "none";
      erroBox.style.display = "none";
      // Validar formulário
      const validation = validarFormulario();
      if (!validation.valid) {
        erroBox.textContent = validation.message;
        erroBox.style.display = "block";
        return;
      }
      const formData = Object.fromEntries(new FormData(form));
      try {
        const response = await fetch("/api/cd/rodovia/cadastrar", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (response.ok && result.success) {
          sucessoBox.textContent = result.message || "Rodovia cadastrada com sucesso!";
          sucessoBox.style.display = "block";
          form.reset();
          // Limpar validações visuais
          form.querySelectorAll('.form-field').forEach(field => {
            field.classList.remove('campo-validado', 'campo-erro');
          });
          form.querySelectorAll('input, select').forEach(input => {
            input.classList.remove('erro-campo');
            hideFieldError(input);
          });
        } else {
          erroBox.textContent = result.detail || result.message || "Erro ao cadastrar rodovia.";
          erroBox.style.display = "block";
        }
      } catch (error) {
        console.error('Erro ao enviar formulário:', error);
        erroBox.textContent = "Erro de conexão. Tente novamente.";
        erroBox.style.display = "block";
      }
    });
  }

  // Inicialização
  carregarMunicipios();
});
