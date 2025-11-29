<template>
  <div class="product-card">
    <div class="product-image">
      <img :src="product.image_url || '/placeholder.png'" :alt="product.name">
    </div>
    
    <div class="product-info">
      <h3>{{ product.name }}</h3>
      <p class="brand">{{ product.brand_name }}</p>
      <p class="category">{{ product.category_name }}</p>
      
      <div class="prices">
        <div v-for="price in product.prices" :key="price.store_id" class="price-item">
          <span class="store">{{ price.store_name }}</span>
          <span class="price">S/ {{ formatPrice(price.price) }}</span>
        </div>
      </div>
      
      <div class="actions">
        <button @click="viewDetails" class="btn-details">Ver Detalles</button>
        <button @click="addToCart" class="btn-add">Agregar al Carrito</button>
      </div>
    </div>
  </div>
</template>

<script setup>
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

const formatPrice = (price) => {
  return parseFloat(price).toFixed(2)
}

const viewDetails = () => {
  router.push({ name: 'product', params: { id: props.product.id } })
}

const addToCart = () => {
  cartStore.addItem(props.product)
}
</script>

<style scoped>
.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  transition: box-shadow 0.3s;
}

.product-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.product-image img {
  width: 100%;
  height: 200px;
  object-fit: contain;
}

.product-info h3 {
  font-size: 16px;
  margin: 12px 0 4px;
}

.brand, .category {
  font-size: 14px;
  color: #666;
}

.prices {
  margin: 12px 0;
}

.price-item {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
}

.price {
  font-weight: bold;
  color: #2c974b;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

button {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-details {
  background: #f0f0f0;
}

.btn-add {
  background: #2c974b;
  color: white;
}

.btn-add:hover {
  background: #247a3d;
}
</style>