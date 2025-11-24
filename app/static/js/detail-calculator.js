// Cálculo automático de subtotal en formularios de detalles de venta/compra

document.addEventListener('DOMContentLoaded', function() {
    const productoSelect = document.getElementById('producto');
    const cantidadInput = document.getElementById('cantidad');
    const precioInput = document.getElementById('precio_unitario');
    const subtotalSpan = document.getElementById('subtotal');

    if (productoSelect) {
        productoSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const price = selectedOption.getAttribute('data-price');
            if (price) {
                precioInput.value = parseFloat(price).toFixed(2);
                calcularSubtotal();
            }
        });
    }

    if (cantidadInput) {
        cantidadInput.addEventListener('input', calcularSubtotal);
    }

    if (precioInput) {
        precioInput.addEventListener('input', calcularSubtotal);
    }

    function calcularSubtotal() {
        const cantidad = parseFloat(cantidadInput.value) || 0;
        const precio = parseFloat(precioInput.value) || 0;
        const subtotal = cantidad * precio;
        subtotalSpan.textContent = subtotal.toFixed(2);
    }

    // Calcular subtotal inicial si hay valores
    if (cantidadInput && precioInput && subtotalSpan) {
        calcularSubtotal();
    }
});
