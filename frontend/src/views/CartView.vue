<template>
  <div class="cart-view">
    <h1>Carrito de Compras</h1>

    <div v-if="cartStore.items.length === 0" class="empty-cart">
      <p>Tu carrito está vacío</p>
      <router-link to="/search" class="btn-continue">Seguir Comprando</router-link>
    </div>

    <div v-else class="cart-container">
      <div class="cart-items-section">
        <h2>Productos ({{ cartStore.totalItems }})</h2>
        
        <div class="cart-items">
          <div v-for="item in cartStore.items" :key="item.product_id" class="cart-item">
            <img :src="item.product.image_url || '/placeholder.png'" :alt="item.product.name">
            
            <div class="item-details">
              <h3>{{ item.product.name }}</h3>
              <p class="brand">{{ item.product.brand_name }}</p>
            </div>

            <div class="item-quantity">
              <button @click="decreaseQuantity(item.product_id)">−</button>
              <input v-model.number="item.quantity" type="number" min="1">
              <button @click="increaseQuantity(item.product_id)">+</button>
            </div>

            <button @click="removeItem(item.product_id)" class="btn-remove">
              🗑️ Eliminar
            </button>
          </div>
        </div>

        <button @click="clearCart" class="btn-clear-cart">Limpiar Carrito</button>
      </div>

      <div class="totals-section">
        <h2>Totales por Tienda</h2>

        <div v-if="cartStore.loading" class="loading">
          <p>Calculando totales...</p>
        </div>

        <div v-else class="totals-list">
          <div v-for="total in cartStore.totals" :key="total.store_id" class="total-card">
            <div class="store-header">
              <h3>{{ total.store_name }}</h3>
              <span class="total-price">S/ {{ formatPrice(total.total) }}</span>
            </div>

            <div class="store-details">
              <p>✓ Disponibles: {{ total.items_available }}</p>
              <p v-if="total.items_unavailable > 0" class="unavailable">
                ✗ No disponibles: {{ total.items_unavailable }}
              </p>
            </div>

            <a href="#" class="btn-shop">Comprar en {{ total.store_name }}</a>
          </div>
        </div>

        <button v-if="cartStore.totals.length > 0" @click="goToStore" class="btn-best-price">
          Comprar en tienda con mejor precio
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/store/modules/cart'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const router = useRouter()

const formatPrice = (price) => {
  return parseFloat(price).toFixed(2)
}

const increaseQuantity = (productId) => {
  const item = cartStore.items.find(i => i.product_id === productId)
  if (item) {
    cartStore.updateQuantity(productId, item.quantity + 1)
  }
}

const decreaseQuantity = (productId) => {
  const item = cartStore.items.find(i => i.product_id === productId)
  if (item) {
    cartStore.updateQuantity(productId, item.quantity - 1)
  }
}

const removeItem = (productId) => {
  if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {
    cartStore.removeItem(productId)
  }
}

const clearCart = () => {
  if (confirm('¿Estás seguro de que quieres limpiar el carrito?')) {
    cartStore.clearCart()
  }
}

const goToStore = () => {
  if (cartStore.totals.length > 0) {
    const bestStore = cartStore.totals[0]
    alert(`Mejor precio en: ${bestStore.store_name} - S/ ${formatPrice(bestStore.total)}`)
  }
}
</script>

<style scoped>
.cart-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.empty-cart {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.btn-continue {
  display: inline-block;
  margin-top: 20px;
  padding: 12px 24px;
  background: #2c974b;
  color: white;
  text-decoration: none;
  border-radius: 8px;
}

.cart-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.cart-items-section h2 {
  margin-top: 0;
}

.cart-items {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
  align-items: center;
}

.cart-item:last-child {
  border-bottom: none;
}

.cart-item img {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

.item-details h3 {
  margin: 0 0 4px;
  font-size: 16px;
}

.brand {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-quantity input {
  width: 50px;
  text-align: center;
}

.item-quantity button {
  width: 30px;
  height: 30px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}

.btn-remove {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

.btn-clear-cart {
  width: 100%;
  padding: 12px;
  margin-top: 20px;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.totals-section {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  height: fit-content;
}

.totals-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.total-card {
  background: white;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.store-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.store-header h3 {
  margin: 0;
}

.total-price {
  font-size: 20px;
  font-weight: bold;
  color: #2c974b;
}

.store-details {
  font-size: 14px;
  margin: 10px 0;
  color: #666;
}

.unavailable {
  color: #d32f2f;
}

.btn-shop {
  display: block;
  width: 100%;;
  padding: 10px;
  margin-top: 10px;
  background: #2c974b;
  color: white;
  text-align: center;
  text-decoration: none;
  border-radius: 4px;
  font-size: 14px;
}

.btn-best-price {
  width: 100%;
  padding: 12px;
  margin-top: 20px;
  background: #2c974b;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

@media (max-width: 768px) {
  .cart-container {
    grid-template-columns: 1fr;
  }

  .cart-item {
    grid-template-columns: 60px 1fr;
  }
}
</style>