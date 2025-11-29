<template>
  <div class="product-card">
    <!-- Imagen del producto -->
    <div class="product-image">
      <img 
        :src="product.image_url || '/placeholder.png'" 
        :alt="product.name"
        @error="handleImageError"
      >
    </div>
    
    <!-- Información del producto -->
    <div class="product-info">
      <h3 class="product-name" :title="product.name">{{ truncateName(product.name) }}</h3>
      <p class="brand">{{ product.brand_name }}</p>
      <p class="category">{{ product.category_name }}</p>
      
      <!-- Precios por tienda -->
      <div class="prices-container">
        <div 
          v-for="price in sortedPrices" 
          :key="price.store_id"
          class="price-row"
          :class="{ 
            'best-price': isBestPrice(price),
            'unavailable': !price.is_available 
          }"
        >
          <div class="store-info">
            <span class="store-name">{{ price.store_name }}</span>
            <span v-if="isBestPrice(price)" class="best-badge">★ Mejor</span>
          </div>
          
          <div class="price-actions">
            <span v-if="price.is_available" class="price">
              S/ {{ formatPrice(price.price) }}
            </span>
            <span v-else class="not-available">
              No disponible
            </span>
            
            <button 
              v-if="price.is_available"
              @click="addToCart(price)"
              class="btn-add-small"
              :title="`Agregar de ${price.store_name}`"
            >
              +
            </button>
          </div>
        </div>
      </div>
      
      <!-- Botón para ver detalles -->
      <button @click="viewDetails" class="btn-details">
        Ver Detalles
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/store/modules/cart'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const cartStore = useCartStore()

// Ordenar precios de menor a mayor (solo disponibles primero)
const sortedPrices = computed(() => {
  return [...props.product.prices].sort((a, b) => {
    // Priorizar disponibles
    if (a.is_available && !b.is_available) return -1
    if (!a.is_available && b.is_available) return 1
    // Luego por precio
    return parseFloat(a.price) - parseFloat(b.price)
  })
})

// Identificar el mejor precio
const isBestPrice = (price) => {
  if (!price.is_available) return false
  const availablePrices = props.product.prices.filter(p => p.is_available)
  if (availablePrices.length === 0) return false
  
  const minPrice = Math.min(...availablePrices.map(p => parseFloat(p.price)))
  return parseFloat(price.price) === minPrice
}

const formatPrice = (price) => {
  return parseFloat(price).toFixed(2)
}

const truncateName = (name) => {
  return name.length > 60 ? name.substring(0, 60) + '...' : name
}

const handleImageError = (e) => {
  e.target.src = '/placeholder.png'
}

const viewDetails = () => {
  router.push({ name: 'product', params: { id: props.product.id } })
}

const addToCart = (price) => {
  cartStore.addItem({
    ...props.product,
    selected_store_id: price.store_id,
    selected_store_name: price.store_name,
    selected_price: price.price,
    selected_url: price.url
  })
}
</script>

<style scoped>
.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.product-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.product-image {
  background: #f9f9f9;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 180px;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.product-info {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.product-name {
  font-size: 15px;
  margin: 0;
  font-weight: 600;
  color: #333;
  line-height: 1.3;
  min-height: 40px;
}

.brand {
  font-size: 13px;
  color: #2c974b;
  font-weight: 500;
  margin: 0;
}

.category {
  font-size: 12px;
  color: #999;
  margin: 0;
}

.prices-container {
  margin: 12px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background: #f9f9f9;
  border-radius: 4px;
  border: 1px solid #f0f0f0;
  transition: all 0.2s;
}

.price-row.best-price {
  background: #e8f5e9;
  border-color: #2c974b;
}

.price-row.unavailable {
  opacity: 0.5;
}

.store-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.store-name {
  font-size: 12px;
  font-weight: 500;
  color: #666;
}

.best-badge {
  font-size: 10px;
  color: #2c974b;
  font-weight: bold;
}

.price-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price {
  font-size: 16px;
  font-weight: bold;
  color: #2c974b;
}

.not-available {
  font-size: 11px;
  color: #999;
}

.btn-add-small {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: #2c974b;
  color: white;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-add-small:hover {
  background: #247a3d;
  transform: scale(1.1);
}

.btn-details {
  width: 100%;
  padding: 10px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: #666;
  transition: all 0.2s;
  margin-top: auto;
}

.btn-details:hover {
  background: #e0e0e0;
}
</style>