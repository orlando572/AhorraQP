export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const ENDPOINTS = {
  PRODUCTS: {
    SEARCH: '/api/products/search',
    GET: (id) => `/api/products/${id}`,
    LIST: '/api/products/'
  },
  CART: {
    CALCULATE: '/api/cart/calculate'
  },
  STORES: {
    LIST: '/api/stores/'
  }
}

export const MESSAGES = {
  ERROR_LOADING_PRODUCTS: 'Error al cargar los productos',
  ERROR_LOADING_PRODUCT: 'Error al cargar el producto',
  ERROR_CALCULATING_CART: 'Error al calcular el carrito',
  SUCCESS_ADDED_TO_CART: 'Producto agregado al carrito',
  SUCCESS_REMOVED_FROM_CART: 'Producto eliminado del carrito',
  EMPTY_SEARCH: 'Por favor ingresa un término de búsqueda',
  NO_RESULTS: 'No se encontraron productos'
}

export const SORT_OPTIONS = [
  { value: 'relevance', label: 'Relevancia' },
  { value: 'price-asc', label: 'Precio: Menor a Mayor' },
  { value: 'price-desc', label: 'Precio: Mayor a Menor' },
  { value: 'name', label: 'Nombre' }
]
