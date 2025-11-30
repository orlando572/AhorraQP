<template>
  <div class="cart-view">
    <!-- Modal de confirmación -->
    <ConfirmModal
      :show="showModal"
      :title="modalConfig.title"
      :message="modalConfig.message"
      :confirmText="modalConfig.confirmText"
      @confirm="modalConfig.onConfirm"
      @close="showModal = false"
    />

    <div class="cart-header">
      <h1>
        <svg class="cart-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="9" cy="21" r="1"/>
          <circle cx="20" cy="21" r="1"/>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Carrito de Compras
      </h1>
      <p v-if="cartStore.totalItems > 0" class="item-count">
        {{ cartStore.totalItems }} {{ cartStore.totalItems === 1 ? 'producto' : 'productos' }}
      </p>
    </div>

    <div v-if="cartStore.items.length === 0" class="empty-cart">
      <div class="empty-illustration">
        <svg class="empty-cart-svg" viewBox="0 0 200 200" fill="none">
          <circle cx="100" cy="100" r="80" fill="#f0f0f0"/>
          <path d="M70 90c0-16.569 13.431-30 30-30s30 13.431 30 30" stroke="#999" stroke-width="3" stroke-linecap="round"/>
          <circle cx="85" cy="90" r="5" fill="#999"/>
          <circle cx="115" cy="90" r="5" fill="#999"/>
          <path d="M60 130h80" stroke="#2c974b" stroke-width="4" stroke-linecap="round"/>
          <path d="M140 130l10 20M60 130l-10 20" stroke="#2c974b" stroke-width="3" stroke-linecap="round"/>
        </svg>
      </div>
      <h3>Tu carrito está vacío</h3>
      <p class="empty-message">Todavía no has agregado productos. <br>¡Comienza a comparar precios y ahorra!</p>
      <router-link to="/search" class="btn-continue">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="11" cy="11" r="8" stroke-width="2"/>
          <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
        </svg>
        Buscar Productos
      </router-link>
    </div>

    <div v-else class="cart-container">
      <div class="cart-items-section">
        <div class="section-header">
          <h2>Tus Productos</h2>
          <button @click="confirmClearCart" class="btn-clear-all">
            <svg class="trash-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polyline points="3 6 5 6 21 6" stroke-width="2" stroke-linecap="round"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Limpiar Todo
          </button>
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
                {{ item.selected_store_name }}
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
                Ver en Tienda
                <svg class="external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </a>
            </div>

            <div class="item-col qty-col">
              <div class="quantity-control">
                <button 
                  @click="decreaseQuantity(item)" 
                  class="qty-btn"
                  :disabled="item.quantity <= 1"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M5 12h14" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
                <span class="quantity">{{ item.quantity }}</span>
                <button @click="increaseQuantity(item)" class="qty-btn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 5v14M5 12h14" stroke-width="2" stroke-linecap="round"/>
                  </svg>
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
              @click="confirmRemoveItem(item)" 
              class="btn-remove"
              title="Eliminar"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M18 6L6 18M6 6l12 12" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div class="summary-section">
        <div class="summary-card">
          <h2>Resumen de Compra</h2>
          
          <div class="summary-row">
            <span>Subtotal ({{ cartStore.totalItems }} productos)</span>
            <span>S/ {{ formatPrice(cartStore.cartTotal) }}</span>
          </div>

          <div class="divider"></div>

          <div class="summary-row total-row">
            <span>Total Estimado</span>
            <span class="total-amount">S/ {{ formatPrice(cartStore.cartTotal) }}</span>
          </div>

          <div v-if="cartStore.totalSavings > 0" class="savings-container">
            <div class="savings-card">
              <div class="savings-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="10" stroke-width="2"/>
                  <path d="M12 6v6l4 2" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              <div class="savings-content">
                <span class="savings-label">¡Estás ahorrando!</span>
                <span class="savings-value">S/ {{ formatPrice(cartStore.totalSavings) }}</span>
                <p class="savings-detail">
                  Comparado con la alternativa más cara de cada producto.
                </p>
              </div>
            </div>
          </div>
          
          <div class="auto-save-notice">
            <svg class="cloud-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" stroke-width="2"/>
              <polyline points="17 21 17 13 7 13 7 21" stroke-width="2"/>
            </svg>
            Tu carrito se guarda automáticamente
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/store/modules/cart'
import ConfirmModal from '@/components/common/ConfirmModal.vue'

const cartStore = useCartStore()
const showModal = ref(false)
const modalConfig = ref({
  title: '',
  message: '',
  confirmText: 'Confirmar',
  onConfirm: () => {}
})

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

const confirmRemoveItem = (item) => {
  modalConfig.value = {
    title: 'Eliminar producto',
    message: `¿Estás seguro de que quieres eliminar "${item.product.name}" del carrito?`,
    confirmText: 'Eliminar',
    onConfirm: () => {
      cartStore.removeItem(item.product_id, item.selected_store_id)
    }
  }
  showModal.value = true
}

const confirmClearCart = () => {
  modalConfig.value = {
    title: 'Vaciar carrito',
    message: '¿Estás seguro de que quieres eliminar todos los productos del carrito? Esta acción no se puede deshacer.',
    confirmText: 'Vaciar',
    onConfirm: () => {
      cartStore.clearCart()
    }
  }
  showModal.value = true
}
</script>

<style scoped>
.cart-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.cart-header {
  margin-bottom: 20px;
}

.cart-header h1 {
  margin-bottom: 5px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 12px;
}

.cart-icon {
  width: 32px;
  height: 32px;
  stroke-width: 1.5;
}

/* Empty Cart Styles */
.empty-cart {
  text-align: center;
  padding: 80px 20px;
  max-width: 500px;
  margin: 0 auto;
}

.empty-illustration {
  margin-bottom: 30px;
}

.empty-cart-svg {
  width: 200px;
  height: 200px;
  margin: 0 auto;
}

.empty-cart h3 {
  font-size: 28px;
  color: #333;
  margin: 0 0 12px;
}

.empty-message {
  color: #666;
  font-size: 16px;
  line-height: 1.6;
  margin: 0 0 32px;
}

.btn-continue {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: #2c974b;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s;
}

.btn-continue:hover {
  background: #247a3d;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 151, 75, 0.3);
}

.search-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
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

.btn-clear-all {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #f0f0f0;
  color: #666;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-clear-all:hover {
  background: #fee;
  color: #d32f2f;
}

.trash-icon {
  width: 16px;
  height: 16px;
  stroke-width: 2;
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
  padding: 4px 8px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  width: fit-content;
}

.store-icon {
  width: 12px;
  height: 12px;
  stroke-width: 2;
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
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.store-link:hover {
  text-decoration: underline;
}

.external-icon {
  width: 12px;
  height: 12px;
  stroke-width: 2;
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
  padding: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.qty-btn:hover:not(:disabled) {
  background: #e0e0e0;
}

.qty-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.qty-btn svg {
  width: 16px;
  height: 16px;
  stroke-width: 2;
}

.quantity {
  padding: 0 12px;
  font-weight: 600;
  font-size: 0.9rem;
  min-width: 30px;
  text-align: center;
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
  padding: 8px;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove svg {
  width: 20px;
  height: 20px;
  stroke-width: 2;
}

.btn-remove:hover {
  background: #fee;
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

.savings-icon svg {
  width: 32px;
  height: 32px;
  stroke: #2c974b;
  stroke-width: 2;
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

/* Auto-save notice */
.auto-save-notice {
  margin-top: 16px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  color: #666;
}

.cloud-icon {
  width: 18px;
  height: 18px;
  stroke: #2c974b;
  stroke-width: 2;
  flex-shrink: 0;
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