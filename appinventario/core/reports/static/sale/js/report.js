$(function () {
    $('input[name="date_range"]').daterangepicker({
        locale : {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-chart-pie"></i> Aceptar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    });
});