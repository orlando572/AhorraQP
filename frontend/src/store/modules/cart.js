import { defineStore } from 'pinia'
import cartService from '@/services/cartService'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    totals: [],
    loading: false,
    lastSavedId: null
  }),

  persist: {
    key: 'ahorraQP-cart',
    storage: localStorage,
  },

  getters: {
    itemCount: (state) => state.items.length,
    totalItems: (state) => state.items.reduce((s, i) => s + i.quantity, 0),
    cartTotal: (state) => state.items.reduce((s, i) => s + (parseFloat(i.selected_price) * i.quantity), 0),

    totalSavings: (state) => {
      return state.items.reduce((saving, item) => {
        const prices = item.product?.prices ?? []
        if (prices.length <= 1) return saving

        const maxPrice = Math.max(
          ...prices.filter(p => p.is_available).map(p => parseFloat(p.price))
        )

        const diff = maxPrice - parseFloat(item.selected_price)
        return diff > 0 ? saving + diff * item.quantity : saving
      }, 0)
    }
  },

  actions: {
    addItem(product) {
      const existing = this.items.find(
        item => item.product_id === product.id && 
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
    },

    removeItem(productId, storeId) {
      this.items = this.items.filter(
        item => !(item.product_id === productId && item.selected_store_id === storeId)
      )
    },

    updateQuantity(productId, storeId, quantity) {
      const item = this.items.find(
        item => item.product_id === productId && item.selected_store_id === storeId
      )

      if (!item) return
      if (quantity <= 0) return this.removeItem(productId, storeId)

      item.quantity = quantity
    },

    clearCart() {
      this.items = []
      this.totals = []
      this.lastSavedId = null
    }
  }
})
