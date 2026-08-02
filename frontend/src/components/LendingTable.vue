<template>
  <div class="p-4 card">
              <div class="flex justify-end mb-3">
            <button class="add-btn" @click="showAddPopup = true"><i class="fas fa-plus" style="color:black; margin-right:6px;"></i>
               Add</button>
          </div>
    <h2 class="text-xl font-bold mb-4"><i class="fas fa-hand-holding-usd" style="color:#6B4F3F; margin-right:6px;"></i>
      Lendings</h2>
    <table class="w-full border">
      <thead>
        <tr class="bg-gray-200">

          <th> To</th>
          <th>Amount</th>
          <th> Reason</th>
          <th> Date</th>
          <th> Status</th>
          <th> Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(lend, i) in lendings" :key="i">
          <td data-title="To">{{ lend.to_whom }}</td>
          <td data-title="Amount">{{ lend.amount }}</td>
          <td data-title="Reason">{{ lend.reason }}</td>
          <td data-title="Date">{{ lend.date }}</td>
          <td data-title="Status">{{ lend.returned ? "Returned" : "Pending" }}</td>
          <td data-title="Action">
            <Button v-if="!lend.returned" @click="markReturned(lend)" class="bg-green-500 text-white">
              <i class="fas fa-check" style="margin-right:4px;"></i>Mark Returned
            </Button>
          </td>
        </tr>
      </tbody>
    </table>

<!-- Add Lending Popup -->
<div v-if="showAddPopup" class="inner-popup">
  <div class="inner-popup-box">

    <button class="close-btn" @click="showAddPopup = false"><i class="fas fa-times" style="color:#6B4F3F"></i></button>

    <h3><i class="fas fa-plus-circle" style="color:#6B4F3F; margin-right:6px;"></i>Add New Lending</h3>

    <input v-model="to_whom" placeholder="To whom" class="input" />
    <input v-model.number="amount" type="number" placeholder="Amount" class="input" />
    <input v-model="reason" placeholder="Reason" class="input" />

    <button class="submit-btn" @click="addNewLending"><i class="fas fa-check-circle" style="color:#6B4F3F; margin-right:6px;"></i>
      Add</button>

  </div>
</div>

    
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const props = defineProps({
  username: {
    type: String,
    required: true
  }
})

const emit = defineEmits(["refresh"]);

const Username = props.username
const lendings = ref([]);
const to_whom = ref("");
const amount = ref("");
const reason = ref("");
const showAddPopup = ref(false);


// ✅ Fetch existing lendings
async function loadLendings() {
  if (!Username) return;
  const res = await axios.get(`/api/lending/get/${Username}`);
  lendings.value = res.data.lendings || [];
}

// ✅ Add new lending
async function addNewLending() {
  const res = await axios.post("/api/lending/add", {
    username: Username,
    amount: Number(amount.value),
    to_whom: to_whom.value,
    reason: reason.value
  });
  lendings.value.push(res.data.lending);
  to_whom.value = amount.value = reason.value = "";
  emit("refresh");
  showAddPopup.value = false;
}

// ✅ Mark lending as returned
async function markReturned(lend) {
  await axios.post("/api/lending/mark-returned", {
    username: Username,
    to_whom: lend.to_whom
  });
  lend.returned = true;
  emit("refresh");
}

onMounted(loadLendings);
</script>


<style scoped>
/* Lending Table Component */
.p-4 {
  padding: 20px;
  box-sizing: border-box;
}

.text-xl {
  font-size: 26px;
}

.font-bold {
  font-weight: 700;
}

.mb-4 {
  margin-bottom: 25px;
}

.mt-4 {
  margin-top: 25px;
}

.flex {
  display: flex;
}

.gap-2 {
  gap: 12px;
}

.w-full {
  width: 100%;
}

.border {
  border: 2px solid #d4a574;
}

.p-2 {
  padding: 14px 18px;
}

.bg-gray-200 {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
}

.bg-green-500 {
  background: linear-gradient(135deg, #6b8e23 0%, #556b2f 100%);
}

.bg-blue-500 {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
}

.text-white {
  color: #f5e6d3;
}

/* Card (reusing from main dashboard) */
.p-4.card,
.p-4 {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(107, 68, 35, 0.2);
  border: 3px solid #d4a574;
  overflow-x: auto; /* allow horizontal scroll if needed */
}

/* Lending Table Heading */
.p-4 h2 {
  font-size: 26px;
  font-weight: 700;
  color: #6b4423;
  margin-bottom: 25px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.05);
}

/* Lending Table */
.p-4 table {
  width: 100%;
  border-collapse: collapse;
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(107, 68, 35, 0.15);
  border: 2px solid #d4a574;
}

.p-4 thead {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
}

.p-4 th {
  padding: 16px 14px;
  text-align: left;
  color: #f5e6d3;
  font-weight: 700;
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.p-4 tbody tr {
  border-bottom: 2px solid #e8d5c0;
  transition: all 0.3s ease;
}

.p-4 tbody tr:last-child {
  border-bottom: none;
}

.p-4 tbody tr:hover {
  background: rgba(212, 165, 116, 0.15);
  transform: scale(1.01);
}

.p-4 td {
  padding: 16px 14px;
  color: #5a4235;
  font-size: 15px;
  font-weight: 500;
}

.p-4 td:nth-child(4) {
  white-space: normal;
  word-break: break-word;
  min-width: 100px;
  line-height: 1.3;
}

/* Status styling */
.p-4 td:nth-child(5) {
  font-weight: 700;
}

/* Button in table */
.p-4 table button {
  background: linear-gradient(135deg, #6b8e23 0%, #556b2f 100%);
  color: #f5e6d3;
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(107, 142, 35, 0.3);
  font-family: 'Quicksand', sans-serif;
}

.p-4 table button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(107, 142, 35, 0.45);
  background: linear-gradient(135deg, #556b2f 0%, #3d4f1f 100%);
}

.p-4 table button:active {
  transform: translateY(0);
}

/* Input Form Section */
.p-4 .flex {
  display: flex;
  gap: 12px;
  margin-top: 25px;
  flex-wrap: wrap;
}

.p-4 input {
  flex: 1;
  min-width: 150px;
  padding: 14px 0px;
  border: 2px solid #d4a574;
  border-radius: 12px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.95);
  color: #4a3728;
  font-family: 'Quicksand', sans-serif;
  font-weight: 500;
  transition: all 0.3s ease;
}


.p-4 input:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 4px rgba(139, 90, 60, 0.15);
  background: #ffffff;
}

.p-4 input::placeholder {
  color: #a88763;
}

/* Add Button */
.p-4 .flex button {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(107, 68, 35, 0.35);
  font-family: 'Quicksand', sans-serif;
  white-space: nowrap;
}

.p-4 .flex button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(107, 68, 35, 0.5);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.p-4 .flex button:active {
  transform: translateY(-1px);
}

/* Popup */
.inner-popup {
  position: fixed;
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.55);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100000 !important;
}

.inner-popup-box {
  background: #fffaf2;
  padding: 35px 30px;
  border-radius: 20px;
  width: 400px;
  max-width: 95%;
  box-shadow: 0 12px 40px rgba(0,0,0,0.45);
  border: 3px solid #8b5a3c;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: popupIn 0.3s ease;
}

@keyframes popupIn {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.inner-popup-box h3 {
  font-size: 26px;
  font-weight: 700;
  color: #6b4423;
  text-align: center;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.05);
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: #8b5a3c;
  color: #f5e6d3;
  border: none;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 10px rgba(0,0,0,0.25);
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #6b4423;
  transform: rotate(90deg) scale(1.1);
  box-shadow: 0 4px 15px rgba(0,0,0,0.35);
}

.input {
  padding: 14px 18px;
  font-size: 16px;
  border-radius: 12px;
  border: 2px solid #d4a574;
  background: rgba(255,255,255,0.95);
  color: #4a3728;
  font-weight: 500;
  transition: all 0.3s ease;
}

.input:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 4px rgba(139,90,60,0.15);
  background: #ffffff;
}

.submit-btn {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(107,68,35,0.45);
  width: 100%;
}

.submit-btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 25px rgba(107,68,35,0.55);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.submit-btn:active {
  transform: translateY(0);
}

/* Responsive Design */
@media (max-width: 968px) {
  .p-4 {
    padding: 20px;
  }

  .p-4 table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
  }

  .p-4 th,
  .p-4 td {
    padding: 12px 10px;
    font-size: 14px;
  }

  .p-4 table button {
    padding: 8px 14px;
    font-size: 13px;
  }
}

@media (max-width: 768px) {
  .p-4 h2 {
    font-size: 22px;
    margin-bottom: 20px;
  }

  .p-4 .flex {
    flex-direction: column;
    gap: 12px;
  }

  .p-4 input {
    width: 100%;
    min-width: 100%;
  }

  .p-4 .flex button {
    width: 100%;
    padding: 16px 28px;
  }
}

@media (max-width: 480px) {
  .p-4 h2 {
    font-size: 20px;
  }

  .inner-popup-box {
    padding: 25px 20px;
    width: 90%;
  }

  .inner-popup-box h3 {
    font-size: 22px;
  }

  .input {
    font-size: 15px;
    padding: 12px 14px;
  }

  .submit-btn {
    font-size: 15px;
    padding: 12px 20px;
  }
}

@media (max-width: 380px) {
  .p-4 input {
    font-size: 14px;
    padding: 12px 14px;
  }

  .p-4 .flex button {
    font-size: 14px;
    padding: 12px 20px;
  }
}

</style>