$(document).ready(function() {
    $('input[type="file"]').each(function() {
        var fileInput = $(this);
        if (!fileInput.attr('id') || (fileInput.attr('id') !== 'id_logo' && fileInput.attr('id') !== 'id_imagen')) {
            return; // Evita procesar otros inputs que no sean los deseados
        }

        fileInput.hide();

        var container = $('<div>', { class: 'input-group' });

        var fileNameDisplay = $('<input>', {
            type: 'text',
            class: 'form-control',
            placeholder: 'Ningún archivo seleccionado',
            readonly: true,
        });

        var customButton = $('<button>', {
            type: 'button',
            class: 'btn btn-sm btn-info',
            html: '<i class="fas fa-folder-open"></i> Seleccionar archivo',
        });

        container.append(fileNameDisplay);
        container.append($('<div>', { class: 'input-group-append' }).append(customButton));

        fileInput.after(container);

        fileInput.on('change', function() {
            var fileName = $(this).val().split('\\').pop();
            fileNameDisplay.val(fileName);
        });

        customButton.on('click', function() {
            fileInput.click();
        });
    });
});
