$(document).ready(function () {
    var idioma = {
        "sProcessing": "Procesando...",
        "sLengthMenu": "Mostrar _MENU_ registros",
        "sZeroRecords": "No se encontraron resultados",
        "sEmptyTable": "Ningún registro disponible",
        "sInfo": "Mostrando _START_ a _END_ de _TOTAL_ registros",
        "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
        "sInfoFiltered": "(filtrado de _MAX_ registros en total)",
        "sSearch": "Buscar:",
        "oPaginate": {
            "sFirst": "Primero",
            "sLast": "Último",
            "sNext": "Siguiente",
            "sPrevious": "Anterior"
        },
        "buttons": {
            "copyTitle": 'Información copiada',
            "copySuccess": {
                "_": '%d filas copiadas',
                "1": '1 fila copiada'
            }
        }
    };

    var table = $('#dataTable').DataTable({
        "paging": true,
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "language": idioma,
        "lengthMenu": [[10, 20, 30, -1], [10, 20, 30, "Mostrar Todo"]],
        "dom": '<"row"<"col-md-6"l><"col-md-6"f>>Brtip',
        "columnDefs": [
            { "orderable": false, "targets": -1 },
            { "searchable": false, "targets": -1 }
        ],
        "order": [],
        "buttons": [
            {
                extend: 'excelHtml5',
                text: '<i class="fas fa-file-excel"></i> Excel',
                className: 'btn btn-sm btn-success',
                exportOptions: { columns: ':not(:last-child)' }
            },
            {
                extend: 'pdfHtml5',
                text: '<i class="fas fa-file-pdf"></i> PDF',
                className: 'btn btn-sm btn-danger',
                exportOptions: { columns: ':not(:last-child)' },
                customize: function (doc) {
                    // Ajustar el ancho de las columnas en el PDF para que ocupe todo el espacio disponible
                    doc.content[1].table.widths = Array(doc.content[1].table.body[0].length + 1).join('*').split('');
                    
                    doc.styles.tableHeader = {
                        fillColor: '#343a40',
                        color: 'white',
                        alignment: 'center'
                    };
                    doc.styles.tableBodyEven = { alignment: 'center' };
                    doc.styles.tableBodyOdd = { alignment: 'center' };
                    doc.defaultStyle.alignment = 'center';
                }
            },
            {
                extend: 'print',
                text: '<i class="fas fa-print"></i> Imprimir',
                className: 'btn btn-sm btn-dark',
                exportOptions: { columns: ':not(:last-child)' },
                customize: function (win) {
                    $(win.document.body).find('table').css('width', '100%');
                }
            }
        ]
    });

    table.buttons().container().appendTo('#export-buttons');
});
