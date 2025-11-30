<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="logo">
        AhorraQP
      </router-link>
      
      <div class="nav-links">
        <router-link to="/" class="nav-link">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke-width="2"/>
            <polyline points="9 22 9 12 15 12 15 22" stroke-width="2"/>
          </svg>
          Inicio
        </router-link>
        
        <router-link to="/search" class="nav-link">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="11" cy="11" r="8" stroke-width="2"/>
            <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
          </svg>
          Buscar
        </router-link>
        
        <router-link to="/cart" class="cart-link">
          <svg class="cart-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="9" cy="21" r="1" fill="currentColor"/>
            <circle cx="20" cy="21" r="1" fill="currentColor"/>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Carrito
          <span v-if="cartStore.itemCount > 0" class="cart-badge">{{ cartStore.itemCount }}</span>
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
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  width: 28px;
  height: 28px;
  stroke-width: 2;
}

.nav-links {
  display: flex;
  gap: 30px;
  align-items: center;
}

.nav-link,
.cart-link {
  color: white;
  text-decoration: none;
  transition: opacity 0.3s;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
}

.nav-icon {
  width: 18px;
  height: 18px;
  stroke-width: 2;
}

.nav-link:hover,
.cart-link:hover {
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
  position: relative;
}

.cart-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
}

.cart-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #ff4444;
  color: white;
  font-size: 11px;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

@media (max-width: 768px) {
  .nav-links {
    gap: 15px;
    font-size: 14px;
  }
  
  .nav-link span:not(.cart-badge),
  .cart-link span:not(.cart-badge) {
    display: none;
  }
}
</style>