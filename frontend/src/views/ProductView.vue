<template>
  <div class="product-view">
    <!-- Notificación de producto agregado -->
    <transition name="notification">
      <div v-if="showNotification" class="notification-toast">
        <svg class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M20 6L9 17l-5-5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div class="notification-content">
          <strong>Producto agregado</strong>
          <span>{{ selectedStoreName }}</span>
        </div>
      </div>
    </transition>

    <router-link to="/search" class="back-link">
      <svg class="back-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M19 12H5M12 19l-7-7 7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Volver a búsqueda
    </router-link>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Cargando producto...</p>
    </div>

    <div v-else-if="product" class="product-container">
      <div class="product-image-section">
        <div class="product-image">
          <img :src="product.image_url || '/placeholder.png'" :alt="product.name">
        </div>
      </div>

      <div class="product-details">
        <h1>{{ product.name }}</h1>
        
        <div class="product-meta">
          <div class="meta-item">
            <span><strong>Marca:</strong> {{ product.brand_name }}</span>
          </div>
          
          <div class="meta-item">
            <span><strong>Categoría:</strong> {{ product.category_name }}</span>
          </div>
        </div>

        <div class="prices-section">
          <h2>Selecciona una tienda</h2>
          <p class="prices-subtitle">Comparamos precios para que ahorres más</p>
          
          <div class="prices-grid">
            <div 
              v-for="price in sortedPrices" 
              :key="price.store_id"
              class="price-card"
              :class="{ 
                'best-price': isBestPrice(price),
                'unavailable': !price.is_available,
                'selected': selectedPrice && selectedPrice.store_id === price.store_id
              }"
              @click="selectPrice(price)"
            >
              <div class="price-card-header">
                <h3>{{ price.store_name }}</h3>
                <span v-if="isBestPrice(price)" class="best-badge">
                  <svg class="star-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                  Mejor precio
                </span>
              </div>
              
              <div class="price-card-body">
                <div v-if="price.is_available" class="price-amount">
                  S/ {{ formatPrice(price.price) }}
                </div>
                <div v-else class="not-available-badge">
                  <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <path d="M12 8v4M12 16h.01" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                  No disponible
                </div>
                
                <a 
                  v-if="price.url && price.is_available" 
                  :href="price.url" 
                  target="_blank" 
                  class="store-link"
                  @click.stop
                >
                  Ver en tienda
                  <svg class="external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </a>
              </div>
              
              <div v-if="price.is_available" class="select-indicator">
                <svg v-if="selectedPrice && selectedPrice.store_id === price.store_id" class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M20 6L9 17l-5-5" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span v-else>Seleccionar</span>
              </div>
            </div>
          </div>
        </div>

        <div class="action-section">
          <button 
            @click="addToCart" 
            class="btn-add-cart"
            :disabled="!selectedPrice"
          >
            <svg class="cart-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="9" cy="21" r="1" fill="currentColor"/>
              <circle cx="20" cy="21" r="1" fill="currentColor"/>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span v-if="selectedPrice">
              Agregar de {{ selectedPrice.store_name }} - S/ {{ formatPrice(selectedPrice.price) }}
            </span>
            <span v-else>
              Selecciona una tienda primero
            </span>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="not-found">
      <svg class="not-found-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <circle cx="12" cy="12" r="10" stroke-width="2"/>
        <path d="M12 8v4M12 16h.01" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <h3>Producto no encontrado</h3>
      <router-link to="/search" class="btn-back">Volver a búsqueda</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '@/store/modules/cart'
import productService from '@/services/productService'

const route = useRoute()
const cartStore = useCartStore()

const product = ref(null)
const loading = ref(true)
const selectedPrice = ref(null)
const showNotification = ref(false)
const selectedStoreName = ref('')

const sortedPrices = computed(() => {
  if (!product.value) return []
  return [...product.value.prices].sort((a, b) => {
    if (a.is_available && !b.is_available) return -1
    if (!a.is_available && b.is_available) return 1
    return parseFloat(a.price) - parseFloat(b.price)
  })
})

const isBestPrice = (price) => {
  if (!price.is_available || !product.value) return false
  const availablePrices = product.value.prices.filter(p => p.is_available)
  if (availablePrices.length === 0) return false
  const minPrice = Math.min(...availablePrices.map(p => parseFloat(p.price)))
  return parseFloat(price.price) === minPrice
}

const formatPrice = (price) => {
  return parseFloat(price).toFixed(2)
}

const selectPrice = (price) => {
  if (price.is_available) {
    selectedPrice.value = price
  }
}

const addToCart = () => {
  if (!selectedPrice.value || !product.value) return
  
  cartStore.addItem({
    ...product.value,
    selected_store_id: selectedPrice.value.store_id,
    selected_store_name: selectedPrice.value.store_name,
    selected_price: selectedPrice.value.price,
    selected_url: selectedPrice.value.url
  })
  
  selectedStoreName.value = selectedPrice.value.store_name
  showNotification.value = true
  
  setTimeout(() => {
    showNotification.value = false
  }, 3000)
}

onMounted(async () => {
  try {
    const response = await productService.getProduct(route.params.id)
    product.value = response.data
    
    // Pre-seleccionar el mejor precio disponible
    const availablePrices = product.value.prices.filter(p => p.is_available)
    if (availablePrices.length > 0) {
      const bestPrice = availablePrices.reduce((min, p) => 
        parseFloat(p.price) < parseFloat(min.price) ? p : min
      )
      selectedPrice.value = bestPrice
    }
  } catch (error) {
    console.error('Error cargando producto:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.product-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  position: relative;
}

/* Notificación Toast */
.notification-toast {
  position: fixed;
  top: 80px;
  right: 20px;
  background: #2c974b;
  color: white;
  padding: 16px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(44, 151, 75, 0.4);
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1000;
  min-width: 280px;
}

.notification-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.notification-content strong {
  font-size: 14px;
}

.notification-content span {
  font-size: 12px;
  opacity: 0.9;
}

.check-icon {
  width: 24px;
  height: 24px;
  stroke-width: 2;
  flex-shrink: 0;
}

.notification-enter-active {
  animation: slideInRight 0.3s ease-out;
}

.notification-leave-active {
  animation: slideOutRight 0.3s ease-in;
}

@keyframes slideInRight {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOutRight {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(400px);
    opacity: 0;
  }
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 20px;
  color: #2c974b;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
}

.back-link:hover {
  gap: 10px;
}

.back-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
}

.loading {
  text-align: center;
  padding: 80px 20px;
  color: #666;
}

.spinner {
  margin: 0 auto 20px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #2c974b;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.product-container {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 40px;
  margin-top: 20px;
}

.product-image-section {
  position: sticky;
  top: 100px;
  height: fit-content;
}

.product-image {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 40px;
  border: 1px solid #e0e0e0;
}

.product-image img {
  width: 100%;
  height: 400px;
  object-fit: contain;
}

.product-details h1 {
  margin: 0 0 20px;
  font-size: 28px;
  color: #333;
}

.product-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 30px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #666;
  font-size: 15px;
}

.meta-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
  color: #2c974b;
}

.prices-section {
  margin: 30px 0;
}

.prices-section h2 {
  margin: 0 0 4px;
  color: #333;
  font-size: 18px; /* Reducido de 22px */
}

.prices-subtitle {
  color: #666;
  margin: 0 0 12px; /* Menos espacio abajo */
  font-size: 13px;
}

.prices-grid {
  display: grid;
  gap: 8px; /* Reducido de 12px */
}

.price-card {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 10px 14px; /* Reducido de 16px */
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.price-card:not(.unavailable):hover {
  border-color: #2c974b;
  box-shadow: 0 2px 8px rgba(44, 151, 75, 0.15);
}

.price-card.selected {
  border-color: #2c974b;
  background: #f0fff4;
  box-shadow: 0 2px 12px rgba(44, 151, 75, 0.2);
}

.price-card.best-price:not(.unavailable) {
  border-color: #2c974b;
  background: linear-gradient(135deg, #f0fff4 0%, #e8f5e9 100%);
}

.price-card.unavailable {
  opacity: 0.5;
  cursor: not-allowed;
}

.price-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px; /* Reducido de 12px */
}

.price-card-header h3 {
  margin: 0;
  font-size: 15px; /* Reducido de 18px */
  color: #333;
}

.best-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #2c974b;
  color: white;
  padding: 2px 8px; /* Padding reducido */
  border-radius: 12px;
  font-size: 11px; /* Letra más pequeña */
  font-weight: 600;
}

.star-icon {
  width: 14px;
  height: 14px;
}

.price-card-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-amount {
  font-size: 20px; /* Reducido de 32px a 20px */
  font-weight: 700;
  color: #2c974b;
}

.not-available-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #999;
  font-size: 14px;
}

.alert-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
}

.store-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #2c974b;
  text-decoration: none;
  font-size: 12px; /* Reducido */
  font-weight: 500;
  padding: 4px 10px; /* Reducido */
  border: 1px solid #2c974b;
  border-radius: 6px;
  transition: all 0.2s;
}

.store-link:hover {
  background: #2c974b;
  color: white;
}

.external-icon {
  width: 14px;
  height: 14px;
  stroke-width: 2;
}

.select-indicator {
  margin-top: 8px; /* Reducido de 12px */
  padding-top: 8px; /* Reducido de 12px */
  border-top: 1px solid #e0e0e0;
  text-align: center;
  font-size: 12px;
  color: #2c974b;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.select-indicator .check-icon {
  width: 20px;
  height: 20px;
  stroke: #2c974b;
}

.action-section {
  margin-top: 30px;
}

.btn-add-cart {
  width: 100%;
  padding: 16px 24px;
  background: #2c974b;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s;
}

.btn-add-cart:hover:not(:disabled) {
  background: #247a3d;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 151, 75, 0.3);
}

.btn-add-cart:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

.cart-icon {
  width: 22px;
  height: 22px;
  stroke-width: 2;
}

.not-found {
  text-align: center;
  padding: 80px 20px;
}

.not-found-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  color: #999;
  stroke-width: 1.5;
}

.not-found h3 {
  color: #333;
  margin-bottom: 20px;
}

.btn-back {
  display: inline-block;
  padding: 12px 24px;
  background: #2c974b;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
}

@media (max-width: 968px) {
  .product-container {
    grid-template-columns: 1fr;
  }

  .product-image-section {
    position: static;
  }
}
</style>