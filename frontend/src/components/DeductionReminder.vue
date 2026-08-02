<template>
  <div class="deduction-reminder">
    <p>Pending Deduction: {{ pending }}</p>
    <input type="number" v-model.number="paid" />
    <button @click="$emit('pay', paid)">Pay</button>
  </div>
</template>

<script>
export default {
  props: ["pending"],
  data() {
    return { paid: 0 };
  },
};
</script>

<style scoped>
.deduction-reminder {
  background: linear-gradient(145deg, #fff9f0 0%, #f5e6d3 100%);
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 6px 20px rgba(107, 68, 35, 0.25);
  border: 3px solid #d4a574;
  margin-bottom: 25px;
  transition: all 0.3s ease;
}

.deduction-reminder:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(107, 68, 35, 0.35);
}

.deduction-reminder p {
  font-size: 18px;
  font-weight: 600;
  color: #6b4423;
  margin-bottom: 18px;
  line-height: 1.6;
}

.deduction-reminder input[type="number"] {
  width: 100%;
  padding: 14px 18px;
  margin-bottom: 16px;
  border: 2px solid #d4a574;
  border-radius: 12px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.95);
  color: #4a3728;
  font-family: 'Quicksand', sans-serif;
  font-weight: 500;
  transition: all 0.3s ease;
}

.deduction-reminder input[type="number"]:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 4px rgba(139, 90, 60, 0.15);
  background: #ffffff;
}

.deduction-reminder input[type="number"]::placeholder {
  color: #a88763;
}

.deduction-reminder button {
  width: 100%;
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(107, 68, 35, 0.35);
  font-family: 'Quicksand', sans-serif;
}

.deduction-reminder button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(107, 68, 35, 0.5);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.deduction-reminder button:active {
  transform: translateY(-1px);
}

/* Responsive */
@media (max-width: 768px) {
  .deduction-reminder {
    padding: 22px;
  }

  .deduction-reminder p {
    font-size: 16px;
  }
}
</style>