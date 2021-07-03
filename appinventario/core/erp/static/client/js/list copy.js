//Para refrescar unicamente el datatable, esta es para usar modals, ahi que reeecuperar la vista que se hizo
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
            {"data": "gender.name"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    modal_title = $('.modal-title');
    getData(); //Se debe de llamar al comienzo
    //Llamo al boton del nuevo registro
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un cliente'); //Busca los componentes span y con html pongio el exto
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-plus');//Busca la etiqueta i, remuevo las clases y le pongo la clase fas fa-plus
        $('form')[0].reset();//Para que se refresque la informacion, opcion 1
        $('#myModalClient').modal('show'); //Inicializo mi componente modal, lo visualizamos
    });

    $('#data tbody')
        //Para editar un elemento
        .on('click', 'a[rel="edit"]', function (){
            modal_title.find('span').html('Edición de un cliente'); 
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblClient.cell($(this).closest('td, li')).index();
            var data = tblClient.row(tr.row).data();//Cuando haga click en una elemento de la tabla, especificmanete en el componente a y el vinculo edit va a pa sar algo
            //TEniendo los datos los transpaso a mis componentes
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="names"]').val(data.names);
            $('input[name="surnames"]').val(data.surnames);
            $('input[name="dni"]').val(data.dni);
            $('input[name="date_birthday"]').val(data.date_birthday);
            $('input[name="address"]').val(data.address);
            $('select[name="gender"]').val(data.gender.id);
            //Ya pase los componenest habro mi model
            $('#myModalClient').modal('show'); 
        })
        //Para borrar un elemento
        .on('click', 'a[rel="delete"]', function (){
            var tr = tblClient.cell($(this).closest('td, li')).index();
            var data = tblClient.row(tr.row).data();//Cuando haga click en una elemento de la tabla, especificmanete en el componente a y el vinculo edit va a pa sar algo
            //Envio los valores por medio de ajax a mi vista
            var parameters = new FormData();
            //En este caso le envio valores de la siguiente manera, sin el formdata
            parameters.append('action','delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el siguiente registro?', parameters, function () {
                $('#myModalClient').modal('hide');
                tblClient.ajax.reload();
            });
        });

    //Para ocultarse el modeal y decir que va a pasar
    $('#myModalClient').on('shown.bs.modal', function () {
        //$('form')[0].reset();//Opcion2
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
