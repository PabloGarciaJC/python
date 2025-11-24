// Gestión de productos en formularios de compras

let details = [];

// Evento para actualizar el precio cuando se selecciona un producto
document.addEventListener('DOMContentLoaded', function() {
    const productSelect = document.getElementById('productSelect');
    if (productSelect) {
        productSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const price = selectedOption.dataset.price || 0;
            document.getElementById('priceInput').value = price;
        });
    }

    const addProductBtn = document.getElementById('addProductBtn');
    if (addProductBtn) {
        addProductBtn.addEventListener('click', addProduct);
    }

    const purchaseForm = document.getElementById('purchaseForm');
    if (purchaseForm) {
        purchaseForm.addEventListener('submit', function(e) {
            if (details.length === 0) {
                e.preventDefault();
                alert('Debe agregar al menos un producto');
            }
        });
    }
});

function addProduct() {
    const productSelect = document.getElementById('productSelect');
    const productId = productSelect.value;
    const productName = productSelect.options[productSelect.selectedIndex].text;
    const quantity = parseInt(document.getElementById('quantityInput').value);
    const price = parseFloat(document.getElementById('priceInput').value);

    if (!productId || quantity <= 0 || price < 0) {
        alert('Por favor complete todos los campos correctamente');
        return;
    }

    const subtotal = quantity * price;

    details.push({
        producto_id: productId,
        producto_nombre: productName,
        cantidad: quantity,
        precio_unitario: price,
        subtotal: subtotal
    });

    updateTable();

    // Reset
    productSelect.value = '';
    document.getElementById('quantityInput').value = 1;
    document.getElementById('priceInput').value = 0;
}

function updateTable() {
    const tbody = document.getElementById('productsTableBody');
    const emptyRow = document.getElementById('emptyRow');

    if (details.length === 0) {
        emptyRow.style.display = '';
        document.getElementById('totalAmount').textContent = 'S/ 0.00';
        document.getElementById('totalInput').value = 0;
        return;
    }

    emptyRow.style.display = 'none';
    tbody.innerHTML = '';

    let total = 0;
    details.forEach((detail, index) => {
        total += detail.subtotal;
        const row = `
            <tr>
                <td>${detail.producto_nombre}</td>
                <td>${detail.cantidad}</td>
                <td>S/ ${detail.precio_unitario.toFixed(2)}</td>
                <td>S/ ${detail.subtotal.toFixed(2)}</td>
                <td>
                    <button type="button" class="btn btn-sm btn-danger" onclick="removeProduct(${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });

    document.getElementById('totalAmount').textContent = `S/ ${total.toFixed(2)}`;
    document.getElementById('totalInput').value = total.toFixed(2);
    document.getElementById('detailsInput').value = JSON.stringify(details);
}

function removeProduct(index) {
    details.splice(index, 1);
    updateTable();
}

// Para el formulario de edición, cargar detalles existentes
function loadExistingDetails(existingDetails) {
    details = existingDetails;
    updateTable();
}
