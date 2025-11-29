import api from './api'

export default {
  // Buscar productos
  searchProducts(query, categoryId = null) {
    return api.get('/api/products/search', {
      params: { q: query, category_id: categoryId }
    })
  },

  // Obtener producto por ID
  getProduct(productId) {
    return api.get(`/api/products/${productId}`)
  },

  // Listar productos
  listProducts(skip = 0, limit = 50) {
    return api.get('/api/products/', {
      params: { skip, limit }
    })
  }
}