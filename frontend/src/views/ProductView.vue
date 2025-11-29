<template>
  <div class="product-view">
    <router-link to="/search" class="back-link">← Volver</router-link>

    <div v-if="loading" class="loading">
      <p>Cargando producto...</p>
    </div>

    <div v-else-if="product" class="product-container">
      <div class="product-image">
        <img :src="product.image_url || '/placeholder.png'" :alt="product.name">
      </div>

      <div class="product-details">
        <h1>{{ product.name }}</h1>
        <p class="brand">Marca: {{ product.brand_name }}</p>
        <p class="category">Categoría: {{ product.category_name }}</p>

        <div class="prices-section">
          <h2>Precios en Tiendas</h2>
          <div class="prices-table">
            <div v-for="price in product.prices" :key="price.store_id" class="price-row">
              <span class="store-name">{{ price.store_name }}</span>
              <span class="price">S/ {{ formatPrice(price.price) }}</span>
              <span class="availability" :class="{ available: price.is_available, unavailable: !price.is_available }">
                {{ price.is_available ? 'Disponible' : 'No disponible' }}
              </span>
              <a v-if="price.url && price.is_available" :href="price.url" target="_blank" class="btn-visit">
                Ver en tienda
              </a>
            </div>
          </div>
        </div>

        <div class="action-buttons">
          <button @click="addToCart" class="btn-add">Agregar al Carrito</button>
        </div>
      </div>
    </div>

    <div v-else class="not-found">
      <p>Producto no encontrado</p>
      <router-link to="/search">Volver a búsqueda</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '@/store/modules/cart'
import productService from '@/services/productService'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()

const product = ref(null)
const loading = ref(true)

const formatPrice = (price) => {
  return parseFloat(price).toFixed(2)
}

const addToCart = () => {
  if (product.value) {
    cartStore.addItem(product.value)
    alert('Producto agregado al carrito')
  }
}

onMounted(async () => {
  try {
    const response = await productService.getProduct(route.params.id)
    product.value = response.data
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
}

.back-link {
  display: inline-block;
  margin-bottom: 20px;
  color: #2c974b;
  text-decoration: none;
  font-weight: bold;
}

.product-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.product-image {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
}

.product-image img {
  width: 100%;
  height: 400px;
  object-fit: contain;
}

.product-details h1 {
  margin: 0 0 16px;
}

.brand, .category {
  color: #666;
  font-size: 16px;
}

.prices-section {
  margin: 30px 0;
}

.prices-table {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.price-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
  gap: 10px;
}

.price-row:last-child {
  border-bottom: none;
}

.store-name {
  font-weight: bold;
}

.price {
  font-size: 18px;
  color: #2c974b;
  font-weight: bold;
}

.availability {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}

.available {
  background: #d4edda;
  color: #155724;
}

.unavailable {
  background: #f8d7da;
  color: #721c24;
}

.btn-visit {
  background: #007bff;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 12px;
}

.action-buttons {
  margin-top: 30px;
}

.btn-add {
  padding: 12px 24px;
  background: #2c974b;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  width: 100%;
}

.btn-add:hover {
  background: #247a3d;
}

@media (max-width: 768px) {
  .product-container {
    grid-template-columns: 1fr;
  }

  .price-row {
    grid-template-columns: 1fr;
  }
}
</style>