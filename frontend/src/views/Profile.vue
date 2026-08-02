<template>
  <div class="profile-page">
    <Sidebar :username="username"/>
      
    <div v-if="profile.username">
      <div class="profile-left">
        <div class="profile-avatar">
      <i class="fas fa-user-circle"></i>
    </div>
      <p><strong>Username:</strong> {{ profile.username }}</p>
      <p><strong>Join Date:</strong> {{ profile.join_date }}</p>
      <p><strong>Total Savings:</strong> ₹{{ allTimeSavings }}</p>

      <!-- <div class="toggle-section">
        <label>
          <input
            type="checkbox"
            v-model="deductionEnabled"
            @change="openDeductionModal"
          />
          Enable 2.5% Deduction for this month
        </label>
      </div> -->
    </div>
    <div class="profile-right">
        <label class="year-label">Select Year</label>
        <select v-model="selectedYear" class="year-select" aria-label="Select year">
          <option value="">-- Select year --</option>
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>

        <div class="download-row">
          <button :disabled="!selectedYear || downloading" @click="openDeleteYearModal" class="download-btn">
            <i class="fas fa-download icon"></i>
            {{ downloading ? 'Preparing...' : 'Download Yearly Report' }}
          </button>
        </div>
      </div>
    </div>

    <div v-else>
      <p><i class="fas fa-info-circle black-icon"></i>Loading profile...</p>
    </div>
    <!-- Delete Confirmation Modal -->
      <!-- <div class="modal" v-if="showDeductionModal">
        <div class="modal-inner">
           <h3>Confirm Action</h3>
          <p>
          Are you sure you want to 
          <strong>{{ deductionEnabled ? 'enable' : 'disable' }}</strong>
          the 2.5% deduction for this month?
        </p>

          <div class="actions">
          <button class="confirm" @click="confirmDeductionChange">Yes</button>
          <button class="cancel" @click="cancelDeductionChange">Cancel</button>
        </div>
        </div>
      </div> -->
      <!-- Delete Year Confirmation Modal -->
<div class="modal" v-if="deleteYearModal">
  <div class="modal-inner">
     <h3 style="color: red;">Confirm Download & Delete</h3>
    <p style="color: red;">
      Downloading the report will <strong>REMOVE ALL DATA</strong> for {{ selectedYear }} from the server.
    </p>

    <div class="actions">
      <button class="confirm" style="background-color: red;" @click="confirmDownloadAndDelete">Confirm</button>
      <button class="cancel" @click="cancelDeleteYear">Cancel</button>
    </div>
  </div>
</div>

  </div>
</template>

<script>
import axios from "axios";
import Sidebar from "../components/Sidebar.vue";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
export default {
  name: "ProfilePage",
   components: {  Sidebar },
  data() {
    return {
      username: "",
      profile: {},
      deductionEnabled: false,
      allTimeSavings: 0,
      selectedYear: "",
      years: [],
      report: null,
      downloading: false,

      showDeductionModal: false,
      tempDeductionValue: false,
      deleteYearModal: false,

    };
  },
  async mounted() {
    try {
      const localData = JSON.parse(localStorage.getItem("user") || "{}");
       if (!localData || !localData.join_date) {
      this.$router.push("/");
      return;
      }
    
    const joinYear = Number(localData.join_date.split("-")[0]);  
    const currentYear = new Date().getFullYear();

    this.years = [];
    for (let y = joinYear; y <= currentYear; y++) {
      this.years.push(String(y));
    }


      // Ask backend which user has this join_date
      const response = await axios.get("/api/find_by_join_date", {
        params: { join_date: localData.join_date }
      });

      if (!response.data.username || response.data.username === "") {
    alert("Invalid user session.");
    this.$router.push("/");
    return;
    }
      this.username = response.data.username; 

      // ✅ Step 1: Fetch full profile from backend
      const resp = await axios.get("/api/profile/get", {
        params: { username: this.username },
      });

      if (resp.data.ok) {
        this.profile = resp.data.profile;
        this.allTimeSavings = resp.data.profile.all_time_savings || 0;
        this.deductionEnabled = resp.data.deduction_enabled ?? false;
      } else {
        alert("Failed to load profile");
      }
    } catch (err) {
      console.error(err);
      alert("Error loading profile data");
    }
  },
  methods: {
    openDeleteYearModal() {
    if (!this.selectedYear) {
      alert("Select a year first");
      return;
    }
    this.deleteYearModal = true;
  },
  cancelDeleteYear() {
    this.deleteYearModal = false;
  },
    openDeductionModal() {
      this.tempDeductionValue = !this.deductionEnabled; // store previous value
      this.showDeductionModal = true;
    },
    // async confirmDeductionChange() {
    //   try {
    //     const resp = await axios.post("/api/monthly/toggle_deduction", {
    //       username: this.profile.username,
    //       enable_deduction: this.deductionEnabled,
    //     });

    //     if (resp.data.ok) {
    //      return;
    //     } else {
    //       alert(resp.data.error || "Failed to update deduction");
    //     }
    //   } catch (err) {
    //     console.error(err);
    //     alert("Server error");
    //   }
    // },
    // cancelDeductionChange() {
    //   // revert checkbox to old value
    //   this.deductionEnabled = this.tempDeductionValue;
    //   this.showDeductionModal = false;
    // },

    async fetchYearlyReport() {
      if (!this.selectedYear) {
        alert("Please select a year first.");
        return null;
      }

      try {
        const resp = await axios.get("/api/report/yearly", {
          params: {
            username: this.username,
            year: this.selectedYear
          }
        });

        if (resp.data.ok) {
          this.report = resp.data;
          return resp.data;
        } else {
          alert(resp.data.error || "No data for selected year");
          return null;
        }
      } catch (err) {
        console.error("Failed fetching yearly report", err);
        alert("Failed to fetch report from server");
        return null;
      }
    },

    getColor(amount) {
      return amount > 1000 ? [255, 0, 0] : [0, 128, 0]; // red / green
    },

    async confirmDownloadAndDelete() {
    this.downloading = true;
    this.deleteYearModal = false;

    try {
      // 1️⃣ Fetch yearly report
      const r = await this.fetchYearlyReport();
      if (!r) return;
        const doc = new jsPDF("p", "pt", "a4");
        const marginLeft = 40;
        const pageWidth = doc.internal.pageSize.getWidth();

        // Title (center)
        doc.setFontSize(20);
        doc.text(`${r.year} Summary Report`, pageWidth / 2, 60, { align: "center" });

        // Header (username + small meta)
        doc.setFontSize(12);
        doc.text(`Name: ${r.username}`, marginLeft, 90);
        doc.text(`Generated: ${new Date().toLocaleString()}`, pageWidth - marginLeft, 90, { align: "right" });

        // Two boxes area
        const topY = 110;
        const leftX = marginLeft;
        const rightX = pageWidth / 2 + 10;

        doc.setFontSize(11);
        // Left box lines
        doc.text("Total Income:", leftX, topY);
        doc.setTextColor(...this.getColor(r.summary.total_income));
        doc.text(String(r.summary.total_income), leftX, topY + 14);
        doc.setTextColor(0,0,0);

        doc.text("Total Savings:", leftX, topY + 36);
        doc.setTextColor(...this.getColor(r.summary.total_savings));
        doc.text(String(r.summary.total_savings), leftX, topY + 50);
        doc.setTextColor(0,0,0);

        // Right box lines
        doc.text("Total Lent:", rightX, topY);
        doc.setTextColor(...this.getColor(r.summary.total_lent));
        doc.text(String(r.summary.total_lent), rightX, topY + 14);
        doc.setTextColor(0,0,0);

        doc.text("Total Returned:", rightX, topY + 36);
        doc.setTextColor(...this.getColor(r.summary.total_returned));
        doc.text(String(r.summary.total_returned), rightX, topY + 50);
        doc.setTextColor(0,0,0);

        // Start tables lower
        let tableStartY = topY + 80;

        // Expenses table
        if (r.expenses && r.expenses.length) {
          autoTable(doc, {
            startY: tableStartY,
            head: [["Amount", "Category", "Date & Time"]],
            body: r.expenses.map(e => [String(e.amount), e.category || "-", e.datetime || "-"]),
            styles: { fontSize: 10 },
            headStyles: { fillColor: [139,90,60] }
          });
          tableStartY = doc.lastAutoTable.finalY + 20;
        } else {
          doc.setFontSize(11);
          doc.text("No expenses for this year.", marginLeft, tableStartY);
          tableStartY += 24;
        }

        // Lendings table
        if (r.lendings && r.lendings.length) {
          autoTable(doc, {
            startY: tableStartY,
            head: [["Amount", "To Whom", "Reason", "Returned", "Date"]],
            body: r.lendings.map(l => [
              String(l.amount),
              l.to_whom || "-",
              l.reason || "-",
              l.returned ? "Yes" : "No",
              l.date || l.datetime || "-"
            ]),
            styles: { fontSize: 10 },
            headStyles: { fillColor: [139,90,60] }
          });
        } else {
          doc.setFontSize(11);
          doc.text("No lendings for this year.", marginLeft, tableStartY);
        }

        // Save PDF
        doc.save(`Yearly-Report-${r.year}-${r.username}.pdf`);

        await axios.delete("/api/report/yearly", {
        data: { username: this.username, year: this.selectedYear }
      });

      } catch (err) {
        console.error("PDF generation failed", err);
        alert("Failed to generate PDF");
      } finally {
        this.downloading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Profile Page Container */

.profile-avatar {
  margin-bottom: 2px;
  font-size: 60px;
  text-align: center;
  color: #3B2F2F; /* coffee-black */
}
.profile-page {
  margin-left: 250px; /* Space for sidebar on desktop */
   overflow-x: hidden !important;
  overflow-y: auto !important;
  height: 100vh;
  padding-bottom: 0 !important;
  background: linear-gradient(135deg, #f5e6d3 0%, #e8d5c0 100%);
  font-family: 'Quicksand', sans-serif;
  transition: margin-left 0.3s ease;
}
/*Main profile content wrapper */
.profile-page > div {
  display: grid;
  overflow: hidden !important;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  align-items: start;
}


/* Profile Left Section */
.profile-left {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 35px;
  box-shadow: 0 8px 30px rgba(107, 68, 35, 0.2);
  border: 3px solid #d4a574;
}

.profile-left p {
  font-size: 18px;
  margin-bottom: 18px;
  color: #5a4235;
  line-height: 1.7;
  padding: 14px 20px;
  background: rgba(212, 165, 116, 0.1);
  border-radius: 12px;
  border-left: 4px solid #8b5a3c;
  transition: all 0.3s ease;
}

.profile-left p:hover {
  background: rgba(212, 165, 116, 0.2);
  transform: translateX(5px);
}

.profile-left p strong {
  color: #6b4423;
  font-weight: 700;
  font-size: 19px;
  display: inline-block;
  min-width: 140px;
}

/* Toggle Section */
.toggle-section {
  margin-top: 30px;
  padding: 25px;
  background: linear-gradient(145deg, rgba(139, 90, 60, 0.1) 0%, rgba(212, 165, 116, 0.15) 100%);
  border-radius: 16px;
  border: 2px solid #d4a574;
}

.toggle-section label {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 17px;
  color: #5a4235;
  cursor: pointer;
  font-weight: 600;
  line-height: 1.6;
}

.toggle-section input[type="checkbox"] {
  width: 24px;
  height: 24px;
  cursor: pointer;
  accent-color: #8b5a3c;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.toggle-section input[type="checkbox"]:hover {
  transform: scale(1.15);
}

/* Profile Right Section */
.profile-right {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 35px;
  box-shadow: 0 8px 30px rgba(107, 68, 35, 0.2);
  border: 3px solid #d4a574;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.profile-right,
.profile-right * {
  box-sizing: border-box;
}


/* Year Label */
.year-label {
  font-size: 18px;
  font-weight: 700;
  color: #6b4423;
  margin-bottom: 8px;
  display: block;
}

/* Year Select Dropdown */
.year-select {
  width: 100%;
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
  background-position: right 16px center;
  padding-right: 45px;
}

.year-select:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 4px rgba(139, 90, 60, 0.2);
  background-color: #ffffff;
}

.year-select:hover {
  border-color: #8b5a3c;
}

.year-select option {
  padding: 12px;
  background: #ffffff;
  color: #4a3728;
}

/* Download Row */
.download-row {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}

/* Download Button */
.download-btn {
  width: 100%;
  padding: 18px 32px;
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
  position: relative;
  overflow: hidden;
}



.download-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(107, 68, 35, 0.5);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.download-btn:active:not(:disabled) {
  transform: translateY(-1px);
}

.download-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: linear-gradient(135deg, #a88763 0%, #8b6f4f 100%);
}

/* Loading state */
.profile-page > div > p:only-child {
  grid-column: 1 / -1;
  font-size: 18px;
  color: #8b5a3c;
  font-weight: 600;
  text-align: center;
  padding: 40px;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}


@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
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
.modal {
  position: fixed !important;
  top: 0;
  left: 0;
  width: 100vw !important;
  height: 100vh !important;
  background: rgba(0,0,0,0.6);
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 999999;
}

.modal-inner {
  background: white;
  padding: 20px;
  width: 90%;
  max-width: 400px;
  border-radius: 12px;
}

.modal-inner h3 {
  font-size: 28px;
  font-weight: 700;
  color: #6b4423;
  margin-bottom: 25px;
  text-align: center;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

.modal-inner p {
  font-size: 17px;
  color: #5a4235;
  margin-bottom: 28px;
  line-height: 1.7;
  text-align: center;
}

.modal-inner p strong {
  color: #8b5a3c;
  font-weight: 700;
  font-size: 19px;
}

/* Modal Actions */
.modal-inner .actions {
  display: flex;
  gap: 14px;
  margin-top: 28px;
  justify-content: center;
}

.modal-inner .actions button {
  flex: 1;
  padding: 16px 28px;
  border: none;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Quicksand', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-inner .actions .confirm {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  box-shadow: 0 4px 15px rgba(107, 68, 35, 0.35);
}

.modal-inner .actions .confirm:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(107, 68, 35, 0.5);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.modal-inner .actions .cancel {
  background: linear-gradient(135deg, #c4956a 0%, #a88763 100%);
  color: #4a3728;
  box-shadow: 0 4px 15px rgba(164, 135, 99, 0.3);
}

.modal-inner .actions .cancel:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(164, 135, 99, 0.45);
  background: linear-gradient(135deg, #a88763 0%, #8b6f4f 100%);
}

.modal-inner .actions button:active {
  transform: translateY(-1px);
}

/* Responsive Design - Tablet and below */
@media (max-width: 968px) {
  .profile-page {
    margin-left: 0; /* Remove sidebar space */
    padding: 25px 20px;
    padding-top: 80px; /* Space for hamburger menu */
  }

  .profile-page > h2 {
    font-size: 30px;
    margin-bottom: 28px;
  }

  .profile-page > div {
    grid-template-columns: 1fr;
    gap: 25px;
  }

  .profile-left,
  .profile-right {
    padding: 28px;
  }
}

/* Responsive Design - Mobile */
@media (max-width: 768px) {
  .profile-page {
    padding: 20px 15px;
    padding-top: 75px;
  }

  .profile-page > h2 {
    font-size: 28px;
    margin-bottom: 25px;
  }

  .profile-left,
  .profile-right {
    padding: 25px;
  }

  .profile-left p {
    font-size: 16px;
    padding: 12px 16px;
  }

  .profile-left p strong {
    font-size: 17px;
    min-width: 120px;
  }

  .toggle-section {
    padding: 20px;
  }

  .toggle-section label {
    font-size: 16px;
  }

  .year-label {
    font-size: 17px;
  }

  .year-select {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
  }

  .profile-right {
    overflow: visible !important;
  }

  .download-btn {
    padding: 16px 28px;
    font-size: 16px;
  }

  .modal-inner {
    padding: 32px;
    width: 92%;
  }

  .modal-inner h3 {
    font-size: 24px;
  }

  .modal-inner p {
    font-size: 16px;
  }

  .modal-inner .actions {
    flex-direction: column;
  }

  .modal-inner .actions button {
    width: 100%;
  }
}

/* Responsive Design - Small Mobile */
@media (max-width: 480px) {
  .profile-page {
    padding: 18px 12px;
    padding-top: 70px;
  }

  .profile-page > h2 {
    font-size: 26px;
    margin-bottom: 22px;
  }

  .profile-page > div {
    gap: 20px;
  }

  .profile-left,
  .profile-right {
    padding: 22px;
    border-radius: 16px;
  }

  .profile-left p {
    font-size: 15px;
    padding: 11px 14px;
    margin-bottom: 14px;
  }

  .profile-left p strong {
    font-size: 16px;
    min-width: 110px;
    display: block;
    margin-bottom: 4px;
  }

  .toggle-section {
    padding: 18px;
  }

  .toggle-section label {
    font-size: 15px;
    gap: 12px;
  }

  .toggle-section input[type="checkbox"] {
    width: 22px;
    height: 22px;
  }

  .year-label {
    font-size: 16px;
  }

.year-select {
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  padding-right: 40px; /* slightly reduced */
}

  .download-btn {
    padding: 15px 24px;
    font-size: 15px;
    letter-spacing: 0.3px;
  }

  .download-btn::before {
    font-size: 18px;
    margin-right: 6px;
  }

  .modal-inner {
    padding: 28px;
    border-radius: 20px;
  }

  .modal-inner h3 {
    font-size: 22px;
    margin-bottom: 20px;
  }

  .modal-inner p {
    font-size: 15px;
    margin-bottom: 24px;
  }

  .modal-inner .actions button {
    padding: 14px 24px;
    font-size: 16px;
  }
}

/* Very small screens */
@media (max-width: 360px) {
  .profile-page {
    padding: 1px 0px;
    padding-top: 65px;
  }

  .profile-page > h2 {
    font-size: 24px;
  }

  .profile-left,
  .profile-right {
    padding: 6px;
  }

  .modal-inner {
    padding: 24px;
    width: 95%;
  }
}
</style>
