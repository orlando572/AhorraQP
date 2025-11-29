<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="logo">AhorraQP</router-link>
      
      <div class="nav-links">
        <router-link to="/">Inicio</router-link>
        <router-link to="/search">Buscar</router-link>
        <router-link to="/cart" class="cart-link">
          🛒 Carrito ({{ cartStore.itemCount }})
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useCartStore } from '@/store/modules/cart'

const cartStore = useCartStore()
</script>

<style scoped>
.navbar {
  background: #2c974b;
  color: white;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  text-decoration: none;
  color: white;
}

.nav-links {
  display: flex;
  gap: 30px;
  align-items: center;
}

.nav-links a {
  color: white;
  text-decoration: none;
  transition: opacity 0.3s;
}

.nav-links a:hover {
  opacity: 0.8;
}

.nav-links .router-link-active {
  font-weight: bold;
  border-bottom: 2px solid white;
  padding-bottom: 4px;
}

.cart-link {
  background: rgba(255,255,255,0.2);
  padding: 8px 16px;
  border-radius: 20px;
}

@media (max-width: 768px) {
  .nav-links {
    gap: 15px;
    font-size: 14px;
  }
}
</style>