import api from './api'

export default {
  // Listar tiendas
  getStores() {
    return api.get('/api/stores/')
  }
}