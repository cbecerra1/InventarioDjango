var tblProducts; // Para recuperar los objetos y la asignamos al datatable
//Creo una variable para almacenar los datos, uso codigo javascritp y luego la envio por ajax
var vents = {
    //Va a tener todo lo que tiene mi cabecera y mi detalle
    items: {
        //Cabecera
        cli: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        //Detalle, el cual sera un array porque tiene muchos productos
        products: []
    },
    // Le coloco funciones a la estructura
    //Funcion para hacer los calculos matematicos
    calculate_invoice: function () {
        var subtotal = 0.00;// Variable para sumar y guardar la suma
        var iva = $('input[name="iva"]').val(); //Para el iva calculado, contiene lo que tiene el input iva
        //Recorremos lo que tiene mi variable, en este caso productos, con this hago referencia como si estuviera dentro de vents
        //Me muevo con la posicion y lo que tiene mi diccionario
        $.each(this.items.products, function (pos, dict) {
           //El precio de venta es un string por lo que ahi que convertilor
            dict.subtotal = dict.cant * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
        })
        this.items.subtotal = subtotal; // Lo pngo dentro de la variable de mi estructura
        this.items.iva = this.items.subtotal * iva; //Calculamos el iva 
        this.items.total = this.items.subtotal + this.items.iva;//Para calcular el total = lo que tiene subtotal + lo que tiene iva
        
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2))//Lo pongo en el input correspondiente
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2))//Lo presento en el pinput de iva
        $('input[name="total"]').val(this.items.total.toFixed(2))//Lo presento en el inputo de total
    },
    //Funcion para añadir items a la tabla
    add: function (item) {
        this.items.products.push(item);//Agrego el producto, Como es un array uso la propiedad push para poner el producto
        this.list(); //Le digo que se liste
    },
    //DEspues de seleccionar el producto listo mi estructura usando datatable, creo un metodo llamado list
    //Lista los items en el datatable
    list: function () {
        //Coloco la funcion antes de que se presente el listado
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            //Como tengo los datos no necesito la parte del ajax, lo envio por una variable
            data: this.items.products, //Llamo a items y leugo a productos usando this porque estoy dentro de la estructura
            columns: [
                { "data": "id" }, //Va a ser un boton
                { "data": "name" },
                { "data": "cat.name" },
                { "data": "pvp" },
                { "data": "cant" }, //Para cantidad la variable no se manda
                { "data": "subtotal" },
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                //La cantidad la perzonalisamos como input
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.cant+'">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            // rowCallback lo uso para modificar valores en la tabla cuando modifico otros valores
            rowCallback( row, data, displayNum, displayIndex, dataIndex){
                //Para encontrar el componente y luego le agregamos el tocuhpin
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    stepinterval: 1,
                });

            },
            initComplete: function (settings, json) {

            }
        });
    },

};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
            '<div class="row">' +
                '<div class="col-lg-1">' +
                '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
                '</div>' +
                '<div class="col-lg-11 text-left shadow-sm">' +
                    //'<br>' +
                    '<p style="margin-bottom: 0;">' +
                    '<b>Nombre:</b> ' + repo.name + '<br>' +
                    '<b>Categoría:</b> ' + repo.cat.name + '<br>' +
                    '<b>PVP:</b> <span class="badge badge-warning">$'+repo.pvp+'</span>'+
                    '</p>' +
                '</div>' +
            '</div>' +
        '</div>');

    return option;
};

$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    //Coloco el nombre de mi componente
    $('#date_joined').datetimepicker({
        //Configuraciones
        //Formato
        format: 'YYYY-MM-DD',
        // Ponemos fecha por defecto
        date: moment().format("YYYY-MM-DD"),
        // Configuramos el idioma
        locale: 'es',
        //Fecha maxima
        //maxDate: moment().format("YYYY-MM-DD"),
    });

    //Implemento para el manejo del valor del iva, manejo el nombre de la entidad
    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        vents.calculate_invoice();//De esta maanera calculamos cuando modificamos el iva
    })
    .val(0.12);

    //Hacemos la busqueda de mis productos, uso el autocomplete
    /*$('input[name="search"]').autocomplete({
        //en source usare una funcion para que por medio de ajax se conecte a mis modelos y mis bases de datos
        source: function (request, response) {
            //Hacemos los que es ajax
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term //Para obtener lo que voy escribiendo, la busqueda la guardo en la variable term
                }, //Coloc los parametros para que se conecte a mi vista
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            //console.log(ui.item); //Imprimo lo que me llega en la busqueda
            console.clear();
            //Para cantidad hago este artificio, que antes de enviarlo
            ui.item.cant = 1;//Al diccionario le agrego una variable nueva llamada cantidad, le pongo 1 para que llegue con 1 y luego el usuario aumetna la cantidad que desee
            ui.item.subtotal = 0.00;
            console.log(vents.items);
            //Como veo que me llega lo agrego a mi estructura
            vents.add(ui.item); 
            $(this).val(''); //Limpio el buscador cada vez que agrego un producto
        }
    });*/

    $('.btnRemoveAll').on('click', function () {
        if (vents.items.products.length === 0) return false;
        alert_action('Notificacion', 'Estas seguro de eliminar todos los registros?', function () {
            vents.items.products = []; //Para elimiar todo le decimos al array de productos que vuelva empezar de 0
            vents.list(); 
        }, function () {
            
        });
    });

    //Para el evento de añadir la cantidad a misproductos
    // event cant
    $('#tblProducts tbody').
        on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index(); // Trabajo c on el elemnto de cantidad para tener la posicion
            alert_action('Notificacion', 'Estas seguro de eliminar el producto?', function () {
                vents.items.products.splice(tr.row,1); //Uso mi array de columnas para estar en posicion y eliminar
                vents.list();//Actualizo el listaod
                }, function () {
                    
                });
        })
        .on('change', 'input[name="cant"]', function () {
        console.clear();
        var cant = parseInt($(this).val());
        //Para concoer la poisicon y que no se me crree un producto cada vez que agrego uno nuevo
        var tr = tblProducts.cell($(this).closest('td, li')).index(); // Con esto se cual es pa posicion
        vents.items.products[tr.row].cant = cant; //Modifico la cantidad segund su posicion colocandole la variable cant
        //Calculamos la factura
        vents.calculate_invoice();
        //ESta parte la uso para obtener el node y haci modificar en linea los ubtotales, codigo sacado de la documentacion de datatable
        //La posicion es la 5 que es la del subtotal y empiezo en 1
        //DEbe de ser d ebajo luego que se calcule la factura
        $('td:eq(5)',tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
    });

    //Para borrar los datos del buscador
    $('.btnClearSearch').on('click', function () {
       $('input[name="search"]').val('').focus();
    });

    //Codigo para hacer el envio de los datos
    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        
        //Para validar que tiene los datos guardados
        if(vents.items.products.length === 0){
            message_error('Debe almenos tener un item en su detalle de venta');
            return false;
        }
        //Ingresamos el cliente y la fecha de registro
        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.cli = $('select[name="cli"]').val();
        var parameters = new FormData();
        //Mandamos los parametros
        parameters.append('action', $('input[name="action"]').val());      
        parameters.append('vents', JSON.stringify(vents.items));  //Lo convierto en un json legible para leerlo e iterarlo    
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            alert_action('Notificación', 'Desea imprimir la factura?', function () {
                window.open('/erp/sale/invoice/pdf/'+response.id+'/','_blank'); //Para que me habra en una pestaña nueva la factura
                location.href = '/erp/sale/list/'; //Se ejecuet la lista
            }, function () {
                location.href = '/erp/sale/list/';   
            });

        });
    });

    //Para listar el datatable
    // vents.list(); //Lo quito porque ya lo estoy listando en el script de la plantilla

    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST', 
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_products'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.cant = 1;
        data.subtotal = 0.00;
        vents.add(data);
        $(this).val('').trigger('change.select2'); //Selecionamos valor vacios y usamos trigger para limpiar
    });

    vents.list();
});