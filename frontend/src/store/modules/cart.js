import { defineStore } from 'pinia'
import cartService from '@/services/cartService'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    totals: [],
    loading: false,
    lastSavedId: null
  }),

  getters: {
    itemCount: (state) => state.items.length,
    
    totalItems: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0),
    
    // Total a pagar (suma de los precios seleccionados)
    cartTotal: (state) => {
      return state.items.reduce((sum, item) => {
        return sum + (parseFloat(item.selected_price) * item.quantity)
      }, 0)
    },

    // Cálculo del Ahorro: Compara el precio seleccionado con el precio MÁS ALTO disponible
    totalSavings: (state) => {
      return state.items.reduce((savings, item) => {
        // 1. Obtener todos los precios disponibles de este producto
        const prices = item.product.prices || []
        
        // 2. Si no hay precios o solo hay 1, no hay comparación
        if (prices.length <= 1) return savings

        // 3. Encontrar el precio más alto disponible
        const availablePrices = prices
          .filter(p => p.is_available)
          .map(p => parseFloat(p.price))
        
        if (availablePrices.length === 0) return savings

        const maxPrice = Math.max(...availablePrices)
        const currentPrice = parseFloat(item.selected_price)

        // 4. Calcular diferencia por unidad
        const diffPerUnit = maxPrice - currentPrice

        // 5. Si la diferencia es positiva, sumar al ahorro
        if (diffPerUnit > 0) {
          return savings + (diffPerUnit * item.quantity)
        }
        
        return savings
      }, 0)
    }
  },

  actions: {
    // Modificamos addItem para guardar el URL y los precios para comparar
    addItem(product) {
      const existing = this.items.find(item => 
        item.product_id === product.id && 
        item.selected_store_id === product.selected_store_id
      )
      
      if (existing) {
        existing.quantity++
      } else {
        this.items.push({
          product_id: product.id,
          product: {
            id: product.id,
            name: product.name,
            brand_name: product.brand_name,
            category_name: product.category_name,
            image_url: product.image_url,
            prices: product.prices 
          },
          quantity: 1,
          selected_store_id: product.selected_store_id,
          selected_store_name: product.selected_store_name,
          selected_price: product.selected_price,
          selected_url: product.selected_url 
        })
      }
      
      this.calculateTotals()
    },

    removeItem(productId, storeId) {
      this.items = this.items.filter(item => 
        !(item.product_id === productId && item.selected_store_id === storeId)
      )
      this.calculateTotals()
    },

    updateQuantity(productId, storeId, quantity) {
      const item = this.items.find(item => 
        item.product_id === productId && item.selected_store_id === storeId
      )
      
      if (item) {
        if (quantity <= 0) {
          this.removeItem(productId, storeId)
        } else {
          item.quantity = quantity
          this.calculateTotals()
        }
      }
    },

    async calculateTotals() {
      // Mantenemos esta lógica solo para compatibilidad
      if (this.items.length === 0) {
        this.totals = []
        return
      }
    },

    clearCart() {
      this.items = []
      this.totals = []
      this.lastSavedId = null
    }
  },
},
{
  persist: {
    key: 'ahorraQP-cart',
    storage: localStorage,
  }
})