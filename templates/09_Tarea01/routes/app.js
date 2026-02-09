
let data = [];              // arreglo de productos agregados
let indexEdit = null;       // índice del producto que se está editando
let indexToDelete = null;   // índice pendiente de eliminar (para el modal)

// Dibuja todas las filas en la tabla en base a "data"
function pintarTabla() {
    const $tbody = $("#lista tbody");
    $tbody.empty();

    let totalGeneral = 0;

    data.forEach((item, index) => {
        const total = item.precio * item.cantidad;
        totalGeneral += total;

        const row = `
            <tr data-index="${index}">
                <td>${item.nombre}</td>
                <td>$${item.precio.toFixed(2)}</td>
                <td>${item.cantidad}</td>
                <td>$${total.toFixed(2)}</td>
                <td>
                    <button type="button" class="btn btn-sm btn-primary btn-editar">Editar</button>
                    <button type="button" class="btn btn-sm btn-danger btn-eliminar">Eliminar</button>
                </td>
            </tr>`;

        $tbody.append(row);
    });

    // Mostrar total general abajo
    $("#total").text("Total General: $" + totalGeneral.toFixed(2));
}

function limpiarFormulario() {
    $("#producto").val("");
    $("#precio").val("");
    $("#cantidad").val("");
    $("#nombre").val("");
    indexEdit = null;
}

$(document).ready(function () {
    // Click en "+ Agregar"
    $("#agregar").on("click", function () {
        const idProducto = $("#producto").val();
        const nombre = $("#nombre").val() || $("#producto option:selected").text();
        const precio = parseFloat($("#precio").val());
        const cantidad = parseInt($("#cantidad").val(), 10);

        if (!idProducto) {
            alert("Seleccione un producto.");
            return;
        }
        if (isNaN(precio) || precio <= 0) {
            alert("Precio inválido.");
            return;
        }
        if (isNaN(cantidad) || cantidad <= 0) {
            alert("Cantidad inválida.");
            return;
        }

        const item = {
            id: idProducto,
            nombre: nombre,
            precio: precio,
            cantidad: cantidad
        };

        if (indexEdit === null) {
            // Agregar nuevo
            data.push(item);
        } else {
            // Actualizar existente
            data[indexEdit] = item;
        }

        pintarTabla();
        limpiarFormulario();
    });

    // Delegación para botón Eliminar (abre modal de confirmación)
    $("#lista").on("click", ".btn-eliminar", function () {
        const idx = $(this).closest("tr").data("index");
        indexToDelete = idx;
        $("#modalEliminar").modal("show");
    });

    // Confirmar eliminación en el modal
    $("#btnConfirmarEliminar").on("click", function () {
        if (indexToDelete !== null) {
            data.splice(indexToDelete, 1);
            indexToDelete = null;
            pintarTabla();
        }
        $("#modalEliminar").modal("hide");
    });

    // Delegación para botón Editar: mostrar tabla de edición individual
    $("#lista").on("click", ".btn-editar", function () {
        const idx = $(this).closest("tr").data("index");
        const item = data[idx];

        if (!item) return;

        indexEdit = idx;

        // Cargar datos en la tabla de edición
        $("#edit-nombre").val(item.nombre);
        $("#edit-precio").val(item.precio.toFixed(2));
        $("#edit-cantidad").val(item.cantidad);
        $("#edit-total").val((item.precio * item.cantidad).toFixed(2));

        // Mostrar editor
        $("#editor").slideDown();
    });

    // Recalcular total cuando cambia la cantidad en el editor
    $("#edit-cantidad").on("input", function () {
        const precio = parseFloat($("#edit-precio").val()) || 0;
        const cantidad = parseInt($(this).val(), 10) || 0;
        const total = precio * cantidad;
        $("#edit-total").val(total.toFixed(2));
    });

    // Guardar cambios desde la tabla de edición
    $("#edit-guardar").on("click", function () {
        if (indexEdit === null) return;

        const cantidad = parseInt($("#edit-cantidad").val(), 10);
        if (isNaN(cantidad) || cantidad <= 0) {
            alert("Cantidad inválida.");
            return;
        }

        const item = data[indexEdit];
        item.cantidad = cantidad;

        pintarTabla();

        // Ocultar editor y limpiar índice
        $("#editor").slideUp();
        indexEdit = null;
    });

    // Cancelar edición
    $("#edit-cancelar").on("click", function () {
        $("#editor").slideUp();
        indexEdit = null;
    });

    // Guardar en Base de Datos: generar inputs ocultos y enviar el formulario
    $("#guardar").on("click", function () {
        if (data.length === 0) {
            alert("No hay productos para guardar.");
            return;
        }

        const $form = $("#formProductos");

        // Eliminar inputs ocultos anteriores (si los hay)
        $form.find(".item-hidden").remove();

        data.forEach(item => {
            const total = item.precio * item.cantidad;

            $form.append(`<input type="hidden" class="item-hidden" name="nombre[]" value="${item.nombre}">`);
            $form.append(`<input type="hidden" class="item-hidden" name="precio[]" value="${item.precio}">`);
            $form.append(`<input type="hidden" class="item-hidden" name="cantidad[]" value="${item.cantidad}">`);
            $form.append(`<input type="hidden" class="item-hidden" name="total[]" value="${total}">`);
        });

        // Enviar formulario normal 
        $form.submit();
    });
});
