<template>
  <div class="history-page">
    <Sidebar :username="username" />
    <!-- Filters -->
    <div class="filters">
      <i class="fas fa-calendar-alt filter-icon"></i>
      <select v-model="selectedYear">
        <option disabled value="">Select year</option>
        <option v-for="y in years" :key="y">{{ y }}</option>
      </select>

      <select v-model="selectedMonth">
        <option disabled value="">Select month</option>
        <option v-for="(m, i) in months" :key="i" :value="i + 1">
          {{ m }}
        </option>
      </select>

      <button @click="fetchHistory"><i class="fas fa-search"></i>Show</button>
    </div>
    <p v-if="errorMsg" class="error-box"><i class="fas fa-exclamation-circle"></i>{{ errorMsg }}</p>
    <div v-if="loading" class="loading"><i class="fas fa-spinner fa-spin"></i>Loading...</div>


    <div v-if="historyData" class="history-content">

      <div v-if="historyData.exists" class="history-grid">

        <!-- LEFT CARD -->
        <div class="summary-card">
          <h4><i class="fas fa-chart-pie" style="color:#6B4F3F;"></i>Summary</h4>
          <h3><i class="fas fa-calendar" style="color:#6B4F3F;"></i>{{ months[selectedMonth - 1] }} {{ selectedYear }}</h3>
          <p><strong><i class="fas fa-wallet black-icon"></i>Income:</strong> ₹{{ historyData.income }}</p>
          <p><strong><i class="fas fa-piggy-bank black-icon"></i>Savings:</strong> ₹{{ historyData.savings }}</p>

          <button class="download-btn" @click="generatePDF"><i class="fas fa-file-download"></i>Download PDF</button>

        </div>

        <!-- RIGHT CARD -->
        <div class="table-card">
          <h4><i class="fas fa-receipt" style="color:#6B4F3F;"></i>Expenses</h4>

          <div class="table-wrapper">
            <table class="history-table">
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(ex, i) in historyData.expenses" :key="i">
                  <td>{{ ex.category }}
                    <div class="date-label">{{ ex.datetime }}</div>
                  </td>
                  <td>{{ ex.amount }}</td>

                </tr>
              </tbody>
            </table>
          </div>

        </div>

      </div>

      <div v-else>
        <p><i class="fas fa-info-circle black-icon"></i>No data exists for this month.</p>
      </div>
    </div>


  </div>
</template>


<script>
import axios from "axios";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

import Sidebar from "../components/Sidebar.vue";

export default {
  name: "HistoryPage",
  components: { Sidebar },
  data() {
    return {
      years: [],
      months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      selectedYear: "",
      selectedMonth: "",
      historyData: null,
      username: "",
      loading: false,
    };
  },

  async mounted() {
    const local = JSON.parse(localStorage.getItem("user") || "{}");
    const resp = await axios.get("/api/find_by_join_date", { params: { join_date: local.join_date } });
    this.username = resp.data.username;

    const joinYear = new Date(local.join_date).getFullYear();
    const currentYear = new Date().getFullYear();
    this.years = [];
    for (let y = joinYear; y <= currentYear; y++) {
      this.years.push(y);
    }
  },

  methods: {
    async fetchHistory() {
      if (!this.selectedYear || !this.selectedMonth) return;
      this.loading = true;

      const resp = await axios.get("/api/history/month", {
        params: {
          username: this.username,
          year: this.selectedYear,
          month: this.selectedMonth
        }
      });

      this.historyData = resp.data;
      this.loading = false;
    },

generatePDF() {
  if (!this.historyData) return;

  const doc = new jsPDF("p", "pt", "a4");
  const marginLeft = 40;
  const pageWidth = doc.internal.pageSize.getWidth();

  const monthName = this.months[this.selectedMonth - 1];

  // Title
  doc.setFontSize(20);
  doc.text(`${monthName} ${this.selectedYear} Monthly Report`, pageWidth / 2, 60, { align: "center" });

  // Header small info
  doc.setFontSize(12);
  doc.text(`Income: ${this.historyData.income}`, marginLeft, 90);
  doc.text(`Savings: ${this.historyData.savings}`, marginLeft, 110);

  // TABLE
  const tableData = this.historyData.expenses.map((ex) => [
    ex.category,
    String(ex.amount),
    ex.datetime
  ]);

  autoTable(doc, {
    startY: 140,
    head: [["Category", "Amount", "Date"]],
    body: tableData,
    styles: { fontSize: 11 },
    headStyles: { fillColor: [139, 90, 60] }
  });

  doc.save(`History_${monthName}_${this.selectedYear}.pdf`);
}





  }
};
</script>

<style scoped>
/* History Page Container */

.history-page {
  margin-left: 250px; /* Space for sidebar on desktop */
  padding: 40px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5e6d3 0%, #e8d5c0 100%);
  font-family: 'Quicksand', sans-serif;
  transition: margin-left 0.3s ease;
}

/* Filters Section */
.filters {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 8px 30px rgba(107, 68, 35, 0.2);
  border: 3px solid #d4a574;
  margin-bottom: 30px;
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  align-items: center;
}

/* Filter Icon */
.filter-icon {
  font-size: 28px;
  color: #8b5a3c;
  margin-right: 5px;
}

/* Select dropdowns */
.filters select {
  flex: 1;
  min-width: 180px;
  padding: 16px 20px;
  border: 3px solid #d4a574;
  border-radius: 14px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.95);
  color: #4a3728;
  font-family: 'Quicksand', sans-serif;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236b4423' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  padding-right: 40px;
  background-position: right 12px center;

}

.filters select:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 4px rgba(139, 90, 60, 0.2);
  background-color: #ffffff;
}

.filters select:hover {
  border-color: #8b5a3c;
}

.filters select option {
  padding: 12px;
  background: #ffffff;
  color: #4a3728;
}

/* Show button */
.filters button {
  padding: 16px 32px;
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  border-radius: 14px;
  font-size: 17px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 18px rgba(107, 68, 35, 0.35);
  font-family: 'Quicksand', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 10px;
}

.filters button i {
  font-size: 18px;
}

.filters button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(107, 68, 35, 0.5);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.filters button:active {
  transform: translateY(-1px);
}
.filters,
.filters * {
  box-sizing: border-box;
}


/* Error Box */
.error-box {
  background: rgba(196, 69, 54, 0.15);
  border: 3px solid rgba(196, 69, 54, 0.4);
  border-radius: 16px;
  padding: 18px 24px;
  color: #c44536;
  font-weight: 700;
  font-size: 17px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 12px;
  animation: shake 0.4s ease;
}

.error-box i {
  font-size: 22px;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

/* Loading state */
.loading {
  font-size: 20px;
  color: #8b5a3c;
  font-weight: 700;
  text-align: center;
  padding: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  border: 3px solid #d4a574;
  box-shadow: 0 8px 30px rgba(107, 68, 35, 0.2);
}

.loading i {
  font-size: 24px;
}

/* History Content Container */
.history-content {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* History Grid - Two Columns */
.history-grid {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 30px;
  align-items: start;
}

/* Summary Card (Left) */
.summary-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 249, 240, 0.95) 100%);
  border-radius: 20px;
  padding: 35px;
  box-shadow: 0 8px 30px rgba(107, 68, 35, 0.25);
  border: 3px solid #d4a574;
  position: sticky;
  top: 20px;
}

.summary-card h4 {
  font-size: 22px;
  font-weight: 700;
  color: #6b4423;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 12px;
  border-bottom: 3px solid #e8d5c0;
}

.summary-card h4 i {
  font-size: 24px;
}

.summary-card h3 {
  font-size: 26px;
  font-weight: 800;
  color: #8b5a3c;
  margin-bottom: 25px;
  text-shadow: 1px 1px 2px rgba(107, 68, 35, 0.1);
  display: flex;
  align-items: center;
  gap: 10px;
}

.summary-card h3 i {
  font-size: 26px;
}

.summary-card p {
  font-size: 18px;
  margin-bottom: 18px;
  color: #5a4235;
  line-height: 1.7;
  padding: 14px 20px;
  background: rgba(212, 165, 116, 0.12);
  border-radius: 12px;
  border-left: 4px solid #8b5a3c;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.summary-card p:hover {
  background: rgba(212, 165, 116, 0.22);
  transform: translateX(5px);
}

.summary-card p strong {
  color: #6b4423;
  font-weight: 700;
  font-size: 19px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.black-icon {
  color: #000000 !important;
  font-size: 18px;
}

/* Download Button */
.download-btn {
  width: 100%;
  margin-top: 25px;
  padding: 16px 28px;
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  border-radius: 14px;
  font-size: 17px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 18px rgba(107, 68, 35, 0.35);
  font-family: 'Quicksand', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.download-btn i {
  font-size: 20px;
}

.download-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(107, 68, 35, 0.5);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.download-btn:active {
  transform: translateY(-1px);
}

/* Table Card (Right) */
.table-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 35px;
  box-shadow: 0 8px 30px rgba(107, 68, 35, 0.2);
  border: 3px solid #d4a574;
  max-height: 400px;
}

.table-card h4 {
  font-size: 24px;
  font-weight: 700;
  color: #6b4423;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 15px;
  border-bottom: 3px solid #e8d5c0;
}

.table-card h4 i {
  font-size: 26px;
}

/* Table Wrapper */
.table-wrapper {
    flex: 1 1 auto !important;    
     max-height: 300px !important; /* take remaining space inside .table-card */   /* <- critical: enables inner scrolling in flex layouts */          /* default; overridden in media queries */
  overflow-x: auto !important;  /* horizontal scroll (keeps your current behavior) */
  overflow-y: auto !important;
  border-radius: 12px;
}

/* History Table */
.history-table {
  width: 100%;
  height: 100%;
  border-collapse: collapse;
  background: #ffffff;
  border-radius: 12px;
  overflow-y: auto !important;
  box-shadow: 0 4px 16px rgba(107, 68, 35, 0.15);
  border: 2px solid #d4a574;
}

.history-table thead {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
}

.history-table th {
  padding: 18px 16px;
  text-align: left;
  color: #f5e6d3;
  font-weight: 700;
  font-size: 17px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.history-table tbody tr {
  border-bottom: 2px solid #e8d5c0;
  transition: all 0.3s ease;
}

.history-table tbody tr:last-child {
  border-bottom: none;
}

.history-table tbody tr:hover {
  background: rgba(212, 165, 116, 0.15);
  transform: scale(1.005);
}

.history-table td {
  padding: 16px;
  color: #5a4235;
  font-size: 16px;
  font-weight: 600;
}

.history-table td:first-child {
  font-weight: 700;
  color: #6b4423;
  font-size: 17px;
}

.history-table td:last-child {
  color: #8b5a3c;
  font-weight: 700;
  font-size: 18px;
}

/* Date Label inside category cell */
.date-label {
  font-size: 13px;
  color: #a88763;
  font-weight: 500;
  margin-top: 4px;
  font-style: italic;
}

/* No data message */
.history-content > div > p:only-child {
  text-align: center;
  font-size: 19px;
  color: #8b5a3c;
  font-weight: 600;
  padding: 50px 20px;
  background: rgba(212, 165, 116, 0.15);
  border-radius: 20px;
  border: 3px dashed #d4a574;
  font-style: italic;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.history-content > div > p:only-child i {
  font-size: 24px;
}

/* Responsive Design - Large Tablets */
@media (max-width: 1200px) {
  .history-grid {
    grid-template-columns: 350px 1fr;
    gap: 25px;
  }

  .summary-card {
    padding: 30px;
  }
}

/* Responsive Design - Tablet and below */
@media (max-width: 968px) {
  .history-page {
    margin-left: 0; /* Remove sidebar space on mobile */
    padding: 25px 20px;
    padding-top: 80px; /* Space for hamburger menu */
  }

  .history-grid {
    grid-template-columns: 1fr !important;
    gap: 20px !important;
  }
.table-card {
    max-height: 350px !important;  /* taller than summary card */
    overflow-y: hidden  !important;
     padding: 28px !important;
  }
  .summary-card,
  .table-card {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }

  .summary-card {
    position: static;
    padding: 28px;
     max-height: 220px;  /* smaller height */
    overflow-y: auto;
  }

.filters {
    flex-direction: column;
    align-items: stretch;
    width: 100%;
  }

  .filters select {
     width: 100%;
  max-width: 100%;
    
  }

  .filters button {
    width: 100%;
    justify-content: center;
  }

  .filter-icon {
    display: none;
  }
  .table-wrapper {
    max-height: calc(350px -  ( 28px + 56px )) !important;
  }

  .history-table th,
  .history-table td {
    font-size: 14px;
    padding: 12px 10px;
  }

  .summary-card h3 { font-size: 18px !important; }
  .summary-card h4 { font-size: 16px !important; }
  .summary-card p { font-size: 13px !important; padding: 8px 12px !important; }
  .summary-card p strong { font-size: 15px !important; }
  .summary-card h3 i,
  .summary-card h4 i { font-size: 20px !important; }
  .download-btn { font-size: 13px !important; padding: 10px 16px !important; }

  /* Expense / Table Card */
  .table-card h4 { font-size: 18px !important; }
  .history-table th { font-size: 14px !important; padding: 12px 10px !important; }
  .history-table td { font-size: 13px !important; padding: 10px 8px !important; }
  .history-table td:first-child { font-size: 14px !important; }
  .history-table td:last-child { font-size: 15px !important; }
}

/* Responsive Design - Mobile */
@media (max-width: 768px) {
  .history-page {
    padding: 20px 15px;
    padding-top: 75px;
  }

  .filters {
    overflow-x: hidden;
    
  }

  .filters select {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
  }

  .filters button {
    padding: 15px 28px;
    font-size: 16px;
  }

  .summary-card,
  .table-card {
    padding: 20px !important;
    border-radius: 14px !important;
    width: 100% !important;
  }
  .summary-card {
    max-height: 200px;
  }
  .table-card {
    max-height: 300px;
    overflow: visible !important;
  }
  /* Fix card overflow */
  .summary-card *,
  .table-card * {
    max-width: 100% !important;
    word-wrap: break-word !important;
  }

  .error-box {
    font-size: 16px;
    padding: 16px 20px;
  }

  .loading {
    font-size: 18px;
    padding: 40px;
  }

.table-wrapper {
   max-height: 160px;
  overflow-x: auto !important;
   overflow-y: auto !important;
  width: 100% !important;
  display: block;
}

.history-table {
  min-width: 600px; /* scrolls horizontally if screen smaller */
}

/* Ensure the card never scrolls horizontally */
.table-card {
  overflow: hidden !important;
}

/* Make the page scroll vertically smoothly on small screens */
.history-page {
  overflow-x: hidden !important;
}

  .history-table th,
  .history-table td {
    padding: 14px 12px;
    font-size: 15px;
  }

  .summary-card h3 { font-size: 17px !important; }
  .summary-card h4 { font-size: 15px !important; }
  .summary-card p { font-size: 12px !important; padding: 7px 10px !important; }
  .summary-card p strong { font-size: 14px !important; }
  .summary-card h3 i,
  .summary-card h4 i { font-size: 18px !important; }
  .download-btn { font-size: 12px !important; padding: 9px 14px !important; }

  .table-card h4 { font-size: 16px !important; }
  .history-table th { font-size: 13px !important; padding: 10px 8px !important; }
  .history-table td { font-size: 12px !important; padding: 8px 6px !important; }
  .history-table td:first-child { font-size: 13px !important; }
  .history-table td:last-child { font-size: 14px !important; }
}

/* Responsive Design - Small Mobile */
@media (max-width: 480px) {
  .history-page {
    padding: 18px 12px;
    padding-top: 70px;
  }

  .filters {
    padding: 18px;
  }

  .filters select {
    padding: 13px 16px;
    font-size: 14px;
  }

  .filters button {
    padding: 14px 24px;
    font-size: 15px;
    gap: 8px;
  }

  .summary-card,
  .table-card {
    padding: 22px;
  }

  .error-box {
    font-size: 15px;
    padding: 14px 18px;
    gap: 10px;
  }

  .loading {
    font-size: 17px;
    padding: 35px 20px;
  }

  .history-table {
    min-width: 400px;
  }

  .history-table th {
    font-size: 15px;
    padding: 14px 10px;
  }

  .history-table td {
    font-size: 14px;
    padding: 12px 10px;
  }

  .date-label {
    font-size: 12px;
  }

  .history-content > div > p:only-child {
    font-size: 17px;
    padding: 40px 18px;
    gap: 10px;
  }

  .summary-card h3 { font-size: 16px !important; }
  .summary-card h4 { font-size: 14px !important; }
  .summary-card p { font-size: 11px !important; padding: 6px 8px !important; }
  .summary-card p strong { font-size: 13px !important; }
  .summary-card h3 i,
  .summary-card h4 i { font-size: 16px !important; }
  .download-btn { font-size: 11px !important; padding: 8px 12px !important; }

  .table-card h4 { font-size: 15px !important; }
  .history-table th { font-size: 12px !important; padding: 8px 6px !important; }
  .history-table td { font-size: 11px !important; padding: 6px 4px !important; }
  .history-table td:first-child { font-size: 12px !important; }
  .history-table td:last-child { font-size: 13px !important; }
}

/* Very small screens */
@media (max-width: 360px) {
  .history-page {
    padding: 15px 0px;
    padding-top: 65px;
  }

  .filters {
    padding: 3px;
  }

  .summary-card,
  .table-card {
    padding: 20px;
  }
  .history-table {
    min-width: 400px;
  }
  .summary-card h3 { font-size: 15px !important; }
  .summary-card h4 { font-size: 13px !important; }
  .summary-card p { font-size: 10px !important; padding: 5px 6px !important; }
  .summary-card p strong { font-size: 12px !important; }
  .summary-card h3 i,
  .summary-card h4 i { font-size: 14px !important; }
  .download-btn { font-size: 10px !important; padding: 6px 10px !important; }

  .table-card h4 { font-size: 14px !important; }
  .history-table th { font-size: 11px !important; padding: 6px 4px !important; }
  .history-table td { font-size: 10px !important; padding: 5px 4px !important; }
  .history-table td:first-child { font-size: 11px !important; }
  .history-table td:last-child { font-size: 12px !important; }
}
</style>
