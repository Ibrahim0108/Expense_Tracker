<template>
  <div>
    <!-- HAMBURGER: visible ONLY on small screens -->
    <button
      class="hamburger"
      @click="toggleMenu"
      aria-label="Open menu"
      aria-expanded="false"
    >
      <i class="fas fa-bars"></i>
    </button>

    <!-- SIDEBAR: shown on large screens, or when menuOpen on small screens -->
    <transition name="slide">
      <aside
        v-if="isLargeScreen || menuOpen"
        class="sidebar"
        @click.self="maybeCloseOnBackdrop"
      >
        <div class="sidebar-inner">
          <h2 class="logo"><i class="fas fa-coins" style="margin-right: 8px;"></i> MyBudget</h2>
          <h2>Hey, {{ username }}</h2>

          <nav class="nav">
            <router-link to="/dashboard" class="nav-link" exact><i class="fas fa-chart-line nav-icon"></i> Dashboard</router-link>
            <router-link to="/profile" class="nav-link"><i class="fas fa-user nav-icon"></i> Profile</router-link>
            <router-link to="/history" class="nav-link"><i class="fas fa-calendar-alt nav-icon"></i> History</router-link>
            <button class="nav-logout" @click="logout"><i class="fas fa-sign-out-alt nav-icon"></i> Logout</button>
          </nav>
        </div>
      </aside>
    </transition>
  </div>
</template>

<script>
export default {
  name: "Sidebar",
  data() {
    return {
      menuOpen: false,
      isLargeScreen: window.innerWidth >= 1096,
    };
  },
   props: {
    username: {
      type: String,
      required: true
    }
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
    handleResize() {
      this.isLargeScreen = window.innerWidth >= 1096;
      if (this.isLargeScreen) this.menuOpen = false; // close mobile menu when switching to large
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
    // allow clicking backdrop (aside covers only) to close on mobile
    maybeCloseOnBackdrop(e) {
      if (!this.isLargeScreen && this.menuOpen) this.menuOpen = false;
    },
  },
 mounted() {
    window.addEventListener("resize", this.handleResize);  
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.handleResize);
  },
};
</script>

<style scoped>
/* -- Sidebar base (fixed left) -- */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 250px;
  height: 100vh;
  background: linear-gradient(180deg, #6b4423 0%, #8b5a3c 100%);
  color: #f5e6d3;
  padding: 30px 20px;
  z-index: 1200;
  box-shadow: 4px 0 20px rgba(107, 68, 35, 0.4);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

/* inner wrapper in case we want spacing */
.sidebar-inner {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* logo */
.logo {
  font-size: 24px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 35px;
  color: #f5e6d3;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  font-family: 'Quicksand', sans-serif;
}

/* nav links */
.nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 12px;
}

.nav-link {
  color: #f5e6d3;
  padding: 14px 16px;
  border-radius: 12px;
  text-decoration: none;
  display: block;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  font-family: 'Quicksand', sans-serif;
}

.nav-link.router-link-active {
  background: rgba(245, 230, 211, 0.25);
  color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transform: translateX(5px);
}
.nav-link,
.nav-logout {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-icon {
  font-size: 18px;
  color: #070707; /* calm blue */
}
.nav-link:hover {
  background: rgba(245, 230, 211, 0.15);
  transform: translateX(5px);
  color: #fff;
}

/* logout button styling */
.nav-logout {
  margin-top: auto;
  background: linear-gradient(135deg, #c44536 0%, #a83830 100%);
  color: #f5e6d3;
  border: none;
  text-align: center;
  padding: 14px 16px;
  cursor: pointer;
  border-radius: 12px;
  font-weight: 700;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(196, 69, 54, 0.3);
  font-family: 'Quicksand', sans-serif;
}
.nav-logout .nav-icon {
  color: #ef4444; /* red for logout */
}

.logo i {
  color: #22c55e; /* green highlight */
}

.username i {
  color: #f59e0b; /* gold tone */
}
.nav-logout:hover {
  background: linear-gradient(135deg, #a83830 0%, #8b2f28 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(196, 69, 54, 0.45);
}

.nav-logout:active {
  transform: translateY(0);
}

/* -- Hamburger button (mobile only) -- */
.hamburger {
  display: none; /* hidden by default; visible only on small screens */
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1300;
  background: linear-gradient(135deg, #d4a574 0%, #c4956a 100%);
  color: #4a3728;
  border: 3px solid #8b5a3c;
  padding: 12px 16px;
  font-size: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(107, 68, 35, 0.35);
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 700;
}

.hamburger:hover {
  background: linear-gradient(135deg, #c4956a 0%, #a88763 100%);
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(107, 68, 35, 0.5);
}

.hamburger:active {
  transform: scale(1.05);
}

/* slide transition for mobile open/close */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

/* -- RESPONSIVE RULES -- */
/* Large screens: keep sidebar visible, hide hamburger */
@media (min-width: 1096px) {
  .hamburger {
    display: none;
  }
  
  .sidebar {
    transform: translateX(0); /* always visible */
     display: flex;
  }
}

/* Tablet and below: hide sidebar by default; hamburger visible */
@media (max-width: 1095px) {
  .hamburger {
    display: block;
  }
  
  /* when v-if shows the aside it will slide in because of transition */
  .sidebar {
    width: 270px;
    background: linear-gradient(180deg, rgba(107, 68, 35, 0.98) 0%, rgba(139, 90, 60, 0.98) 100%);
    backdrop-filter: blur(8px);
    box-shadow: 4px 0 25px rgba(0, 0, 0, 0.5);
  }

  .logo {
    font-size: 22px;
    margin-bottom: 20px;
    margin-top: 40px;
  }

  .nav-link {
    font-size: 15px;
    padding: 12px 14px;
  }

  .nav-logout {
    font-size: 15px;
    padding: 12px 14px;
  }
}

/* Mobile portrait */
@media (max-width: 480px) {
  .hamburger {
    top: 15px;
    left: 15px;
    padding: 10px 14px;
    font-size: 22px;
  }

  .sidebar {
    width: 250px;
    padding: 55px 18px;
  }

  .logo {
    font-size: 20px;
    margin-bottom: 25px;
  }

  .nav {
    gap: 10px;
  }

  .nav-link {
    font-size: 14px;
    padding: 11px 12px;
  }

  .nav-logout {
    font-size: 14px;
    padding: 11px 12px;
  }
}

/* Very small screens */
@media (max-width: 360px) {
  .sidebar {
    width: 230px;
    padding: 20px 15px;
  }

  .hamburger {
    padding: 8px 12px;
    font-size: 20px;
  }
}
</style>
