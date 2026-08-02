<template>
  <div class="page-root">
    <button class="floating-btn" @click="toggleFabMenu">
      <i class="fas fa-bars"></i>
    </button>
    <Sidebar :username="username"/>
    <main class="main-area">
      <div class="dashboard">

        <!-- Net card -->
        <div class="left-panel">
          <div class="card">
            <h3>This month ({{ month }})</h3>
            <div v-if="monthData">
              <p>Total Income: ₹{{ monthData.income_base ?? 0 }}</p>


              <p><strong>Savings: ₹{{ monthData.savings ?? 0 }}</strong></p>
              <button @click="openExpenseModal">Add Expense</button>

            </div>

            <div v-else>
              <p>No month setup yet. You should see an income modal if this is a new month.</p>
            </div>
          </div>
        </div>

        <div class="right-panel">
          <ExpenseTable v-if="monthData && monthData.expenses" :expenses="monthData.expenses" @edit="openEditExpense"
            @delete="deleteExpense" />
        </div>



      </div>


      <div v-if="fabMenuOpen" class="fab-menu">

        <button class="fab-option" @click="showLendingPopup = true">
          Lending
        </button>
        <!-- <div v-if="monthData?.deduction_enabled">
          <button class="fab-option" @click="openDeductionModal">Deduction</button>
        </div> -->

      </div>
      <!-- Income modal -->
      <div class="modal" v-if="showIncomeModal">
        <div class="modal-inner">
          <h3>Enter this month's income</h3>
          <input v-model="incomeInput" placeholder="Enter monthly income" />
          <input v-model="incomeCategory" type="text" placeholder="Category (e.g. Salary, Freelance)" />

          <!-- Deduction toggle -->
          <!-- <div class="toggle-row">
            <label><input type="checkbox" v-model="enableDeduction" /> Enable 2.5% Deduction</label>
          </div> -->
          <div class="actions">
            <button @click="submitIncome">Save</button>
            <button @click="closeIncomeModal">Cancel</button>
          </div>
          <p v-if="modalError" class="error">{{ modalError }}</p>
        </div>
      </div>

      <!-- Deduction modal -->
      <!-- <div class="modal" v-if="showDeductionModal">
        <div class="modal-inner">
          <h3>Deduction (2.5%)</h3>
          <p>Total Deduction: ₹{{ monthData?.deductions?.total ?? 0 }}</p>
          <p>Paid: ₹{{ monthData?.deductions?.paid ?? 0 }}</p>
          <p>Remaining: ₹{{ monthData?.deductions?.remaining ?? 0 }}</p>

          <input v-model="deductionPayment" placeholder="Enter amount to pay" type="number" min="0" />
          <div class="actions">
            <button @click="submitDeductionPayment">Pay</button>
            <button @click="closeDeductionModal">Close</button>
          </div>
          <p v-if="deductionError" class="error">{{ deductionError }}</p>
        </div>
      </div> -->

      <!-- Add inside Dashboard.vue template -->
      <!-- Add/Edit Expense Modal -->
      <div class="modal" v-if="showExpenseModal">
        <div class="modal-inner">
          <h3>{{ editingIndex !== null ? 'Edit Expense' : 'Add Expense' }}</h3>
          <input v-model="expenseAmount" placeholder="Amount" type="number" />
          <input v-model="expenseCategory" placeholder="Category" type="text" />
          <div class="actions">
            <button @click="saveExpense">Save</button>
            <button @click="closeExpenseModal">Cancel</button>
          </div>
          <p v-if="expenseError" class="error">{{ expenseError }}</p>
        </div>
      </div>


      <!-- raw debug -->
      <!-- <pre>{{ monthData }}</pre> -->
      <!-- Lending Overlay -->
      <div v-if="showLendingPopup" class="overlay">
        <div class="overlay-inner">
          <button class="close-btn" @click="showLendingPopup = false">✖</button>
          <LendingTable :username="username" @refresh="fetchMonth" />
        </div>
      </div>


      <!-- Delete Confirmation Modal -->
      <div class="modal" v-if="showDeleteConfirm">
        <div class="modal-inner">
          <h3>Delete Expense?</h3>
          <p>Are you sure you want to delete this expense?</p>

          <div class="actions">
            <button class="danger" @click="confirmDelete">Yes, Delete</button>
            <button @click="cancelDelete">Cancel</button>
          </div>
        </div>
      </div>


      <!-- Reminder Popup -->
      <div v-if="showReminderPopup" class="overlay">
        <div class="overlay-inner text-center">
          <h3>Lending Reminder ⚠️</h3>
          <p>You have pending lendings that should be returned soon!</p>
          <button class="btn" @click="showReminderPopup = false">Got it</button>
        </div>
      </div>


    </main>
  </div>
</template>

<script>
import axios from "axios";
import ExpenseTable from "../components/ExpenseTable.vue";
import LendingTable from "../components/LendingTable.vue";
import Sidebar from "../components/Sidebar.vue";
export default {
  name: "Dashboard",
  components: { ExpenseTable, LendingTable, Sidebar },

  data() {
    return {
      showDeleteConfirm: false,
      deleteIndex: null,
      username: "",
      month: "",
      monthData: null,
      showIncomeModal: false,
      showDeductionModal: false,
      showReminderPopup: false,
      incomeInput: "",
      incomeCategory: "",
      enableDeduction: false,
      modalError: "",
      showExpenseModal: false,
      showLendingPopup: false,
      expenseAmount: "",
      expenseCategory: "",
      expenseError: "",
      deductionPayment: "",
      deductionError: "",
      editingIndex: null,
      fabMenuOpen: false
    };
  },
  async mounted() {

    const localData = JSON.parse(localStorage.getItem("user") || "{}");
    // adjust key name if you stored it differently

    // no local data at all → go back to login
    if (!localData || !localData.join_date) {
      this.$router.push("/");
      return;
    }


    // 1) Check current month status
    try {
      // Ask backend which user has this join_date
      const response = await axios.get("/api/find_by_join_date", {
        params: { join_date: localData.join_date }
      });

      if (!response.data.ok || !response.data.username) {
        this.$router.push("/");
        return;
      }

      this.username = response.data.username; // now username is set
      const resp = await axios.get("/api/monthly/check", { params: { username: this.username } });
      if (!resp.data.ok) {
        console.error("Check error", resp.data);
        return;
      }

      this.month = resp.data.month;
      if (resp.data.new_month) {
        // new month -> show income modal
        this.showIncomeModal = true;
      } else {
        // load existing month data
        await this.fetchMonth();
      }
    } catch (err) {
      console.error(err);
    }
        await this.CheckIncomeBaseForPresentMonth();
    await this.checkLendingReminders();
  },
  methods: {
    toggleFabMenu() {
      this.fabMenuOpen = !this.fabMenuOpen;
    },
    openExpenseModal() {
      this.showExpenseModal = true;
      this.editingIndex = null;
      this.expenseAmount = "";
      this.expenseCategory = "";
    },
    openEditExpense(index, expense) {
      this.showExpenseModal = true;
      this.editingIndex = index;
      this.expenseAmount = expense.amount;
      this.expenseCategory = expense.category;
    },
    closeExpenseModal() {
      this.showExpenseModal = false;
    },
    async fetchMonth() {
      try {
        const resp = await axios.get("/api/monthly/get", { params: { username: this.username } });
        if (resp.data.ok) {
          this.monthData = resp.data.month_data;
        } else {
          this.monthData = null;
        }
      } catch (err) {
        console.error(err);
      }
    },
    // openDeductionModal() {
    //   this.showDeductionModal = true;
    // },
    // closeDeductionModal() {
    //   this.showDeductionModal = false;
    // },
    async closeIncomeModal() {
      const resp = await axios.get("/api/monthly/get", {
       params: { username: this.username }
      });

      if (resp.data.ok) {
       this.monthData = resp.data.month_data;
      }
      if (!this.monthData || !this.monthData.income_base || this.monthData.income_base === 0) {
       this.modalError = "You must enter income to continue.";

       return;
     }
      this.showIncomeModal = false;
    },

    async CheckIncomeBaseForPresentMonth(){
    const resp = await axios.get("/api/monthly/get", {
    params: { username: this.username }
      });

      if (resp.data.ok) {
       this.monthData = resp.data.month_data;
      }
      if (!this.monthData || !this.monthData.income_base || this.monthData.income_base === 0) {
         this.showIncomeModal = true;

         return;
     }
    },


    async submitIncome() {
      this.modalError = "";
      const income = this.incomeInput;
      const category = this.incomeCategory || "Salary";
      if (!income || isNaN(Number(income))) {
        this.modalError = "Please enter a valid numeric income.";
        return;
      }
      try {
        const resp = await axios.post("/api/monthly/setup", {
          username: this.username,
          income: Number(income),
          category,
          enable_deduction: this.enableDeduction
        });
        if (resp.data.ok) {
          this.monthData = resp.data.month_data;
          this.showIncomeModal = false;
          // after setup, open deduction modal automatically
          if (this.enableDeduction) {
            this.showDeductionModal = true;
          }
        } else {
          this.modalError = resp.data.error || "Failed to save income";
        }
      } catch (err) {
        console.error(err);
        this.modalError = "Network or server error";
      }
    },


    async saveExpense() {
      this.expenseError = "";
      const amount = Number(this.expenseAmount);
      const category = this.expenseCategory.trim();

      if (!amount || !category) {
        this.expenseError = "Enter valid amount and category.";
        return;
      }

      try {
        let url = "/api/expense/add-expense";
        let payload = { username: this.username, amount, category };

        if (this.editingIndex !== null) {
          url = "/api/expense/edit";
          payload.index = this.editingIndex;
        }

        const resp = await axios.post(url, payload);
        if (resp.data.ok) {
          this.monthData = resp.data.month_data;
          await this.fetchMonth();
          this.closeExpenseModal();
        } else {
          this.expenseError = resp.data.error || "Failed to save expense";
        }
      } catch (err) {
        console.error(err);
        this.expenseError = "Network/server error";
      }
    },

    deleteExpense(index) {
      this.deleteIndex = index;
      this.showDeleteConfirm = true;
    },


    async confirmDelete() {
      try {
        const resp = await axios.post("/api/expense/delete", {
          username: this.username,
          index: this.deleteIndex
        });

        if (resp.data.ok) {
          await this.fetchMonth();
        }
      } catch (err) {
        console.error(err);
      }

      this.showDeleteConfirm = false;
      this.deleteIndex = null;
    },

    cancelDelete() {
      this.showDeleteConfirm = false;
      this.deleteIndex = null;
    },


    async submitDeductionPayment() {
      this.deductionError = "";
      const amount = parseFloat(this.deductionPayment);
      if (!amount || amount <= 0) {
        this.deductionError = "Enter a valid amount";
        return;
      }

      try {
        const resp = await axios.post("/api/deduction/pay", { username: this.username, amount });
        if (resp.data.ok) {
          this.monthData = resp.data.month_data;
          this.deductionPayment = "";
        } else {
          this.deductionError = resp.data.error || "Failed to pay deduction";
        }
      } catch (err) {
        console.error(err);
        this.deductionError = "Network/server error";
      }
    },

    async checkLendingReminders() {
      try {
        const res = await axios.get(`/api/lending/get/${this.username}`);
        const lendings = res.data.lendings || [];
        const pending = lendings.filter(l => !l.returned);

        if (pending.length === 0) return;

        const today = new Date();
        const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
        const diff = (lastDay - today) / (1000 * 60 * 60 * 24);

        if (diff <= 5) this.showReminderPopup = true;
      } catch (err) {
        console.error("Failed to check lending reminders", err);
      }
    },


  }
};
</script>

<style scoped>
body {
  box-sizing: border-box;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Quicksand', sans-serif;
}

/* Page Root */
.page-root {
  margin-top: 30PX;
  display: flex;
  width: 100%;
  min-height: 100%;
  background: linear-gradient(135deg, #f5e6d3 0%, #e8d5c0 100%);
}

/* Main Area */
.main-area {
  flex: 1;
  padding-left: 250px;
  overflow-y: auto;
  background: transparent;
}

/* Dashboard */
.dashboard {
  display: flex;
  gap: 10px;
  align-items: stretch;
  margin-top: 20px;
  max-width: 1200px;
  margin: 0 auto;
   min-height: 400px; 
}

.left-panel {
  flex: 1;
  min-width: 280px;
  display: flex;
  flex-direction: column;
}

/* Right Panel = Expense Table */
.right-panel {
  flex: 2;
  overflow-y: auto;
  max-height: 418px; 
  overflow-x: auto;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.left-panel>*,
.right-panel>* {
  height: 100%;
}


/* Card */
.card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 35px;
  box-shadow: 0 8px 30px rgba(107, 68, 35, 0.2);

  border: 3px solid #d4a574;
}

.card h3 {
  font-size: 26px;
  font-weight: 700;
  color: #6b4423;
  margin-bottom: 25px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.05);
}

.card p {
  font-size: 17px;
  margin-bottom: 14px;
  color: #5a4235;
  line-height: 1.7;
}

.card p strong {
  color: #6b4423;
  font-weight: 700;
  font-size: 19px;
}

.card button {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 15px;
  margin-right: 12px;
  box-shadow: 0 4px 15px rgba(107, 68, 35, 0.3);
}

.card button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(107, 68, 35, 0.45);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.card button:active {
  transform: translateY(-1px);
}

/* Modal - Centered Popup with Overlay */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(74, 55, 40, 0.88);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
  backdrop-filter: blur(4px);
}
.modal-inner h3 {
  margin-bottom: 10px;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.actions .danger {
  background: #e53935;
  color: white;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.modal-inner {
  background: linear-gradient(145deg, #fff9f0 0%, #f5e6d3 100%);
  border-radius: 24px;
  padding: 40px;
  max-width: 520px;
  width: 90%;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5);
  border: 4px solid #8b5a3c;
  animation: slideDown 0.4s ease;
  max-height: 90vh;
  overflow-y: auto;
}

@keyframes slideDown {
  from {
    transform: translateY(-60px) scale(0.95);
    opacity: 0;
  }

  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.modal-inner h3 {
  font-size: 28px;
  font-weight: 700;
  color: #6b4423;
  margin-bottom: 28px;
  text-align: center;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

.modal-inner input {
  width: 100%;
  padding: 16px 20px;
  margin-bottom: 20px;
  border: 2px solid #d4a574;
  border-radius: 12px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.95);
  color: #4a3728;
  transition: all 0.3s ease;
  font-weight: 500;
}

.modal-inner input:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 4px rgba(139, 90, 60, 0.15);
  background: #ffffff;
}

.modal-inner input::placeholder {
  color: #a88763;
}

.modal-inner p {
  font-size: 17px;
  margin-bottom: 14px;
  color: #5a4235;
  line-height: 1.7;
}

/* Toggle Row */
.toggle-row {
  margin: 22px 0;
  padding: 18px;
  background: rgba(212, 165, 116, 0.2);
  border-radius: 12px;
  border: 2px solid #e8d5c0;
}

.toggle-row label {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  color: #5a4235;
  cursor: pointer;
  font-weight: 600;
}

.toggle-row input[type="checkbox"] {
  width: 22px;
  height: 22px;
  cursor: pointer;
  accent-color: #8b5a3c;
}

/* Actions */
.actions {
  display: flex;
  gap: 14px;
  margin-top: 28px;
  justify-content: center;
}

.actions button {
  flex: 1;
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  padding: 16px 28px;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(107, 68, 35, 0.35);
}

.actions button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(107, 68, 35, 0.5);
}

.actions button:last-child {
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}


/* Error */
.error {
  color: #c44536;
  font-weight: 700;
  margin-top: 18px;
  text-align: center;
  padding: 14px;
  background: rgba(196, 69, 54, 0.12);
  border-radius: 10px;
  border: 2px solid rgba(196, 69, 54, 0.3);
}

/* FAB Menu wrapper */
.fab-menu {
  position: fixed;
  bottom: 90px;
  right: 80px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 9999;
  animation: fadeIn 0.3s ease;
}

/* Sub-buttons */
.fab-option {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  padding: 12px 20px;
  border-radius: 14px;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(107, 68, 35, 0.45);
  transition: all 0.3s ease;
  border: 2px solid #d4a574;
}

.fab-option:hover {
  transform: translateX(-6px);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

/* Floating Button */
.floating-btn {
  position: fixed;
  bottom: 30px;
  right: 40px;
  width: 65px;
  height: 65px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: 4px solid #d4a574;
  font-size: 34px;
  cursor: pointer;
  box-shadow: 0 8px 25px rgba(107, 68, 35, 0.45);
  transition: all 0.4s ease;
  z-index: 1050;
}

.floating-btn:hover {
  transform: scale(1.15) rotate(15deg);
  box-shadow: 0 10px 35px rgba(107, 68, 35, 0.6);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.floating-btn:active {
  transform: scale(1.05) rotate(10deg);
}

/* Overlay - Centered Popup */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(74, 55, 40, 0.88);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999 !important;
  animation: fadeIn 0.3s ease;
  backdrop-filter: blur(4px);
}

.overlay-inner {
  background: linear-gradient(145deg, #fff9f0 0%, #f5e6d3 100%);
  border-radius: 24px;
  padding: 40px;
  max-width: 750px;
  width: 90%;
  max-height: 88vh;
  overflow-y: auto;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5);
  border: 4px solid #8b5a3c;
  position: relative;
  animation: slideDown 0.4s ease;
}

.overlay-inner h3 {
  font-size: 28px;
  font-weight: 700;
  color: #6b4423;
  margin-bottom: 22px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

.overlay-inner p {
  font-size: 17px;
  color: #5a4235;
  margin-bottom: 22px;
  line-height: 1.7;
}

/* Close Button */
.close-btn {
  position: absolute;
  top: 18px;
  right: 18px;
  background: #8b5a3c;
  color: #f5e6d3;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 22px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.25);
  font-weight: 700;
}

.close-btn:hover {
  background: #6b4423;
  transform: rotate(90deg) scale(1.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
}

/* Text Center */
.text-center {
  text-align: center;
}

/* Button */
.btn {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  padding: 16px 36px;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(107, 68, 35, 0.35);
}

.btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(107, 68, 35, 0.5);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.btn:active {
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 1079px) {
  .main-area {
    padding-left: 0px !important;
    flex-direction: column;

  }

  .left-panel {
    min-width: 100% !important;
    width: 100% !important;
  }

  .right-panel {
    width: 100% !important;
    min-width: 100% !important;
    overflow:hidden !important;
    
  }

  .right-panel table {
    width: 100% !important;
    display: block;
    overflow-x: auto;
    max-height: 300px;
    /* Only scroll table content if too big */
  }

  .dashboard {
    flex-direction: column;
    width: 100% !important;
  }

  .dashboard>h2 {
    font-size: 28px;
  }

  .card {
    padding: 25px;
  }

  .modal-inner,
  .overlay-inner {
    padding: 28px;
    width: 95%;
  }

  .floating-btn {
    width: 65px;
    height: 65px;
    font-size: 30px;
    bottom: 25px;
    right: 25px;
  }

  .actions {
    flex-direction: column;
  }
}
</style>
