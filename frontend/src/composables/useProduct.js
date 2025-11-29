import { ref } from 'vue'
import productService from '@/services/productService'

export const useProduct = () => {
  const product = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const getProduct = async (id) => {
    loading.value = true
    error.value = null

    try {
      const response = await productService.getProduct(id)
      product.value = response.data
    } catch (err) {
      error.value = 'Error al cargar el producto'
      console.error('Get product error:', err)
    } finally {
      loading.value = false
    }
  }

  const getMinPrice = () => {
    if (!product.value || !product.value.prices) return 0
    return Math.min(...product.value.prices.map(p => parseFloat(p.price)))
  }

  const getMaxPrice = () => {
    if (!product.value || !product.value.prices) return 0
    return Math.max(...product.value.prices.map(p => parseFloat(p.price)))
  }

  const getAvailableStores = () => {
    if (!product.value) return []
    return product.value.prices.filter(p => p.is_available)
  }

  return {
    product,
    loading,
    error,
    getProduct,
    getMinPrice,
    getMaxPrice,
    getAvailableStores
  }
}
