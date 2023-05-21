<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['jsonData']),
    jsonData: {
        get() {
        //   console.log("jsonData in component:", this.$store.state.jsonData);
          return this.$store.state.jsonData;
        },
        set(value) {
          this.$store.dispatch('setJsonData', value);
        }
      },
  },
//   created() {
//     console.log("jsonData in component:", this.jsonData);
//   },
  methods: {
    newSearch() {
      this.$router.push({ path: '/' });
    },
    async cancelSearch() {
      const taskId = this.jsonData['Task ID'];
      const cancelUrl = `http://127.0.0.1:8000/task/${taskId}/stop`;
      const statusUrl = `http://127.0.0.1:8000/task/${taskId}/status`;
      try {
          this.buttonText = "Cancelling..."
          await fetch(cancelUrl, { method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          const response = await fetch(statusUrl, { method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
            // body: JSON.stringify(this.jsonData["Task ID"]),
          });
  
          this.jsonData = await response.json();
  
        } catch (error) {
          console.error(error);
        }
    }
  },
};
</script>

<template>
    <div class="results-container">
      <div class="text-container">
        <p class="textheader">Your AI assistant has begun your research!</p>
        <p class="textbody">Download partial results anytime during the search. Full results remain available for another 24 hours and will be automatically deleted after.</p>
        <p class="textbody">You need the Task ID to retrieve the results. <span class="important-notice">Make sure to save the Task ID. It won't be displayed again.</span></p>
      </div>
      <table class="results-table">
        <tr v-for="(value, key) in jsonData" :key="key">
          <td class="key-column">{{ key }}</td>
          <td :class="{'task-id-value': key === 'Task ID'}">{{ value }}</td>
        </tr>
      </table>
      <div class="button-container">
        <button type="button" @click="newSearch" class="startover-button">New Search</button>
        <button type="button" @click="cancelSearch" class="cancel-button">Cancel Search</button>
      </div>
    </div>
  </template>
  
  <style scoped>
  .results-container {
    margin-top: -20px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .textheader {
    width: 1000px; /* Match the table width */
    text-align: left;
    font-size: 20px;
    font-weight: bold;

  }
  .textbody {
    margin-top: 40px;
    width: 900px;
    padding-left: 50px;
  }
  .results-container p {
    font-family: Arial, sans-serif;
    font-size: 20px;
    margin-bottom: 10px;
  }
  
  .important-notice {
    font-weight: bold;
    color: red;
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
    margin-top: 50px;
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

.cancel-button {
    border: 2px solid #ff4800;
    border-radius: 8px;
    background-color: #ffffff;
    color: #ff4800;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
  }

  .cancel-button:hover {
    background-color: #ff4800;
    color: #ffffff;
  }

  </style>
  