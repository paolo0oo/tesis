

function addToCart(productId) {
    fetch('/add-to-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}' // Asegúrate de que el token esté disponible
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartSidebar(data.cart);
            openCart();
        } else {
            alert('No se pudo agregar el producto al carrito.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function openCart() {
    document.getElementById('cartSidebar').classList.add('open');
}

function closeCart() {
    document.getElementById('cartSidebar').classList.remove('open');
}

function updateCartSidebar(cart) {
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');

    cartItems.innerHTML = ''; // Limpiar los elementos actuales
    let total = 0;

    for (let item of cart) {
        cartItems.innerHTML += `
            <div class="cart-item">
                <p>${item.nombre_prod} - $${item.Precio} x ${item.cantidad}</p>
            </div>
        `;
        total += item.Precio * item.cantidad;
    }

    cartTotal.textContent = total.toFixed(2);
}

function updateCartSidebar(cart) {
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');

    cartItems.innerHTML = ''; // Limpiar los elementos actuales
    let total = 0;

    for (let item of cart) {
        cartItems.innerHTML += `
            <div class="cart-item">
                <p>${item.nombre_prod} - $${item.Precio} x ${item.cantidad}</p>
                <div class="item-actions">
                    <button onclick="updateQuantity('${item.ID_prod}', -1)" class="btn btn-sm btn-secondary">-</button>
                    <button onclick="updateQuantity('${item.ID_prod}', 1)" class="btn btn-sm btn-secondary">+</button>
                    <button onclick="removeFromCart('${item.ID_prod}')" class="btn btn-sm btn-danger">Eliminar</button>
                </div>
            </div>
        `;
        total += item.Precio * item.cantidad;
    }

    cartTotal.textContent = total.toFixed(2);
}

function updateQuantity(productId, change) {
    fetch('/update-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ product_id: productId, change: change })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartSidebar(data.cart);
        } else {
            alert(data.message || 'Error al actualizar la cantidad.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function removeFromCart(productId) {
    fetch('/remove-from-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartSidebar(data.cart);
        } else {
            alert(data.message || 'Error al eliminar el producto.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function goToCheckout() {
    window.location.href = '/carrito/';
}




// Función para filtrar productos
const searchInput = document.getElementById('searchInput');
const productCards = document.querySelectorAll('.product-card');
const sugerenciasContainer = document.getElementById('sugerencias');

// Función para buscar productos y mostrar sugerencias
searchInput.addEventListener('input', function () {
  const searchTerm = searchInput.value.toLowerCase();
  sugerenciasContainer.innerHTML = ''; // Limpiar sugerencias anteriores
  let resultadosEncontrados = false;

  if (searchTerm !== "") {
    productCards.forEach((card) => {
      const productName = card.querySelector('.product-title').textContent.toLowerCase();

      // Si el nombre del producto contiene el término de búsqueda, se muestra como sugerencia
      if (productName.includes(searchTerm)) {
        const sugerenciaDiv = document.createElement('div');
        sugerenciaDiv.textContent = card.querySelector('.product-title').textContent;
        sugerenciasContainer.appendChild(sugerenciaDiv);
        resultadosEncontrados = true;

        // Evento para seleccionar una sugerencia y mostrar solo el producto relacionado
        sugerenciaDiv.addEventListener('click', () => {
          searchInput.value = sugerenciaDiv.textContent;
          sugerenciasContainer.innerHTML = ''; // Limpiar sugerencias
          mostrarProductoCoincidente(sugerenciaDiv.textContent); // Mostrar el producto
        });
      }
    });
  }

  if (!resultadosEncontrados && searchTerm !== "") {
    const noResults = document.createElement('div');
    noResults.textContent = 'No se encontraron resultados.';
    sugerenciasContainer.appendChild(noResults);
  }
});




