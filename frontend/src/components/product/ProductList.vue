<template>
  <div class="product-list">
    <div v-if="products.length === 0" class="empty-state">
      <p>{{ emptyMessage }}</p>
    </div>

    <div v-else class="products-grid">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
        @add-to-cart="$emit('add-to-cart', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import ProductCard from './ProductCard.vue'

defineProps({
  products: {
    type: Array,
    required: true
  },
  emptyMessage: {
    type: String,
    default: 'No hay productos disponibles'
  }
})

defineEmits(['add-to-cart'])
</script>

<style scoped>
.product-list {
  width: 100%;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}
</style>
