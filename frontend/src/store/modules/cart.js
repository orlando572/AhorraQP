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
    
    // Obtener total por tienda específica
    getTotalByStore: (state) => (storeId) => {
      return state.items
        .filter(item => item.selected_store_id === storeId)
        .reduce((sum, item) => sum + (parseFloat(item.selected_price) * item.quantity), 0)
    },
    
    // Agrupar items por tienda
    itemsByStore: (state) => {
      const grouped = {}
      state.items.forEach(item => {
        const storeId = item.selected_store_id
        if (!grouped[storeId]) {
          grouped[storeId] = {
            store_id: storeId,
            store_name: item.selected_store_name,
            items: [],
            total: 0
          }
        }
        grouped[storeId].items.push(item)
        grouped[storeId].total += parseFloat(item.selected_price) * item.quantity
      })
      return Object.values(grouped)
    },
    
    // Obtener la tienda con mejor precio
    bestStore: (state) => {
      const stores = Object.values(state.itemsByStore)
      if (stores.length === 0) return null
      return stores.reduce((best, current) => 
        current.total < best.total ? current : best
      )
    }
  },

  actions: {
    // Agregar item con tienda seleccionada
    addItem(product) {
      // Buscar si ya existe este producto de esta tienda
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
            image_url: product.image_url
          },
          quantity: 1,
          selected_store_id: product.selected_store_id,
          selected_store_name: product.selected_store_name,
          selected_price: product.selected_price
        })
      }
      
      this.calculateTotals()
    },

    // Remover item
    removeItem(productId, storeId) {
      this.items = this.items.filter(item => 
        !(item.product_id === productId && item.selected_store_id === storeId)
      )
      this.calculateTotals()
    },

    // Actualizar cantidad
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

    // Calcular totales
    async calculateTotals() {
      if (this.items.length === 0) {
        this.totals = []
        return
      }

      this.loading = true
      try {
        // Preparar items agrupados por tienda
        const itemsByStore = {}
        this.items.forEach(item => {
          const storeId = item.selected_store_id
          if (!itemsByStore[storeId]) {
            itemsByStore[storeId] = {
              store_id: storeId,
              store_name: item.selected_store_name,
              total: 0,
              items_count: 0
            }
          }
          itemsByStore[storeId].total += parseFloat(item.selected_price) * item.quantity
          itemsByStore[storeId].items_count += item.quantity
        })
        
        // Convertir a array y ordenar por total
        this.totals = Object.values(itemsByStore).sort((a, b) => a.total - b.total)
        
      } catch (error) {
        console.error('Error calculando totales:', error)
      } finally {
        this.loading = false
      }
    },

    // Guardar carrito en el backend
    async saveCart() {
      if (this.items.length === 0) {
        return { success: false, message: 'El carrito está vacío' }
      }

      try {
        const cartData = {
          items: this.items.map(item => ({
            product_id: item.product_id,
            product_name: item.product.name,
            brand: item.product.brand_name,
            quantity: item.quantity,
            store_id: item.selected_store_id,
            store_name: item.selected_store_name,
            price: item.selected_price,
            subtotal: parseFloat(item.selected_price) * item.quantity
          })),
          totals: this.totals
        }
        
        const response = await cartService.saveCart(cartData)
        this.lastSavedId = response.data.id
        
        return { 
          success: true, 
          message: 'Carrito guardado exitosamente',
          id: response.data.id
        }
      } catch (error) {
        console.error('Error guardando carrito:', error)
        return { 
          success: false, 
          message: 'Error al guardar el carrito' 
        }
      }
    },

    // Limpiar carrito
    clearCart() {
      this.items = []
      this.totals = []
      this.lastSavedId = null
    }
  },

},
{
  // Persistir en localStorage con pinia-plugin-persistedstate v3
  persist: {
    key: 'ahorraQP-cart',
    storage: localStorage,
  }
})