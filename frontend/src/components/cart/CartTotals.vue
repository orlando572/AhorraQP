<template>
  <div class="cart-totals">
    <h2>Totales por Tienda</h2>

    <div v-if="loading" class="loading">
      <p>Calculando totales...</p>
    </div>

    <div v-else-if="totals.length > 0" class="totals-list">
      <div
        v-for="total in totals"
        :key="total.store_id"
        class="total-card"
        :class="{ 'best-price': isBestPrice(total) }"
      >
        <div class="card-header">
          <h3>{{ total.store_name }}</h3>
          <span class="price">S/ {{ formatPrice(total.total) }}</span>
        </div>

        <div class="card-body">
          <p class="info">
            ✓ Disponibles: <strong>{{ total.items_available }}</strong>
          </p>
          <p v-if="total.items_unavailable > 0" class="info warning">
            ✗ No disponibles: {{ total.items_unavailable }}
          </p>
        </div>

        <button class="btn-shop">
          Comprar en {{ total.store_name }}
        </button>
      </div>
    </div>

    <div v-else class="empty">
      <p>Agrega productos al carrito para ver totales</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  totals: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const formatPrice = (price) => {
  return parseFloat(price).toFixed(2)
}

const isBestPrice = (total) => {
  if (props.totals.length === 0) return false
  return total.store_id === props.totals[0].store_id
}
</script>

<style scoped>
.cart-totals {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}

.cart-totals h2 {
  margin-top: 0;
  margin-bottom: 20px;
}

.totals-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.total-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
}

.total-card.best-price {
  border-color: #2c974b;
  box-shadow: 0 0 0 2px rgba(44, 151, 75, 0.1);
}

.total-card.best-price::before {
  content: '★ MEJOR PRECIO';
  display: block;
  background: #2c974b;
  color: white;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: bold;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.card-header h3 {
  margin: 0;
}

.price {
  font-size: 20px;
  font-weight: bold;
  color: #2c974b;
}

.card-body {
  padding: 12px 15px;
  font-size: 14px;
}

.info {
  margin: 4px 0;
  color: #666;
}

.info.warning {
  color: #d32f2f;
}

.btn-shop {
  width: 100%;
  padding: 12px;
  background: #2c974b;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
}

.btn-shop:hover {
  background: #1e6b35;
}

.loading,
.empty {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}
</style>