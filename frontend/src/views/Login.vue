<template>
  <div class="login-container">
    
    <div>
      <h2>Enter Username</h2>
      <form @submit.prevent="loginUser">
      <input type="text" v-model="username" placeholder="Username" />
      <button>Login</button>
      </form>
      <p v-if="error">{{ error }}</p>
    </div>
    </div>  
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      pin: "",
      username: "",
      error: "",
      pinVerified: false,
    };
  },
  methods: {

    async loginUser() {
      this.error = "";
      try {
        const res = await axios.post("/api/login", { username: this.username });
        if (res.data.status === "success") {
          // save user data in localStorage/session
           const safeUser = { join_date: res.data.user.join_date };
          localStorage.setItem("user", JSON.stringify(safeUser));
          this.$router.push("/dashboard");
        } else {
          this.error = "Login failed";
        }
      } catch (e) {
        this.error = e.response?.data?.error || "Network Error";
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5e6d3 0%, #d4a574 50%, #c4956a 100%);
  font-family: 'Quicksand', sans-serif;
  padding: 20px;
  overflow: hidden;
}

/* Animated coffee beans floating in background */
.login-container::before {
  content: '☕';
  position: absolute;
  font-size: 120px;
  opacity: 0.08;
  top: 10%;
  left: 15%;
  animation: float 8s ease-in-out infinite;
}

.login-container::after {
  content: '☕';
  position: absolute;
  font-size: 80px;
  opacity: 0.06;
  bottom: 15%;
  right: 20%;
  animation: float 10s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(10deg);
  }
}

/* Login card/box */
.login-container > div {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 249, 240, 0.98) 100%);
  border-radius: 30px;
  padding: 50px 45px;
  max-width: 450px;
  width: 100%;
  box-shadow: 
    0 20px 60px rgba(107, 68, 35, 0.3),
    0 0 0 1px rgba(212, 165, 116, 0.5) inset;
  border: 4px solid #d4a574;
  position: relative;
  z-index: 10;
  animation: slideUp 0.6s ease-out;
  backdrop-filter: blur(10px);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Decorative coffee cup icon on top */
.login-container > div::before {
  content: '☕';
  position: absolute;
  top: -35px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 60px;
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  width: 85px;
  height: 85px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(107, 68, 35, 0.4);
  border: 5px solid #f5e6d3;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(-10px);
  }
}

/* Heading */
.login-container h2 {
  font-size: 32px;
  font-weight: 800;
  color: #6b4423;
  margin-bottom: 35px;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(107, 68, 35, 0.15);
  letter-spacing: 0.5px;
  margin-top: 20px;
}

/* Input field */
.login-container input[type="text"] {
  padding: 18px 24px;
  margin-bottom: 25px;
  border: 3px solid #d4a574;
  border-radius: 16px;
  font-size: 17px;
  background: rgba(255, 255, 255, 0.9);
  color: #4a3728;
  font-family: 'Quicksand', sans-serif;
  font-weight: 600;
  transition: all 0.4s ease;
  box-shadow: 0 4px 15px rgba(107, 68, 35, 0.1) inset;
  text-align: center;
}

.login-container input[type="text"]:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 
    0 0 0 5px rgba(139, 90, 60, 0.2),
    0 4px 15px rgba(107, 68, 35, 0.1) inset;
  background: #ffffff;
  transform: scale(1.02);
}

.login-container input[type="text"]::placeholder {
  color: #a88763;
  font-weight: 500;
}

/* Button */
.login-container button {
  width: 100%;
  padding: 18px 32px;
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  border-radius: 16px;
  font-size: 19px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.4s ease;
  box-shadow: 
    0 8px 20px rgba(107, 68, 35, 0.4),
    0 0 0 3px rgba(212, 165, 116, 0.3);
  font-family: 'Quicksand', sans-serif;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

/* Button shine effect */
.login-container button::before {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.login-container button:hover::before {
  left: 100%;
}

.login-container button:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 
    0 12px 30px rgba(107, 68, 35, 0.5),
    0 0 0 5px rgba(212, 165, 116, 0.4);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.login-container button:active {
  transform: translateY(-1px) scale(1);
  box-shadow: 
    0 6px 15px rgba(107, 68, 35, 0.4),
    0 0 0 3px rgba(212, 165, 116, 0.3);
}

/* Error message */
.login-container p {
  color: #c44536;
  font-weight: 700;
  margin-top: 20px;
  text-align: center;
  padding: 14px 20px;
  background: rgba(196, 69, 54, 0.12);
  border-radius: 12px;
  border: 2px solid rgba(196, 69, 54, 0.3);
  font-size: 15px;
  animation: shake 0.4s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

/* Decorative corner elements */
.login-container > div::after {
  position: absolute;
  bottom: 15px;
  right: 15px;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #d4a574 0%, #c4956a 100%);
  border-radius: 50%;
  opacity: 0.3;
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.3);
    opacity: 0.5;
  }
}

/* Additional decorative element */
.login-container > div {
  position: relative;
}

.login-container > div > *:first-child::before {
  position: absolute;
  top: 15px;
  left: 15px;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  border-radius: 50%;
  opacity: 0.2;
  animation: pulse 3s ease-in-out infinite 1.5s;
}

/* Responsive Design - Tablet */
@media (max-width: 768px) {
  .login-container > div {
    padding: 45px 35px;
    max-width: 400px;
  }

  .login-container h2 {
    font-size: 28px;
    margin-bottom: 30px;
  }

  .login-container input[type="text"] {
    padding: 16px 20px;
    font-size: 16px;
  }

  .login-container button {
    padding: 16px 28px;
    font-size: 17px;
  }

  .login-container > div::before {
    width: 75px;
    height: 75px;
    font-size: 55px;
    top: -32px;
  }
}

/* Responsive Design - Mobile */
@media (max-width: 480px) {
  .login-container {
    padding: 0px;
  }

  .login-container > div {
    padding: 40px 28px;
    border-radius: 25px;
    border-width: 3px;
  }

  .login-container h2 {
    font-size: 26px;
    margin-bottom: 28px;
    margin-top: 15px;
  }

  .login-container input[type="text"] {
    padding: 15px 18px;
    font-size: 15px;
    margin-bottom: 22px;
  }

  .login-container button {
    padding: 15px 24px;
    font-size: 16px;
    letter-spacing: 0.5px;
  }

  .login-container > div::before {
    width: 65px;
    height: 65px;
    font-size: 45px;
    top: -28px;
    border-width: 4px;
  }

  .login-container::before {
    font-size: 90px;
  }

  .login-container::after {
    font-size: 60px;
  }

  .login-container p {
    font-size: 14px;
    padding: 12px 16px;
  }
}

/* Very small screens */
@media (max-width: 360px) {
  .login-container > div {
    padding: 35px 22px;
  }

  .login-container h2 {
    font-size: 24px;
  }

  .login-container button {
    font-size: 15px;
  }
}
</style>
