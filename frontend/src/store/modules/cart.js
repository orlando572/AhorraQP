import { defineStore } from 'pinia'
import cartService from '@/services/cartService'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    totals: [],
    loading: false
  }),

  getters: {
    itemCount: (state) => state.items.length,
    totalItems: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0)
  },

  actions: {
    addItem(product) {
      const existing = this.items.find(item => item.product_id === product.id)
      
      if (existing) {
        existing.quantity++
      } else {
        this.items.push({
          product_id: product.id,
          product: product,
          quantity: 1
        })
      }
      
      this.calculateTotals()
    },

    removeItem(productId) {
      this.items = this.items.filter(item => item.product_id !== productId)
      this.calculateTotals()
    },

    updateQuantity(productId, quantity) {
      const item = this.items.find(item => item.product_id === productId)
      if (item) {
        item.quantity = quantity
        if (quantity <= 0) {
          this.removeItem(productId)
        } else {
          this.calculateTotals()
        }
      }
    },

    async calculateTotals() {
      if (this.items.length === 0) {
        this.totals = []
        return
      }

      this.loading = true
      try {
        const cartItems = this.items.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity
        }))
        
        const response = await cartService.calculateTotals(cartItems)
        this.totals = response.data.totals
      } catch (error) {
        console.error('Error calculando totales:', error)
      } finally {
        this.loading = false
      }
    },

    clearCart() {
      this.items = []
      this.totals = []
    }
  },

  persist: true 
})