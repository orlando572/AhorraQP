<template>
  <div class="cart-item">
    <img
      :src="item.product.image_url || '/placeholder.png'"
      :alt="item.product.name"
      class="item-image"
    />

    <div class="item-info">
      <h3>{{ item.product.name }}</h3>
      <p class="brand">{{ item.product.brand_name }}</p>
    </div>

    <div class="quantity-control">
      <button @click="decreaseQuantity" class="qty-btn">−</button>
      <input
        :value="item.quantity"
        @change="updateQuantity"
        type="number"
        min="1"
        class="qty-input"
      />
      <button @click="increaseQuantity" class="qty-btn">+</button>
    </div>

    <button @click="remove" class="btn-remove" title="Eliminar">
      🗑️
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update-quantity', 'remove'])

const increaseQuantity = () => {
  emit('update-quantity', props.item.product_id, props.item.quantity + 1)
}

const decreaseQuantity = () => {
  if (props.item.quantity > 1) {
    emit('update-quantity', props.item.product_id, props.item.quantity - 1)
  }
}

const updateQuantity = (e) => {
  const qty = parseInt(e.target.value) || 1
  if (qty > 0) {
    emit('update-quantity', props.item.product_id, qty)
  }
}

const remove = () => {
  if (confirm('¿Eliminar este producto?')) {
    emit('remove', props.item.product_id)
  }
}
</script>

<style scoped>
.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
  background: white;
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: contain;
  background: #f5f5f5;
  border-radius: 4px;
}

.item-info h3 {
  margin: 0;
  font-size: 16px;
}

.brand {
  margin: 4px 0 0;
  font-size: 14px;
  color: #999;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.qty-btn:hover {
  background: #f5f5f5;
}

.qty-input {
  width: 50px;
  text-align: center;
  border: 1px solid #ddd;
  padding: 4px;
  border-radius: 4px;
}

.btn-remove {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  padding: 8px;
}

@media (max-width: 768px) {
  .cart-item {
    grid-template-columns: 60px 1fr;
  }
}
</style>

