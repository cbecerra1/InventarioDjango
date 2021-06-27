//Para refrescar unicamente el datatable
var tblClient;
function getData(){
    tblClient = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "names"},
            {"data": "surnames"},
            {"data": "dni"},
            {"data": "date_birthday"},
            {"data": "gender"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    getData(); //Se debe de llamar al comienzo
    //Llamo al boton del nuevo registro
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        //$('form')[0].reset();//Para que se refresque la informacion, opcion 1
        $('#myModalClient').modal('show'); //Inicializo mi componente modal, lo visualizamos
    });

    //Para ocultarse el modeal y decir que va a pasar
    $('#myModalClient').on('shown.bs.modal', function () {
        $('form')[0].reset();//Opcion2
    });

    //Para enviar los datos del formulario
    $('form').on('submit', function (e) {
        e.preventDefault();
        //var parameters = $(this).serializeArray(); //ME da un diccionario con todos los datos de mi formulario obtenidos por el metodo post
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalClient').modal('hide'); //Para cerrar el modal
            tblClient.ajax.reload();//Usando la funcion de datatable
            //getData(); //PAra que solo se actualice la tabla
            //location.reload(); //Se usa para actualizar toda la pagina
        });
    });
});

