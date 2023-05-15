<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['jsonData']),
  },
  created() {
    console.log("jsonData in component:", this.jsonData);
  },
  methods: {
    newSearch() {
      this.$router.push({ path: '/' });
    },
  },
};
</script>

<template>
    <div class="results-container">
      <div class="text-container">
        <p>Your AI agent has begun your research!</p>
        <p>Download partial results anytime during the search. Full results remain available for another 24 hours and will be automatically deleted.</p>
        <p>You need the Task ID to retrieve the results. <span class="important-notice">Make sure to save the Task ID. It won't be displayed again.</span></p>

      </div>
      <table class="results-table">
        <tr v-for="(value, key) in jsonData" :key="key">
          <td class="key-column">{{ key }}</td>
          <td :class="{'task-id-value': key === 'Task ID'}">{{ value }}</td>
        </tr>
      </table>
      <div class="button-container">
        <button type="button" @click="newSearch" class="startover-button">New Search</button>
      </div>
    </div>
  </template>
  
  <style scoped>
  .results-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  .text-container {
    max-width: 1000px; /* Match the table width */
    width: 100%;
    text-align: left;
  }
  
  .results-container p {
    font-family: Arial, sans-serif;
    font-size: 20px;
    margin-bottom: 20px;
  }
  
  .important-notice {
    font-weight: bold;
    color: red;
  }
  
  .search-results-title {
    font-weight: bold;
    margin-bottom: 20px;
  }
  
  .results-table {
    width: 900px;
    font-family: Arial, sans-serif;
    font-size: 20px;
    margin-bottom: 20px;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  .results-table td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  
  .key-column {
    width: 200px; /* Adjust as needed */
  }
  
  .task-id-value {
    font-weight: bold;
    color: red;
  }
  
  .button-container {
    display: flex;
    justify-content: center;
    gap: 120px;
    margin-top: 80px;
  }
  
  .startover-button {
    border: 2px solid #0c952c;
    border-radius: 8px;
    background-color: #ffffff;
    color: #0c952c;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
  }
  
  .startover-button:hover {
    background-color: #0c952c;
    color: #ffffff;
  }
  </style>
  