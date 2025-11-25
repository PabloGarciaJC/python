// Gestión de productos en formularios de ventas y compras

class ProductManager {
    constructor(products, existingProducts = []) {
        this.products = products;
        this.selectedProducts = existingProducts;
    }

    addProduct(productId, quantity) {
        if (!productId || quantity <= 0) {
            alert('Seleccione un producto y cantidad válida');
            return;
        }

        const product = this.products.find(p => p.id === productId);
        if (!product) return;

        const existing = this.selectedProducts.find(p => p.producto_id === productId);
        if (existing) {
            existing.cantidad += quantity;
            existing.subtotal = existing.cantidad * existing.precio_unitario;
        } else {
            this.selectedProducts.push({
                producto_id: productId,
                nombre: product.nombre,
                precio_unitario: product.precio,
                cantidad: quantity,
                subtotal: product.precio * quantity
            });
        }

        this.render();
    }

    removeProduct(index) {
        this.selectedProducts.splice(index, 1);
        this.render();
    }

    render() {
        const tbody = document.getElementById('productsBody');
        const table = document.getElementById('productsTable');

        if (this.selectedProducts.length === 0 && table) {
            table.style.display = 'none';
            return;
        }

        if (table) {
            table.style.display = 'table';
        }

        tbody.innerHTML = this.selectedProducts.map((p, i) => `
            <tr>
                <td>${p.nombre}</td>
                <td>$${p.precio_unitario.toFixed(2)}</td>
                <td>${p.cantidad}</td>
                <td>$${p.subtotal.toFixed(2)}</td>
                <td><button type="button" class="btn btn-danger" onclick="manager.removeProduct(${i})">X</button></td>
            </tr>
        `).join('');

        const total = this.selectedProducts.reduce((sum, p) => sum + p.subtotal, 0);
        document.getElementById('totalAmount').textContent = `$${total.toFixed(2)}`;
    }

    getProducts() {
        return this.selectedProducts;
    }
}

// Instancia global del manager (se inicializará desde la vista)
let manager = null;

// Función para agregar producto (llamada desde el botón)
function addProduct() {
    const select = document.getElementById('productSelect');
    const quantity = parseInt(document.getElementById('quantityInput').value);
    const productId = parseInt(select.value);

    manager.addProduct(productId, quantity);

    select.value = '';
    document.getElementById('quantityInput').value = 1;
}

// Inicialización del formulario
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('saleForm') || document.getElementById('purchaseForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            if (manager.selectedProducts.length === 0) {
                e.preventDefault();
                alert('Debe agregar al menos un producto');
                return;
            }
            document.getElementById('details').value = JSON.stringify(manager.selectedProducts);
        });

        // Si hay productos existentes, renderizarlos
        if (manager && manager.selectedProducts.length > 0) {
            manager.render();
        }
    }
});
