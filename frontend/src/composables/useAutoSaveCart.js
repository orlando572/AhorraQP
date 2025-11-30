import { watch } from 'vue'
import { useCartStore } from '@/store/modules/cart'
import cartService from '@/services/cartService'

export const useAutoSaveCart = () => {
  const cartStore = useCartStore()
  let saveTimeout = null

  // Auto-guardar el carrito cuando cambia
  watch(
    () => cartStore.items,
    (items) => {
      // Si el carrito está vacío, no guardar
      if (items.length === 0) return

      // Debounce: esperar 2 segundos después del último cambio
      clearTimeout(saveTimeout)
      
      saveTimeout = setTimeout(async () => {
        try {
          // Preparar los datos para guardar
          const cartData = {
            items: items.map(item => ({
              product_id: item.product_id,
              product_name: item.product.name,
              brand_name: item.product.brand_name,
              quantity: item.quantity,
              store_name: item.selected_store_name,
              price: item.selected_price
            })),
            totals: {
              total_items: cartStore.totalItems,
              cart_total: cartStore.cartTotal,
              total_savings: cartStore.totalSavings
            }
          }

          // Guardar en la base de datos
          await cartService.saveCart(cartData)
          
          console.log('✅ Carrito guardado automáticamente')
        } catch (error) {
          console.error('Error guardando carrito:', error)
          // No mostrar error al usuario, es un guardado silencioso
        }
      }, 2000) // Esperar 2 segundos después del último cambio
    },
    { deep: true }
  )
}