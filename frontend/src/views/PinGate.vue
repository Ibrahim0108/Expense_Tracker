<template>
      <div class="pin-page">

        <div class="pin-gate" style="padding:16px; max-width:420px; margin:40px auto">
            <div class="warning-header">
                <div class="danger-badge">⚠ RESTRICTED ⚠</div>
                <h2>SECURITY CHECKPOINT</h2>
                <div class="subtitle">AUTHORIZED PERSONNEL ONLY</div>
            </div>
            <h2>Enter Secret PIN</h2>
            <form @submit.prevent="submitPin" id="pinForm">
                <input v-model="pin" placeholder="ENTER ACCESS CODE" autocomplete="one-time-code" type="password" />
                <button :disabled="loading" id="submitBtn">{{ loading ? "Checking..." : "AUTHENTICATE" }}</button>
            </form>
            <div v-if="error" id="errorMessage" class="error" style="color:red">{{ error }}</div>
            <div class="attempts-warning">
                <span id="attemptsLeft">YOU GET 3 ATTEMPTS</span>
            </div>
            <!-- <p v-if="error" style="color:red">{{ error }}</p> -->
        </div>
    </div>
</template>

<script>
export default {
    name: "PinGate",
    data() {
        return { pin: "", loading: false, error: null };
    },
    mounted() {
    // Save current global background
    this.oldBackground = document.body.style.background || "";
    // Set custom background for this page
    document.body.style.background = "linear-gradient(135deg, #1a0000 0%, #330000 50%, #1a0000 100%)";
    },
    beforeUnmount() {
    // Restore previous background when leaving page
    document.body.style.background = this.oldBackground;
    },
    methods: {
        async submitPin() {
            this.loading = true;
            this.error = null;
            try {
                const res = await fetch("/api/pin/verify", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ pin: this.pin }),
                });
                const data = await res.json();
                if (!res.ok || !data.ok) {
                    this.error = data.error || "Invalid pin";
                } else {
                    // unlocked — navigate to dashboard
                    this.$router.push({ name: "Login" });
                }
            } catch (err) {
                this.error = "Network error";
            } finally {
                this.loading = false;
            }
        },
    },
};
</script>

<style scoped>
body {
    box-sizing: border-box;
    background: linear-gradient(135deg, #1a0000 0%, #330000 50%, #1a0000 100%) !important;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
}

/* Animated background pattern */
body::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image:
        repeating-linear-gradient(45deg,
            transparent,
            transparent 2px,
            rgba(255, 0, 0, 0.03) 2px,
            rgba(255, 0, 0, 0.03) 4px);
    animation: scan 3s linear infinite;
}

@keyframes scan {
    0% {
        transform: translateY(-100%);
    }

    100% {
        transform: translateY(100vh);
    }
}


.pin-gate {
    background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
    border: 3px solid #ff0000;
    border-radius: 8px;
    box-shadow:
        0 0 30px rgba(255, 0, 0, 0.5),
        inset 0 0 20px rgba(255, 0, 0, 0.1);
    padding: 40px 32px;
    width: 100%;
    max-width: 400px;
    margin: 20px;
    position: relative;
    z-index: 10;
    animation: pulse-border 2s ease-in-out infinite alternate;
}

@keyframes pulse-border {
    0% {
        border-color: #ff0000;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.5), inset 0 0 20px rgba(255, 0, 0, 0.1);
    }

    100% {
        border-color: #ff4444;
        box-shadow: 0 0 50px rgba(255, 0, 0, 0.8), inset 0 0 30px rgba(255, 0, 0, 0.2);
    }
}

.warning-header {
    text-align: center;
    margin-bottom: 20px;
}

.danger-badge {
    background: #ff0000;
    color: #ffffff;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
    border-radius: 4px;
    margin-bottom: 16px;
    animation: blink 1.5s infinite;
}

@keyframes blink {

    0%,
    50% {
        opacity: 1;
    }

    51%,
    100% {
        opacity: 0.3;
    }
}

h2 {
    color: #ff0000;
    text-align: center;
    margin: 0 0 8px 0;
    font-size: 24px;
    font-weight: bold;
    letter-spacing: 3px;
    text-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
    animation: flicker 3s infinite;
}

@keyframes flicker {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0.8;
    }

    75% {
        opacity: 0.9;
    }
}

.subtitle {
    color: #ffaa00;
    text-align: center;
    font-size: 12px;
    margin-bottom: 32px;
    letter-spacing: 1px;
    opacity: 0.9;
}

form {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

input {
    padding: 18px 20px;
    border: 2px solid #666666;
    border-radius: 4px;
    font-size: 20px;
    background: #000000;
    color: #00ff00;
    text-align: center;
    letter-spacing: 4px;
    font-family: 'Courier New', monospace;
    font-weight: bold;
    transition: all 0.3s ease;
    outline: none;
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.8);
}

input:focus {
    border-color: #ff0000;
    box-shadow:
        inset 0 0 10px rgba(0, 0, 0, 0.8),
        0 0 20px rgba(255, 0, 0, 0.3);
    background: #0a0a0a;
}

input::placeholder {
    color: #666666;
    letter-spacing: 2px;
}

button {
    padding: 18px 24px;
    background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%);
    color: #ffffff;
    border: 2px solid #ff0000;
    border-radius: 4px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    letter-spacing: 2px;
    font-family: 'Courier New', monospace;
    text-transform: uppercase;
    position: relative;
    overflow: hidden;
}

button::before {
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

button:hover:not(:disabled)::before {
    left: 100%;
}

button:hover:not(:disabled) {
    background: linear-gradient(135deg, #ff3333 0%, #ff0000 100%);
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
    transform: translateY(-2px);
}

button:active:not(:disabled) {
    transform: translateY(0);
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background: #666666;
    border-color: #666666;
}

.error {
    color: #ff0000;
    text-align: center;
    margin: 20px 0 0 0;
    font-size: 14px;
    padding: 16px;
    background: rgba(255, 0, 0, 0.1);
    border: 1px solid #ff0000;
    border-radius: 4px;
    font-weight: bold;
    letter-spacing: 1px;
    animation: shake 0.5s ease-in-out;
}

@keyframes shake {

    0%,
    100% {
        transform: translateX(0);
    }

    25% {
        transform: translateX(-5px);
    }

    75% {
        transform: translateX(5px);
    }
}

.attempts-warning {
    color: #ffaa00;
    text-align: center;
    font-size: 12px;
    margin-top: 16px;
    letter-spacing: 1px;
}

.loading-scanner {
    display: inline-block;
    width: 20px;
    height: 2px;
    background: #00ff00;
    animation: scanner 1s linear infinite;
}

@keyframes scanner {
    0% {
        transform: scaleX(0);
    }

    50% {
        transform: scaleX(1);
    }

    100% {
        transform: scaleX(0);
    }
}

/* Responsive design */
@media (max-width: 480px) {
    .pin-gate {
        margin: 16px;
        padding: 32px 24px;
    }

    h2 {
        font-size: 20px;
        letter-spacing: 2px;
    }

    input,
    button {
        padding: 16px 18px;
        font-size: 18px;
    }

    .danger-badge {
        font-size: 10px;
        padding: 6px 12px;
    }
}

@media (max-width: 320px) {
    .pin-gate {
        margin: 12px;
        padding: 24px 20px;
    }

    h2 {
        font-size: 18px;
    }

    input,
    button {
        padding: 14px 16px;
        font-size: 16px;
    }
}

/* Larger screens */
@media (min-width: 768px) {
    .pin-gate {
        padding: 48px 40px;
        max-width: 450px;
    }

    h2 {
        font-size: 28px;
        letter-spacing: 4px;
    }

    input,
    button {
        padding: 20px 24px;
        font-size: 22px;
    }
}
</style>
