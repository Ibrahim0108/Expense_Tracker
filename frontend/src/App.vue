

<template>
  <div id="app" class="p-5">
    <router-view />

    <footer class="app-footer">
  <span>© 2024 MyBudget</span>
  <span class="divider">•</span>
  <span>Ibrahim</span>
</footer>

  </div>
</template>

<script >
export default {
  name: "App",
};
</script>

<style scoped>
.app-footer {
  position: fixed;
  bottom: 0;
  left: 0;

  width: 100vw;
  text-align: center;

  padding: 12px 16px;
  font-size: 14px;
  color: #6b4423;

  background: rgba(245, 230, 211, 0.98);
  border-top: 1px solid #d4a574;
  z-index: 1000;
}

/* Small screens */
@media (max-width: 768px) {
  .app-footer {
    font-size: 13px;
    padding: 10px 12px;
  }
}

/* Very small screens */
@media (max-width: 450px) {
  .app-footer {
    font-size: 12px;
    padding: 8px 6px;
  }

  .app-footer span {
    display: block;
    line-height: 1.4;
  }

  .divider {
    display: none;
  }
}


</style>
