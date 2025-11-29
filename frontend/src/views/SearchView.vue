<template>
  <div class="search-view">
    <div class="search-header">
      <h1>Buscar Productos</h1>
      
      <div class="search-box">
        <input
          v-model="searchQuery"
          @input="onSearch"
          type="text"
          placeholder="Busca arroz, leche, aceite..."
          class="search-input"
        >
      </div>
    </div>

    <div v-if="loading" class="loading">
      <p>Buscando productos...</p>
    </div>

    <div v-else-if="products.length > 0" class="results">
      <p class="results-count">{{ products.length }} productos encontrados</p>
      
      <div class="products-grid">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
        />
      </div>
    </div>

    <div v-else-if="searchQuery" class="no-results">
      <p>No se encontraron productos para "{{ searchQuery }}"</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ProductCard from '@/components/product/ProductCard.vue'
import productService from '@/services/productService'

const searchQuery = ref('')
const products = ref([])
const loading = ref(false)

let searchTimeout = null

const onSearch = () => {
  clearTimeout(searchTimeout)
  
  if (searchQuery.value.length < 2) {
    products.value = []
    return
  }

  searchTimeout = setTimeout(async () => {
    loading.value = true
    try {
      const response = await productService.searchProducts(searchQuery.value)
      products.value = response.data
    } catch (error) {
      console.error('Error buscando productos:', error)
    } finally {
      loading.value = false
    }
  }, 300)
}
</script>

<style scoped>
.search-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-header {
  margin-bottom: 30px;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  margin-top: 16px;
}

.search-input:focus {
  outline: none;
  border-color: #2c974b;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.results-count {
  color: #666;
  font-size: 14px;
}

.loading, .no-results {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>