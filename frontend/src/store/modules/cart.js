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
      return state.items.reduce((total, item) => {

        if (!item.product || !item.product.prices) return total

        const pricesValues = item.product.prices.map(p => parseFloat(p.price))

        if (pricesValues.length <= 1) return total

        const maxPrice = Math.max(...pricesValues)
        const selectedPrice = parseFloat(item.selected_price)

        const savingsPerUnit = maxPrice - selectedPrice

        if (savingsPerUnit > 0) {
          return total + (savingsPerUnit * item.quantity)
        }

        return total
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

      this._autoSaveCart()
    },

    removeItem(productId, storeId) {
      this.items = this.items.filter(
        item => !(item.product_id === productId && item.selected_store_id === storeId)
      )
      this._autoSaveCart()
    },

    updateQuantity(productId, storeId, quantity) {
      const item = this.items.find(
        item => item.product_id === productId && item.selected_store_id === storeId
      )

      if (!item) return
      if (quantity <= 0) return this.removeItem(productId, storeId)

      item.quantity = quantity
      this._autoSaveCart()
    },

    clearCart() {
      this.items = []
      this.totals = []
      this.lastSavedId = null
    },

    _autoSaveCart() {
      if (this._saveTimeout) clearTimeout(this._saveTimeout)
      if (this.items.length === 0) return

      this._saveTimeout = setTimeout(async () => {
        try {
          const cartData = {
            items: this.items.map(item => ({
              product_id: item.product_id,
              product_name: item.product.name,
              brand_name: item.product.brand_name,
              quantity: item.quantity,
              store_name: item.selected_store_name,
              price: item.selected_price
            })),
            totals: {
              total_items: this.totalItems,
              cart_total: this.cartTotal,
              total_savings: this.totalSavings
            }
          }

          const response = await cartService.saveCart(cartData)
          if (response.data && response.data.id) {
            this.lastSavedId = response.data.id
            console.log('Carrito guardado automáticamente en DB')
          }
        } catch (error) {
          console.error('Error auto-guardando carrito:', error)
        }
      }, 2000)
    }
  }
})