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

        $('#tblProducts').DataTable({
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
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
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
                        return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="'+row.cant+'">';
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
            initComplete: function (settings, json) {

            }
        });
    },

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
    $('input[name="search"]').autocomplete({
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
    });
});