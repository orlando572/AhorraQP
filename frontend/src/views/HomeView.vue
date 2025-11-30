<template>
  <div class="home-view">
    <!-- Hero Section Mejorado -->
    <div class="hero">
      <div class="hero-content">
        <div class="hero-badge">🛒 Compara y Ahorra</div>
        <h1 class="hero-title">
          Encuentra los <span class="highlight">mejores precios</span> en supermercados
        </h1>
        <p class="hero-subtitle">
          Compara precios entre tiendas al instante y ahorra dinero en tus compras del día a día
        </p>
        <div class="hero-actions">
          <router-link to="/search" class="btn-primary">
            <span>Comenzar a Buscar</span>
            <span class="arrow">→</span>
          </router-link>
          <router-link to="/cart" class="btn-secondary">
            Ver mi Carrito
          </router-link>
        </div>
        
        <!-- Stats -->
        <div class="stats">
          <div class="stat-item">
            <div class="stat-number">3+</div>
            <div class="stat-label">Supermercados</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">1000+</div>
            <div class="stat-label">Productos</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">100%</div>
            <div class="stat-label">Gratis</div>
          </div>
        </div>
      </div>
      
      <div class="hero-decoration">
        <div class="floating-card card-1">
          <div class="mini-product">
            <div class="mini-icon">🍚</div>
            <div class="mini-info">
              <span>Arroz</span>
              <span class="mini-price">S/ 3.50</span>
            </div>
          </div>
        </div>
        <div class="floating-card card-2">
          <div class="mini-product">
            <div class="mini-icon">🥛</div>
            <div class="mini-info">
              <span>Leche</span>
              <span class="mini-price">S/ 4.20</span>
            </div>
          </div>
        </div>
        <div class="floating-card card-3">
          <div class="mini-product">
            <div class="mini-icon">💧</div>
            <div class="mini-info">
              <span>Agua</span>
              <span class="mini-price">S/ 6.90</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stores Section Mejorado -->
    <div class="stores-section">
      <div class="stores-header">
        <h2 class="section-title">Supermercados Disponibles</h2>
        <p class="section-subtitle">Comparamos precios en las principales cadenas de supermercados</p>
      </div>
      
      <div v-if="stores.length > 0" class="stores-grid">
        <div v-for="store in stores" :key="store.id" class="store-card">
          <div class="store-logo">
            <img v-if="store.logo_url" :src="store.logo_url" :alt="store.name">
            <span v-else class="store-initial">{{ store.name.charAt(0) }}</span>
          </div>
          <p class="store-name">{{ store.name }}</p>
        </div>
      </div>
      
      <div v-else class="stores-loading">
        <div class="spinner"></div>
        <p>Cargando supermercados...</p>
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
  min-height: 100vh;
}

/* Hero Section Mejorado */
.hero {
  position: relative;
  background: linear-gradient(135deg, #2c974b 0%, #1e6b35 100%);
  color: white;
  padding: 80px 40px;
  overflow: hidden;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  min-height: 600px;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%);
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 600px;
}

.hero-badge {
  display: inline-block;
  background: rgba(255,255,255,0.2);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 20px;
  backdrop-filter: blur(10px);
}

.hero-title {
  font-size: 52px;
  font-weight: 800;
  line-height: 1.2;
  margin: 0 0 20px;
}

.highlight {
  background: linear-gradient(120deg, #fff 0%, #a8e6cf 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 20px;
  line-height: 1.6;
  opacity: 0.95;
  margin: 0 0 40px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 60px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  background: white;
  color: #2c974b;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 16px;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

.arrow {
  transition: transform 0.3s;
}

.btn-primary:hover .arrow {
  transform: translateX(5px);
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  padding: 16px 32px;
  background: transparent;
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: rgba(255,255,255,0.1);
  border-color: white;
}

/* Stats */
.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 36px;
  font-weight: 800;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

/* Hero Decoration */
.hero-decoration {
  position: relative;
  height: 100%;
}

.floating-card {
  position: absolute;
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.15);
  animation: float 3s ease-in-out infinite;
}

.card-1 {
  top: 10%;
  right: 20%;
  animation-delay: 0s;
}

.card-2 {
  top: 45%;
  right: 10%;
  animation-delay: 1s;
}

.card-3 {
  top: 70%;
  right: 35%;
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.mini-product {
  display: flex;
  align-items: center;
  gap: 12px;
}

.mini-icon {
  font-size: 32px;
}

.mini-info {
  display: flex;
  flex-direction: column;
  color: #333;
}

.mini-info span:first-child {
  font-weight: 600;
  font-size: 14px;
}

.mini-price {
  color: #2c974b;
  font-weight: 700;
  font-size: 18px;
}

/* Stores Section */
  .stores-section {
  background: #f8f9fa;
  padding: 80px 40px;
}

.stores-header {
  max-width: 1200px;
  margin: 0 auto 50px;
}

.section-title {
  text-align: center;
  font-size: 36px;
  font-weight: 800;
  color: #333;
  margin: 0 0 10px;
}

.section-subtitle {
  text-align: center;
  font-size: 18px;
  color: #666;
  margin: 0 0 50px;
}

.stores-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 24px;
}

.store-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.store-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  border-color: #2c974b;
}

.store-logo {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.store-logo img {
  max-width: 100%;
  max-height: 80px;
  object-fit: contain;
}

.store-initial {
  width: 60px;
  height: 60px;
  background: #2c974b;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
}

.store-name {
  font-weight: 600;
  color: #333;
  margin: 0;
}

.stores-loading {
  text-align: center;
  padding: 60px;
  color: #666;
}

.spinner {
  margin: 0 auto 20px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #2c974b;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 1024px) {
  .hero {
    grid-template-columns: 1fr;
    padding: 60px 30px;
    min-height: auto;
  }
  
  .hero-decoration {
    display: none;
  }
  
  .hero-title {
    font-size: 42px;
  }
  
  .hero-actions {
    flex-direction: column;
  }
  
  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 40px 20px;
  }
  
  .hero-title {
    font-size: 32px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .stats {
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
  }
  
  .stat-number {
    font-size: 24px;
  }
  
  .features-section,
  .stores-section,
  .cta-section {
    padding: 50px 20px;
  }
  
  .cta-content h2 {
    font-size: 28px;
  }
}
</style>