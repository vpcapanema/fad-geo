const fileInput = document.getElementById("fileInput");
const fileNameField = document.getElementById("fileName");
const uploadButton = document.getElementById("uploadButton");
const progressContainer = document.getElementById("progressContainer");
const uploadProgress = document.getElementById("uploadProgress");
const resultMessage = document.getElementById("resultMessage");
const errorMessage = document.getElementById("errorMessage");
const validateButton = document.getElementById("validateButton");
const validationResult = document.getElementById("validationResult");
const btnRelatorioValidacao = document.getElementById("btnRelatorioValidacao");

const API_BASE_URL = "http://127.0.0.1:8000";
let uploadInProgress = false;

fileInput.addEventListener("change", () => {
  fileNameField.value = fileInput.files.length ? fileInput.files[0].name : "Selecionar arquivo";
  uploadButton.disabled = !fileInput.files.length || uploadInProgress;
});

uploadButton.addEventListener("click", async () => {
  if (!fileInput.files.length) return;

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("arquivo", file);

  uploadInProgress = true;
  uploadButton.disabled = true;
  progressContainer.style.display = "block";
  uploadProgress.value = 0;

  try {
    const response = await fetch(`${API_BASE_URL}/upload/`, {
      method: "POST",
      body: formData
    });
    const data = await response.json();
    handleUploadResponse(data);
  } catch (error) {
    handleUploadError(error);
  } finally {
    uploadInProgress = false;
    uploadButton.disabled = false;
  }
});

const handleUploadResponse = (data) => {
  progressContainer.style.display = "none";
  const btnRelatorio = document.getElementById("btnRelatorioUpload");

  if (data.sucesso) {
    resultMessage.classList.remove("hidden");
    errorMessage.classList.add("hidden");
    validateButton.classList.remove("hidden");
    btnRelatorio.style.display = "none";
  } else {
    resultMessage.classList.add("hidden");
    errorMessage.classList.remove("hidden");
    errorMessage.innerHTML = data.erros ?
      `❌ Erros:<br><ul>${data.erros.map(e => `<li>${e}</li>`).join("")}</ul>` :
      "❌ Erro desconhecido";
    btnRelatorio.href = data.relatorio || "#";
    btnRelatorio.style.display = data.relatorio ? "inline-block" : "none";
  }
};

const handleUploadError = (error) => {
  console.error("Erro no upload:", error);
  progressContainer.style.display = "none";
  resultMessage.classList.add("hidden");
  errorMessage.classList.remove("hidden");
  errorMessage.innerHTML = "❌ Falha na comunicação com o servidor";
};

validateButton.addEventListener("click", async () => {
  validationResult.classList.remove("hidden");
  validationResult.innerHTML = "Validando...";
  validationResult.style.color = "inherit";

  try {
    const response = await fetch(`${API_BASE_URL}/geometria/validar`);
    const data = await response.json();

    if (data.validado) {
      validationResult.style.color = "green";
      validationResult.innerHTML = "✔️ Geometria válida";
    } else {
      validationResult.style.color = "red";
      validationResult.innerHTML = data.erros ?
        `❌ Problemas:<br><ul>${data.erros.map(e => `<li>${e}</li>`).join("")}</ul>` :
        "❌ Geometria inválida";
    }

    if (data.relatorio) {
      btnRelatorioValidacao.href = data.relatorio;
      btnRelatorioValidacao.classList.remove("hidden");
    }
  } catch (error) {
    console.error("Erro na validação:", error);
    validationResult.style.color = "red";
    validationResult.innerHTML = "❌ Falha na validação";
  }
});
