import { ref } from 'vue'
import productService from '@/services/productService'

export const useSearch = () => {
  const results = ref([])
  const loading = ref(false)
  const error = ref(null)
  let searchTimeout = null

  const search = async (query, categoryId = null) => {
    if (!query || query.trim().length < 2) {
      results.value = []
      return
    }

    clearTimeout(searchTimeout)
    
    searchTimeout = setTimeout(async () => {
      loading.value = true
      error.value = null

      try {
        const response = await productService.searchProducts(query, categoryId)
        results.value = response.data
      } catch (err) {
        error.value = 'Error en la búsqueda'
        results.value = []
        console.error('Search error:', err)
      } finally {
        loading.value = false
      }
    }, 300)
  }

  const clearSearch = () => {
    results.value = []
    error.value = null
    clearTimeout(searchTimeout)
  }

  return {
    results,
    loading,
    error,
    search,
    clearSearch
  }
}