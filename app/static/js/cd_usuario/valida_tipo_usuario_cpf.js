// Validação dinâmica de tipo de usuário para CPF (carrega todos os tipos do CPF ao confirmar dados pessoais)
// Requer jQuery

let tiposUsuarioExistentesCPF = [];

function buscarTiposUsuarioPorCPF(cpf, callback) {
    if (!cpf) return callback([]);
    $.ajax({
        url: '/api/cd/tipos-usuario-cpf',
        method: 'GET',
        data: { cpf: cpf },
        success: function(res) {
            tiposUsuarioExistentesCPF = res && Array.isArray(res.tipos) ? res.tipos : [];
            callback(tiposUsuarioExistentesCPF);
        },
        error: function() {
            tiposUsuarioExistentesCPF = [];
            callback([]);
        }
    });
}

$(function() {
    // Quando o usuário confirmar os dados pessoais
    $('#confirmarPFBtn').on('click', function() {
        var cpf = $('#cpf').val().replace(/\D/g, '');
        if (cpf.length === 11) {
            buscarTiposUsuarioPorCPF(cpf, function() {
                // Tipos carregados em tiposUsuarioExistentesCPF
            });
        } else {
            tiposUsuarioExistentesCPF = [];
        }
    });

    // Quando selecionar o tipo de usuário
    $('#tipo_usuario').on('change', function() {
        var tipo = $(this).val();
        if (tipo && tiposUsuarioExistentesCPF.length > 0) {
            if (tiposUsuarioExistentesCPF.includes(tipo)) {
                this.setCustomValidity('Já existe um usuário desse tipo para este CPF.');
                alert('Já existe um usuário desse tipo para este CPF.');
            } else {
                this.setCustomValidity('');
            }
        } else {
            this.setCustomValidity('');
        }
    });
});
