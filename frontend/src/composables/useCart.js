import { computed } from 'vue'
import { useCartStore } from '@/store/modules/cart'

export const useCart = () => {
  const cartStore = useCartStore()

  const isEmpty = computed(() => cartStore.items.length === 0)
  const itemCount = computed(() => cartStore.itemCount)
  const totalItems = computed(() => cartStore.totalItems)
  const hasUnavailableItems = computed(() => {
    return cartStore.totals.some(t => t.items_unavailable > 0)
  })

  const addItem = (product) => {
    cartStore.addItem(product)
  }

  const removeItem = (productId) => {
    cartStore.removeItem(productId)
  }

  const updateQuantity = (productId, quantity) => {
    cartStore.updateQuantity(productId, quantity)
  }

  const clear = () => {
    cartStore.clearCart()
  }

  const getBestPrice = () => {
    if (cartStore.totals.length === 0) return null
    return cartStore.totals[0]
  }

  return {
    isEmpty,
    itemCount,
    totalItems,
    hasUnavailableItems,
    addItem,
    removeItem,
    updateQuantity,
    clear,
    getBestPrice,
    items: computed(() => cartStore.items),
    totals: computed(() => cartStore.totals),
    loading: computed(() => cartStore.loading)
  }
}
