<template>
  <div class="cart-view">
    <div class="cart-header">
      <h1>🛒 Carrito de Compras</h1>
      <p v-if="cartStore.totalItems > 0" class="item-count">
        {{ cartStore.totalItems }} {{ cartStore.totalItems === 1 ? 'producto' : 'productos' }}
      </p>
    </div>

    <!-- Carrito vacío -->
    <div v-if="cartStore.items.length === 0" class="empty-cart">
      <div class="empty-icon">🛒</div>
      <h3>Tu carrito está vacío</h3>
      <p>Agrega productos para comparar precios</p>
      <router-link to="/search" class="btn-continue">Buscar Productos</router-link>
    </div>

    <!-- Carrito con items -->
    <div v-else class="cart-container">
      <!-- Lista de productos agrupados por tienda -->
      <div class="cart-items-section">
        <div class="section-header">
          <h2>Productos por Tienda</h2>
          <button @click="clearCart" class="btn-clear-all">Limpiar Todo</button>
        </div>

        <!-- Agrupar por tienda -->
        <div 
          v-for="storeGroup in cartStore.itemsByStore" 
          :key="storeGroup.store_id"
          class="store-group"
        >
          <div class="store-group-header">
            <h3>{{ storeGroup.store_name }}</h3>
            <span class="store-total">
              S/ {{ formatPrice(storeGroup.total) }}
            </span>
          </div>

          <div class="store-items">
            <div 
              v-for="item in storeGroup.items" 
              :key="`${item.product_id}-${item.selected_store_id}`"
              class="cart-item"
            >
              <img 
                :src="item.product.image_url || '/placeholder.png'" 
                :alt="item.product.name"
                class="item-image"
              />
              
              <div class="item-details">
                <h4>{{ item.product.name }}</h4>
                <p class="brand">{{ item.product.brand_name }}</p>
                <p class="price-unit">S/ {{ formatPrice(item.selected_price) }} c/u</p>
              </div>

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

              <div class="item-total">
                <span class="subtotal-label">Subtotal:</span>
                <span class="subtotal-price">
                  S/ {{ formatPrice(item.selected_price * item.quantity) }}
                </span>
              </div>

              <button 
                @click="removeItem(item)" 
                class="btn-remove"
                title="Eliminar"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumen y totales -->
      <div class="summary-section">
        <div class="summary-card">
          <h2>Resumen de Compra</h2>
          
          <!-- Totales por tienda -->
          <div class="totals-list">
            <div 
              v-for="(total, index) in sortedTotals" 
              :key="total.store_id"
              class="total-row"
              :class="{ 'best-price': index === 0 }"
            >
              <div class="total-header">
                <span class="store-name">{{ total.store_name }}</span>
                <span v-if="index === 0" class="best-badge">★ Mejor Precio</span>
              </div>
              <div class="total-details">
                <span class="items-count">
                  {{ total.items_count }} {{ total.items_count === 1 ? 'producto' : 'productos' }}
                </span>
                <span class="total-price">S/ {{ formatPrice(total.total) }}</span>
              </div>
            </div>
          </div>

          <!-- Ahorro potencial -->
          <div v-if="potentialSavings > 0" class="savings-info">
            <div class="savings-badge">
              💰 Ahorro potencial
            </div>
            <p class="savings-amount">
              S/ {{ formatPrice(potentialSavings) }}
            </p>
            <p class="savings-text">
              comprando en {{ sortedTotals[0].store_name }}
            </p>
          </div>

          <!-- Acciones -->
          <div class="actions">
            <button @click="saveCart" class="btn-save" :disabled="saving">
              {{ saving ? 'Guardando...' : '💾 Guardar Carrito' }}
            </button>
            
            <button @click="goToBestStore" class="btn-checkout">
              Comprar en {{ sortedTotals[0].store_name }}
            </button>
          </div>

          <!-- Mensaje de guardado -->
          <div v-if="saveMessage" class="save-message" :class="saveMessage.type">
            {{ saveMessage.text }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCartStore } from '@/store/modules/cart'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const router = useRouter()

const saving = ref(false)
const saveMessage = ref(null)

// Ordenar totales de menor a mayor
const sortedTotals = computed(() => {
  return [...cartStore.totals].sort((a, b) => a.total - b.total)
})

// Calcular ahorro potencial
const potentialSavings = computed(() => {
  if (sortedTotals.value.length < 2) return 0
  const best = sortedTotals.value[0].total
  const worst = sortedTotals.value[sortedTotals.value.length - 1].total
  return worst - best
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

const saveCart = async () => {
  saving.value = true
  saveMessage.value = null
  
  const result = await cartStore.saveCart()
  
  if (result.success) {
    saveMessage.value = {
      type: 'success',
      text: `✓ ${result.message} (ID: ${result.id})`
    }
  } else {
    saveMessage.value = {
      type: 'error',
      text: `✗ ${result.message}`
    }
  }
  
  saving.value = false
  
  // Limpiar mensaje después de 5 segundos
  setTimeout(() => {
    saveMessage.value = null
  }, 5000)
}

const goToBestStore = () => {
  if (sortedTotals.value.length > 0) {
    const bestStore = sortedTotals.value[0]
    alert(
      `Mejor precio en ${bestStore.store_name}\n` +
      `Total: S/ ${formatPrice(bestStore.total)}\n` +
      `Productos: ${bestStore.items_count}`
    )
  }
}
</script>

<style scoped>
.cart-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.cart-header {
  margin-bottom: 30px;
}

.cart-header h1 {
  margin: 0 0 8px;
  color: #333;
}

.item-count {
  color: #666;
  font-size: 15px;
  margin: 0;
}

/* Carrito vacío */
.empty-cart {
  text-align: center;
  padding: 100px 20px;
  color: #666;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-cart h3 {
  color: #333;
  margin: 0 0 10px;
}

.btn-continue {
  display: inline-block;
  margin-top: 24px;
  padding: 14px 32px;
  background: #2c974b;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-continue:hover {
  background: #247a3d;
  transform: translateY(-2px);
}

/* Carrito con items */
.cart-container {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 30px;
  align-items: start;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  color: #333;
}

.btn-clear-all {
  padding: 8px 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.2s;
}

.btn-clear-all:hover {
  background: #e0e0e0;
}

/* Grupos por tienda */
.store-group {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.store-group-header {
  background: #f9f9f9;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
}

.store-group-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.store-total {
  font-size: 20px;
  font-weight: bold;
  color: #2c974b;
}

.store-items {
  padding: 10px;
}

/* Items del carrito */
.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto auto;
  gap: 16px;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.cart-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: contain;
  background: #f9f9f9;
  border-radius: 6px;
}

.item-details h4 {
  margin: 0 0 6px;
  font-size: 15px;
  color: #333;
}

.brand {
  margin: 0 0 4px;
  font-size: 13px;
  color: #2c974b;
}

.price-unit {
  margin: 0;
  font-size: 13px;
  color: #666;
}

/* Control de cantidad */
.quantity-control {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #f9f9f9;
  padding: 8px 12px;
  border-radius: 8px;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  color: #666;
  transition: all 0.2s;
}

.qty-btn:hover:not(:disabled) {
  background: #2c974b;
  color: white;
}

.qty-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.quantity {
  font-weight: 600;
  min-width: 20px;
  text-align: center;
}

/* Total del item */
.item-total {
  text-align: right;
}

.subtotal-label {
  display: block;
  font-size: 11px;
  color: #999;
  margin-bottom: 4px;
}

.subtotal-price {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.btn-remove {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  padding: 8px;
  opacity: 0.6;
  transition: all 0.2s;
}

.btn-remove:hover {
  opacity: 1;
  transform: scale(1.1);
}

/* Resumen */
.summary-section {
  position: sticky;
  top: 80px;
}

.summary-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 24px;
}

.summary-card h2 {
  margin: 0 0 20px;
  color: #333;
  font-size: 20px;
}

.totals-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.total-row {
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  border: 2px solid #f0f0f0;
}

.total-row.best-price {
  background: #e8f5e9;
  border-color: #2c974b;
}

.total-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.store-name {
  font-weight: 600;
  color: #333;
}

.best-badge {
  font-size: 12px;
  color: #2c974b;
  font-weight: bold;
}

.total-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.items-count {
  font-size: 13px;
  color: #666;
}

.total-price {
  font-size: 20px;
  font-weight: bold;
  color: #2c974b;
}

/* Ahorro */
.savings-info {
  background: #fff3cd;
  border: 2px solid #ffc107;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
  text-align: center;
}

.savings-badge {
  font-size: 14px;
  font-weight: 600;
  color: #856404;
  margin-bottom: 8px;
}

.savings-amount {
  font-size: 24px;
  font-weight: bold;
  color: #856404;
  margin: 0 0 4px;
}

.savings-text {
  font-size: 13px;
  color: #856404;
  margin: 0;
}

/* Acciones */
.actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-save {
  padding: 12px;
  background: #f0f0f0;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  color: #666;
  transition: all 0.2s;
}

.btn-save:hover:not(:disabled) {
  background: #e0e0e0;
  border-color: #d0d0d0;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-checkout {
  padding: 16px;
  background: #2c974b;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-checkout:hover {
  background: #247a3d;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 151, 75, 0.3);
}

/* Mensaje de guardado */
.save-message {
  margin-top: 12px;
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
  text-align: center;
}

.save-message.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.save-message.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

@media (max-width: 1024px) {
  .cart-container {
    grid-template-columns: 1fr;
  }

  .summary-section {
    position: static;
  }
}

@media (max-width: 768px) {
  .cart-item {
    grid-template-columns: 60px 1fr;
    gap: 12px;
  }

  .quantity-control,
  .item-total,
  .btn-remove {
    grid-column: 2;
  }
}
</style>