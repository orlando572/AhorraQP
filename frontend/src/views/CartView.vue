<template>
  <div class="cart-view">
    <div class="cart-header">
      <h1>🛒 Carrito de Compras</h1>
      <p v-if="cartStore.totalItems > 0" class="item-count">
        {{ cartStore.totalItems }} {{ cartStore.totalItems === 1 ? 'producto' : 'productos' }}
      </p>
    </div>

    <div v-if="cartStore.items.length === 0" class="empty-cart">
      <div class="empty-icon">🛒</div>
      <h3>Tu carrito está vacío</h3>
      <p>Agrega productos para comparar precios</p>
      <router-link to="/search" class="btn-continue">Buscar Productos</router-link>
    </div>

    <div v-else class="cart-container">
      
      <div class="cart-items-section">
        <div class="section-header">
          <h2>Tus Productos</h2>
          <button @click="clearCart" class="btn-clear-all">Limpiar Todo</button>
        </div>

        <div class="items-list">
          <div 
            v-for="item in cartStore.items" 
            :key="`${item.product_id}-${item.selected_store_id}`"
            class="cart-item-row"
          >
            <div class="item-col image-col">
              <img 
                :src="item.product.image_url || '/placeholder.png'" 
                :alt="item.product.name"
              />
            </div>
            
            <div class="item-col info-col">
              <h4>{{ item.product.name }}</h4>
              <span class="brand">{{ item.product.brand_name }}</span>
              <div class="store-badge">
                Vendido por: <strong>{{ item.selected_store_name }}</strong>
              </div>
            </div>

            <div class="item-col price-col">
              <div class="price-unit">S/ {{ formatPrice(item.selected_price) }}</div>
              <a 
                v-if="item.selected_url" 
                :href="item.selected_url" 
                target="_blank" 
                class="store-link"
              >
                Ver en Tienda ↗
              </a>
            </div>

            <div class="item-col qty-col">
              <div class="quantity-control">
                <button 
                  @click="decreaseQuantity(item)" 
                  class="qty-btn"
                  :disabled="item.quantity <= 1"
                >
                  −
                </button>
                <span class="quantity">{{ item.quantity }}</span>
                <button @click="increaseQuantity(item)" class="qty-btn">
                  +
                </button>
              </div>
            </div>

            <div class="item-col subtotal-col">
              <span class="subtotal-label">Total:</span>
              <span class="subtotal-amount">
                S/ {{ formatPrice(item.selected_price * item.quantity) }}
              </span>
            </div>

            <button 
              @click="removeItem(item)" 
              class="btn-remove"
              title="Eliminar"
            >
              ✕
            </button>
          </div>
        </div>
      </div>

      <div class="summary-section">
        <div class="summary-card">
          <h2>Resumen de Compra</h2>
          
          <div class="summary-row">
            <span>Subtotal Productos ({{ cartStore.totalItems }})</span>
            <span>S/ {{ formatPrice(cartStore.cartTotal) }}</span>
          </div>

          <div class="divider"></div>

          <div class="summary-row total-row">
            <span>Total Estimado</span>
            <span class="total-amount">S/ {{ formatPrice(cartStore.cartTotal) }}</span>
          </div>

          <div v-if="cartStore.totalSavings > 0" class="savings-container">
            <div class="savings-card">
              <div class="savings-icon">💰</div>
              <div class="savings-content">
                <span class="savings-label">¡Estás ahorrando!</span>
                <span class="savings-value">S/ {{ formatPrice(cartStore.totalSavings) }}</span>
                <p class="savings-detail">
                  Comparado con la alternativa más cara de cada producto.
                </p>
              </div>
            </div>
          </div>
          
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/store/modules/cart'

const cartStore = useCartStore()

const formatPrice = (price) => {
  return parseFloat(price).toFixed(2)
}

const increaseQuantity = (item) => {
  cartStore.updateQuantity(
    item.product_id, 
    item.selected_store_id, 
    item.quantity + 1
  )
}

const decreaseQuantity = (item) => {
  if (item.quantity > 1) {
    cartStore.updateQuantity(
      item.product_id, 
      item.selected_store_id, 
      item.quantity - 1
    )
  }
}

const removeItem = (item) => {
  if (confirm('¿Eliminar este producto del carrito?')) {
    cartStore.removeItem(item.product_id, item.selected_store_id)
  }
}

const clearCart = () => {
  if (confirm('¿Estás seguro de que quieres vaciar todo el carrito?')) {
    cartStore.clearCart()
  }
}
</script>

<style scoped>
.cart-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.cart-header h1 {
  margin-bottom: 5px;
  color: #333;
}

.cart-container {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 30px;
  align-items: start;
  margin-top: 20px;
}

/* Items List Styles */
.cart-items-section {
  background: white;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  overflow: hidden;
}

.section-header {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

.items-list {
  display: flex;
  flex-direction: column;
}

.cart-item-row {
  display: grid;
  grid-template-columns: 80px 2fr 1fr 120px 100px 40px;
  gap: 15px;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  align-items: center;
}

.cart-item-row:last-child {
  border-bottom: none;
}

.item-col {
  display: flex;
  flex-direction: column;
}

.image-col img {
  width: 80px;
  height: 80px;
  object-fit: contain;
  border-radius: 8px;
  border: 1px solid #eee;
}

.info-col h4 {
  margin: 0 0 4px 0;
  color: #333;
  font-size: 1rem;
}

.brand {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 4px;
}

.store-badge {
  font-size: 0.8rem;
  color: #555;
  background: #f5f5f5;
  padding: 2px 8px;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
}

.price-unit {
  font-weight: 600;
  color: #333;
}

.store-link {
  font-size: 0.8rem;
  color: #2c974b;
  text-decoration: none;
  margin-top: 4px;
}

.store-link:hover {
  text-decoration: underline;
}

.qty-col .quantity-control {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
}

.qty-btn {
  background: #f9f9f9;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.quantity {
  padding: 0 10px;
  font-weight: 600;
  font-size: 0.9rem;
}

.subtotal-label {
  font-size: 0.75rem;
  color: #888;
}

.subtotal-amount {
  font-weight: 700;
  color: #2c974b;
  font-size: 1.1rem;
}

.btn-remove {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 1.2rem;
  transition: color 0.2s;
}

.btn-remove:hover {
  color: #d32f2f;
}

/* Summary Styles */
.summary-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  position: sticky;
  top: 20px;
}

.summary-card h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.25rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  color: #555;
}

.total-row {
  margin-top: 15px;
  font-weight: bold;
  color: #333;
  font-size: 1.2rem;
}

.total-amount {
  color: #2c974b;
}

.divider {
  height: 1px;
  background: #eee;
  margin: 15px 0;
}

/* Savings Styles */
.savings-container {
  margin-top: 20px;
}

.savings-card {
  background: #f0fff4;
  border: 1px solid #c6f6d5;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  gap: 15px;
}

.savings-icon {
  font-size: 1.5rem;
}

.savings-content {
  display: flex;
  flex-direction: column;
}

.savings-label {
  font-size: 0.9rem;
  color: #276749;
  font-weight: 600;
}

.savings-value {
  font-size: 1.4rem;
  font-weight: 800;
  color: #2f855a;
  margin: 4px 0;
}

.savings-detail {
  font-size: 0.75rem;
  color: #48bb78;
  margin: 0;
  line-height: 1.2;
}

/* Responsive */
@media (max-width: 1024px) {
  .cart-container {
    grid-template-columns: 1fr;
  }
  
  .cart-item-row {
    grid-template-columns: 80px 1fr auto;
    grid-template-areas: 
      "img info info"
      "img price qty"
      "img subtotal remove";
  }

  .image-col { grid-area: img; }
  .info-col { grid-area: info; }
  .price-col { grid-area: price; }
  .qty-col { grid-area: qty; }
  .subtotal-col { grid-area: subtotal; }
  .btn-remove { grid-area: remove; justify-self: end; }
}
</style>