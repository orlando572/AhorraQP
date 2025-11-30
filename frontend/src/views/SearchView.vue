<template>
  <div class="search-view">
    <!-- Header de búsqueda -->
    <div class="search-header">
      <h1>
        <svg class="search-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="11" cy="11" r="8" stroke-width="2"/>
          <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
        </svg>
        Buscar Productos
      </h1>
      
      <!-- Filtros -->
      <div class="filters-section">
        <!-- Búsqueda por nombre -->
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="11" cy="11" r="8" stroke-width="2"/>
            <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <input
            v-model="searchQuery"
            @input="onSearch"
            type="text"
            placeholder="Busca arroz, leche, aceite, fideos..."
            class="search-input"
          >
          <button v-if="searchQuery" @click="clearFilters" class="btn-clear">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M18 6L6 18M6 6l12 12" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <!-- Filtro por categoría -->
        <div class="category-filter">
          <label>
            Categoría:
          </label>
          <select v-model="selectedCategory" @change="onCategoryChange" class="category-select">
            <option :value="null">Todas las categorías</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Estado de carga -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Buscando productos...</p>
    </div>

    <!-- Resultados -->
    <div v-else-if="products.length > 0" class="results">
      <div class="results-header">
        <p class="results-count">
          <strong>{{ products.length }}</strong> productos encontrados
          <span v-if="selectedCategory" class="filter-tag">
            en {{ getCategoryName(selectedCategory) }}
          </span>
        </p>
      </div>
      
      <div class="products-grid">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
        />
      </div>
    </div>

    <!-- Sin resultados -->
    <div v-else-if="searchQuery || selectedCategory" class="no-results">
      <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <circle cx="11" cy="11" r="8" stroke-width="2"/>
        <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
        <path d="M8 11h6M11 8v6" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <h3>No se encontraron productos</h3>
      <p v-if="searchQuery">Para la búsqueda: "{{ searchQuery }}"</p>
      <p v-if="selectedCategory">En la categoría: {{ getCategoryName(selectedCategory) }}</p>
      <button @click="clearFilters" class="btn-try-again">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M1 4v6h6M23 20v-6h-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Limpiar filtros
      </button>
    </div>

    <!-- Estado inicial -->
    <div v-else class="initial-state">
      <svg class="welcome-icon" viewBox="0 0 200 200" fill="none">
        <circle cx="100" cy="100" r="80" fill="#f0f0f0"/>
        <circle cx="100" cy="80" r="30" fill="white" stroke="#2c974b" stroke-width="3"/>
        <path d="M100 110 L100 150" stroke="#2c974b" stroke-width="3" stroke-linecap="round"/>
        <path d="M70 130 L100 150 L130 130" stroke="#2c974b" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <circle cx="90" cy="75" r="5" fill="#2c974b"/>
        <circle cx="110" cy="75" r="5" fill="#2c974b"/>
        <path d="M85 90 Q100 100 115 90" stroke="#2c974b" stroke-width="3" stroke-linecap="round" fill="none"/>
      </svg>
      <h3>Encuentra los mejores precios</h3>
      <p>Busca por nombre o selecciona una categoría</p>
      
      <!-- Categorías populares -->
      <div class="popular-categories">
        <h4>Categorías populares:</h4>
        <div class="category-chips">
          <button
            v-for="cat in popularCategories"
            :key="cat.id"
            @click="selectCategory(cat.id)"
            class="category-chip"
          >
            {{ cat.name }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import ProductCard from '@/components/product/ProductCard.vue'
import productService from '@/services/productService'
import categoryService from '@/services/categoryService'

const searchQuery = ref('')
const selectedCategory = ref(null)
const products = ref([])
const categories = ref([])
const loading = ref(false)

let searchTimeout = null

// Categorías populares
const popularCategories = computed(() => {
  return categories.value.filter(cat => 
    ['Arroz', 'Aceite', 'Leche', 'Yogurt', 'Azúcar y Endulzantes'].includes(cat.name)
  )
})

const getCategoryName = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category ? category.name : ''
}

const onSearch = () => {
  clearTimeout(searchTimeout)
  
  if (searchQuery.value.length < 2 && !selectedCategory.value) {
    products.value = []
    return
  }

  searchTimeout = setTimeout(async () => {
    await performSearch()
  }, 300)
}

const onCategoryChange = () => {
  performSearch()
}

const performSearch = async () => {
  loading.value = true
  try {
    const response = await productService.searchProducts(
      searchQuery.value || '',
      selectedCategory.value
    )
    products.value = response.data
  } catch (error) {
    console.error('Error buscando productos:', error)
    products.value = []
  } finally {
    loading.value = false
  }
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  performSearch()
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = null
  products.value = []
}

onMounted(async () => {
  try {
    const response = await categoryService.getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('Error cargando categorías:', error)
  }
})
</script>

<style scoped>
.search-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.search-header {
  margin-bottom: 30px;
}

.search-header h1 {
  margin: 0 0 20px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-title-icon {
  width: 32px;
  height: 32px;
  stroke-width: 2;
}

.filters-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 4px 16px;
  transition: all 0.3s;
}

.search-box:focus-within {
  border-color: #2c974b;
  box-shadow: 0 0 0 3px rgba(44, 151, 75, 0.1);
}

.search-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
  color: #999;
}

.search-input {
  flex: 1;
  padding: 10px 8px;
  font-size: 16px;
  border: none;
  outline: none;
}

.btn-clear {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: #999;
  display: flex;
  align-items: center;
  transition: all 0.2s;
}

.btn-clear:hover {
  color: #d32f2f;
}

.btn-clear svg {
  width: 20px;
  height: 20px;
  stroke-width: 2;
}

.category-filter {
  display: flex;
  align-items: center;
  gap: 12px;
}

.category-filter label {
  font-weight: 500;
  color: #666;
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-icon {
  width: 18px;
  height: 18px;
  stroke-width: 2;
}

.category-select {
  padding: 10px 16px;
  font-size: 15px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  min-width: 250px;
}

.category-select:focus {
  outline: none;
  border-color: #2c974b;
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

.results-header {
  margin-bottom: 20px;
}

.results-count {
  color: #666;
  font-size: 15px;
  margin: 0;
}

.filter-tag {
  color: #2c974b;
  font-weight: 500;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.no-results, .initial-state {
  text-align: center;
  padding: 80px 20px;
  color: #666;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  color: #ccc;
  stroke-width: 1.5;
}

.welcome-icon {
  width: 200px;
  height: 200px;
  margin: 0 auto 20px;
}

.no-results h3, .initial-state h3 {
  color: #333;
  margin: 0 0 10px;
  font-size: 24px;
}

.btn-try-again {
  margin-top: 20px;
  padding: 12px 24px;
  background: #2c974b;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-try-again:hover {
  background: #247a3d;
}

.btn-try-again svg {
  width: 18px;
  height: 18px;
  stroke-width: 2;
}

.popular-categories {
  margin-top: 40px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.popular-categories h4 {
  color: #333;
  margin-bottom: 16px;
}

.category-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.category-chip {
  padding: 10px 20px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.2s;
}

.category-chip:hover {
  border-color: #2c974b;
  color: #2c974b;
  background: #f0fff4;
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
  }

  .category-select {
    min-width: auto;
    width: 100%;
  }
}
</style>