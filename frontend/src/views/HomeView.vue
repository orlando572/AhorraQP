<template>
  <div class="home-view">
    <div class="hero">
      <h1>Bienvenido a AhorraQP</h1>
      <p>Compara precios entre supermercados y ahorra dinero</p>
      <router-link to="/search" class="btn-primary">Comenzar a Buscar</router-link>
    </div>

    <div class="features">
      <div class="feature-card">
        <h3> Compara Precios</h3>
        <p>Ve los precios en diferentes supermercados al instante</p>
      </div>
      <div class="feature-card">
        <h3> Lista de Compras</h3>
        <p>Crea tu carrito y ve cuál tienda es más económica</p>
      </div>
      <div class="feature-card">
        <h3> Ahorra Dinero</h3>
        <p>Compra en la tienda con los mejores precios</p>
      </div>
    </div>

    <div class="stores-section">
      <h2>Supermercados Disponibles</h2>
      <div class="stores-grid">
        <div v-for="store in stores" :key="store.id" class="store-card">
          <img v-if="store.logo_url" :src="store.logo_url" :alt="store.name">
          <p>{{ store.name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import storeService from '@/services/storeService'

const stores = ref([])

onMounted(async () => {
  try {
    const response = await storeService.getStores()
    stores.value = response.data
  } catch (error) {
    console.error('Error cargando tiendas:', error)
  }
})
</script>

<style scoped>
.home-view {
  padding: 20px;
}

.hero {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #2c974b 0%, #1e6b35 100%);
  color: white;
  border-radius: 12px;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 48px;
  margin: 0 0 16px;
}

.hero p {
  font-size: 20px;
  margin: 0 0 24px;
}

.btn-primary {
  display: inline-block;
  padding: 12px 32px;
  background: white;
  color: #2c974b;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: transform 0.3s;
}

.btn-primary:hover {
  transform: scale(1.05);
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 40px 0;
}

.feature-card {
  padding: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  text-align: center;
}

.feature-card h3 {
  color: #2c974b;
  margin-top: 0;
}

.stores-section {
  margin: 40px 0;
}

.stores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.store-card {
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  text-align: center;
  transition: box-shadow 0.3s;
}

.store-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.store-card img {
  max-width: 100%;
  height: 60px;
  object-fit: contain;
  margin-bottom: 10px;
}
</style>