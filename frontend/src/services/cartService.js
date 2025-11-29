import api from './api'

export default {
  // Calcular totales del carrito
  calculateTotals(items) {
    return api.post('/api/cart/calculate', { items })
  }
}