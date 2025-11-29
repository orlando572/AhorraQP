<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>AhorraQP</h3>
        <p>Compara precios y ahorra dinero en tus compras</p>
      </div>
      
      <div class="footer-section">
        <h4>Enlaces</h4>
        <ul>
          <li><router-link to="/">Inicio</router-link></li>
          <li><router-link to="/search">Buscar</router-link></li>
          <li><router-link to="/cart">Carrito</router-link></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4>Contacto</h4>
        <p>Email: info@ahorraQp.pe</p>
        <p>Teléfono: +51 XXX XXX XXX</p>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; 2025 AhorraQP</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #222;
  color: white;
  margin-top: 60px;
  padding: 40px 20px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-bottom: 20px;
}

.footer-section h3,
.footer-section h4 {
  margin-top: 0;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section a {
  color: #ccc;
  text-decoration: none;
}

.footer-section a:hover {
  color: #2c974b;
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #444;
  color: #888;
}
</style>