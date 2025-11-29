import api from './api'

export default {
  // Obtener todas las categorías
  getCategories() {
    return api.get('/api/categories/')
  }
}