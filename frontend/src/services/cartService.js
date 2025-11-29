import api from './api'

export default {
  // Calcular totales del carrito
  calculateTotals(items) {
    return api.post('/api/cart/calculate', { items })
  },

  // Guardar carrito en la base de datos
  saveCart(cartData) {
    return api.post('/api/cart/save', cartData)
  }
}