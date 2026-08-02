<template>
  <div class="expense-table">
    <h3><i class="fas fa-receipt" style="color:#6B4F3F; margin-right:6px;"></i> Expenses</h3>
     <div class="table-scroll">
    <table v-if="expenses.length" border="1" cellpadding="8" class="w-full">
      <thead>
        <tr>
          <th></th>
            <th> Amount</th>
            <th>Category</th>
            <th> Date & Time</th>
            <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(e, index) in expenses" :key="index">
          <td data-label="#"> {{ index + 1 }}</td>
          <td data-label="Amount">{{ e.amount }}</td>
          <td data-label="Category">{{ e.category }}</td>
          <td data-label="Date & Time">{{ e.datetime }}</td>
          <td data-label="Actions" class="icons">
            <button @click="$emit('edit', index, e)"><i class="fas fa-edit" style="color:black; font-size:18px;"></i></button>
            <button @click="$emit('delete', index)"><i class="fas fa-trash-alt" style="color:black; font-size:18px;"></i></button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else class="text-gray-600 italic">No expenses recorded yet.</p>
    </div>
    
  </div>
</template>

<script>
export default {
  name: "ExpenseTable",
  props: {
    expenses: {
      type: Array,
      default: () => []
    }
  }
};
</script>

<style scoped>
/* Expense Table Component */
.expense-table {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(107, 68, 35, 0.2);
  border: 3px solid #d4a574;
}

.expense-table h3 {
  font-size: 26px;
  font-weight: 700;
  color: #6b4423;
  margin-bottom: 25px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.05);
}

.expense-table table {
  width: 100%;
  border-collapse: collapse;
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(107, 68, 35, 0.15);
}

.expense-table thead {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
}

.expense-table th {
  padding: 16px 14px;
  text-align: left;
  color: #f5e6d3;
  font-weight: 700;
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.expense-table tbody tr {
  border-bottom: 2px solid #e8d5c0;
  transition: all 0.3s ease;
}

.expense-table tbody tr:last-child {
  border-bottom: none;
}

.expense-table tbody tr:hover {
  background: rgba(212, 165, 116, 0.15);
  transform: scale(1.01);
}

.expense-table td {
  padding: 16px 6px;
  color: #5a4235;
  font-size: 15px;
  font-weight: 500;
}

.expense-table td:first-child {
  font-weight: 700;
  color: #8b5a3c;
}

.expense-table button {
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  color: #f5e6d3;
  border: none;
  padding: 10px 1px;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  margin: 0 5px;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(107, 68, 35, 0.3);
}

.expense-table button:hover {
  transform: translateY(-2px) scale(1.1);
  box-shadow: 0 5px 15px rgba(107, 68, 35, 0.45);
  background: linear-gradient(135deg, #6b4423 0%, #5a3a1f 100%);
}

.expense-table button:active {
  transform: translateY(0) scale(1.05);
}

.expense-table p {
  font-size: 17px;
  color: #8b5a3c;
  text-align: center;
  padding: 40px 20px;
  font-weight: 600;
  font-style: italic;
}
.table-scroll {
  width: 100%;
  max-height: 300px; /* adjust height as needed */
  overflow-x: auto; /* horizontal scroll if needed */
  overflow-y: auto; /* vertical scroll for rows */
  -webkit-overflow-scrolling: touch;
  
}

.table-scroll table {
  width: 100%;
  border-collapse: collapse;
}

.table-scroll thead {
  position: sticky;
  top: 0;
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  z-index: 2;
}


/* Responsive Design - Mobile First */
@media (max-width: 768px) {
  .expense-table {
    padding: 10px;
    overflow-x: auto;
  }

  .expense-table h3 {
    font-size: 22px;
    margin-bottom: 20px;
  }

  /* Make table scrollable on mobile */
  .expense-table table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
  }

  .expense-table th,
  .expense-table td {
    padding: 12px 10px;
    font-size: 14px;
  }

  .expense-table button {
    padding: 8px 10px;
    font-size: 16px;
    margin: 0 3px;
  }
  .table-scroll {
  width: 100%;
  max-height: 300px;
  overflow-x: auto; /* enables horizontal scroll */
  overflow-y: auto; /* prevents vertical scroll inside */
  -webkit-overflow-scrolling: touch;
}

.table-scroll table {
   width: 100%;
  border-collapse: collapse;
}
.table-scroll thead {
  position: sticky;
  top: 0;
  background: linear-gradient(135deg, #8b5a3c 0%, #6b4423 100%);
  z-index: 2;
}

}

@media (max-width: 480px) {
  .expense-table {
    padding: 7px;
  }
.table-scroll {
  width: 100%;
  max-height: 300px;
  overflow-x: auto; /* enables horizontal scroll */
  overflow-y: auto; /* prevents vertical scroll inside */
  -webkit-overflow-scrolling: touch;
}

  .expense-table h3 {
    font-size: 20px;
  }

  .expense-table th,
  .expense-table td {
    padding: 10px 8px;
    font-size: 13px;
  }

  .expense-table th {
    font-size: 14px;
  }

  .expense-table button {
    padding: 6px 8px;
    font-size: 15px;
  }
}

/* Alternative: Card-based layout for very small screens */
@media (max-width: 380px) {
  .expense-table table,
  .expense-table thead,
  .expense-table tbody,
  .expense-table th,
  .expense-table td,
  .expense-table tr {
    display: block;
  }

  .expense-table thead tr {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }

  .expense-table tbody tr {
    margin-bottom: 15px;
    border: 2px solid #d4a574;
    border-radius: 12px;
    padding: 12px;
    background: #ffffff;
  }

  .expense-table tbody tr:hover {
    transform: scale(1);
  }

  .expense-table td {
    border: none;
    position: relative;
    padding: 10px 0px 10px 53%;
    text-align: right;
  }
  .expense-table td[data-label="Date & Time"] {
    white-space: normal;
    word-break: break-word;
  }
.expense-table td[data-label="Actions"] {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-left: 45%; /* keep same label space */
  }

  /* Keep label on the left */
  .expense-table td[data-label="Actions"]::before {
    left: -9px;
    width: 40%;
  }
  .expense-table td:before {
    content: attr(data-label);
    position: absolute;
    left: -9px;
    width: 40%;
    padding-right: 10px;
    white-space: nowrap;
    text-align: left;
    font-weight: 700;
    color: #8b5a3c;
  }

  .expense-table td:last-child {
    text-align: center;
  }

  .expense-table button {
    display: inline-block;
    width: auto;
  }
}
</style>
