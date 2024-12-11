document.addEventListener('DOMContentLoaded', function () {
    // Ocultar automaticamente as mensagens após 5 segundos
    setTimeout(function () {
      let alerts = document.querySelectorAll('.alert');
      alerts.forEach(function (alert) {
        let bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      });
    }, 5000);
  });