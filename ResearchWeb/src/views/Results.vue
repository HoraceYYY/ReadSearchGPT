<script>
  import { mapGetters } from 'vuex';

  export default {
    data() {
  return {
    // Other data properties...
    copyMessage: '',
    copyMessageTheme: ''
  };
},
    computed: {
    ...mapGetters(['taskId']),
      jsonData: {
        get() {
        //   console.log("jsonData in component:", this.$store.state.jsonData);
          return this.$store.state.jsonData;
        },
        set(value) {
          this.$store.dispatch('setJsonData', value);
        }
      },
      buttonText() {
        return this.jsonData.Status === "Researching..." ? "Cancel Search" : " New Search ";
      },
      buttonClass() {
        return this.jsonData.Status === "Researching..." ? "cancel-button" : "newsearch-button";
      },
      processedJsonData() {
      // Deep clone the original data so we do not mutate the state directly
      let processedData = JSON.parse(JSON.stringify(this.jsonData));

      // Check if 'Research Topic(s)' exists and is a string
      if (processedData['Research Topic(s)'] && typeof processedData['Research Topic(s)'] === 'string') {
        // Remove brackets and quotes, then split string into array
        let topics = processedData['Research Topic(s)'].replace(/[\[\]']+/g, '').split(', ');

        // Format the 'Research Topic(s)' field
        processedData['Research Topic(s)'] = topics.map((topic, index) => `${index + 1}. ${topic}`).join(', ');
      }

      return processedData;
    },
    },
    methods: {
      async downloadResults() {

        const url = `http://localhost:8000/task/${this.taskId}/webdownload`;

        try {
          const response = await fetch(url, { method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = `${this.taskId}.xlsx`; // or any name you want to give to your file
        document.body.appendChild(a);
        a.click();
        // After a timeout, remove the element and revoke the object URL
        setTimeout(() => {
            a.remove();
            window.URL.revokeObjectURL(downloadUrl);
        }, 0);

        } catch (error) {
          console.error(error);
        }
      },
      handleButtonClick() {
        if (this.jsonData.Status === "Researching...") {
          this.cancelSearch();
        } else {
          this.$router.push({ path: '/' });
        }
      },
      async cancelSearch() {
        const cancelUrl = `http://localhost:8000/task/${this.taskId}/stop`;
        const statusUrl = `http://localhost:8000/task/${this.taskId}/status`;
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
          });
  
          this.jsonData = await response.json();
  
        } catch (error) {
          console.error(error);
        }
      },
      async refreshData() {
      const taskId = this.$store.state.taskId;
      const statusUrl = `https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/task/${taskId}/status`;

      try {
        const response = await fetch(statusUrl, { method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        this.jsonData = await response.json();

      } catch (error) {
        console.error(error);
      }
    },
    copyToClipboard(value) {
      navigator.clipboard.writeText(value)
        .then(() => {
          this.copyMessage = 'Research ID copied to clipboard!';
          this.copyMessageTheme = 'success';
          setTimeout(() => {
            this.copyMessage = '';
          }, 2500);
        })
        .catch(err => {
          console.error('Could not copy text: ', err);
          this.copyMessage = 'Failed to copy Research ID.';
          this.copyMessageTheme = 'danger';
          setTimeout(() => {
            this.copyMessage = '';
            this.copyMessageTheme = '';
          }, 2500);
        });
    },
    }
  };
  </script>




<template>
  <div class="container">
    <div class="text-container text-start">
      <div v-if="copyMessage" class="copy-message-popup" :class="copyMessageTheme">{{ copyMessage }}</div>
      <p class="textheader">Search Result:</p>
      <div class="table-responsive text-start">
    <table class="table results-table mx-auto">
      <tr v-for="(value, key) in processedJsonData" :key="key">
        <td class="key-column">{{ key }}</td>
        <td :class="{'status-green': key === 'Status' && (value === 'Researching...' || value === 'Completed'), 'status-red': key === 'Status' && value !== 'Researching...' && value !== 'Completed', 'refresh-button-cell': key === 'Status'}" >
          {{ value }}
          <button v-if="key === 'Status'" @click="refreshData" class="refresh-button btn btn-sm btn-outline-success float-end">↺</button>
          <button v-if="key === 'Research ID'" @click="copyToClipboard(value)" class="copy-button btn btn-sm btn-outline-primary float-end">&#x1F4CB</button>
        </td>
      </tr>
    </table>
  </div>
      <div class="d-flex justify-content-center gap-5 mt-4">
        <button @click="downloadResults" class="download-button btn btn-outline-primary">Download Results</button>
        <button @click="handleButtonClick" :class="['btn btn-outline', buttonClass]">{{ buttonText }}</button>
      </div>
    </div>
  </div>
</template>
  
<style scoped>
.copy-message-popup {
  position: fixed;
  top: 0;
  left: 50%;  /* center the popup */
  transform: translateX(-50%); /* shift it left by half its width */
  padding: 1rem;
  text-align: center;
  max-width: 400px;  /* limit the width */
  z-index: 1000;
}

.copy-message-popup.success {
  background-color: #d4edda;
  color: #155724;
}

.copy-message-popup.danger {
  background-color: #f8d7da;
  color: #721c24;
}
.copy-button {
  padding: 0.25rem 0.5rem; /* adjust as needed for size */
  border: none; /* removes border */
  background: transparent; /* makes background transparent */
  font-size: 0.75rem; /* adjust as needed for size */
}
.refresh-button {
  padding: 0.25rem 0.5rem; /* make button smaller */
  border: none; /* removes border */
}

.refresh-button-cell {
  position: relative; /* needed for button positioning */
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.btn-outline-success {
  color: #198754;
  border-color: #198754;
}

.btn-outline-success:hover {
  color: #fff;
  background-color: #198754;
  border-color: #198754;
}
.container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.text-container {
  margin-top: -5px;
  max-width: 800px; /* Match the table width */
  width: 100%;
  
}

.textheader {
  font-family: Arial, sans-serif;
  font-size: 1.25rem;
  margin-bottom: 1rem;
  font-weight: bold;
  color: #fff;

}

.table-responsive {
  margin-top: 1rem;
  color: #fff;
}

.results-table {
  border-collapse: collapse;
  max-width: 800px;
  color: #fff;
}

.results-table td {
  border: 1px solid #dee2e6;
  padding: 0.5rem;
}

.key-column {
  width: 200px; /* Adjust as needed */
}

.status-green {
  color: green;
}

.status-red {
  color: red;
}

.download-button,
.cancel-button,
.newsearch-button {
  width: 200px; /* Make both buttons the same width */
}

.download-button {
  border-color: #8e8ef7;
  color: #8e8ef7;
}

.download-button:hover {
  background-color: #8e8ef7;
  color: #fff;
}

.cancel-button {
  border-color: #ff4800;
  color: #ff4800;
}

.cancel-button:hover {
  background-color: #ff4800;
  color: #fff;
}

.newsearch-button {
  border-color: #0c952c;
  color: #0c952c;
}

.newsearch-button:hover {
  background-color: #0c952c;
  color: #fff;
}


@media (max-width: 576px) {
  /* For mobile view */
  .results-table td {
    font-size: 0.875rem; /* Make text smaller */
  }
  
  .key-column {
    width: 100px; /* Make key column narrower */
  }
}
</style>