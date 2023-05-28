<script>
  import { mapGetters } from 'vuex';

  export default {
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
    },
    methods: {
      async downloadResults() {

        const url = `https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/task/${this.taskId}/webdownload`;

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
        const cancelUrl = `https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/task/${this.taskId}/stop`;
        const statusUrl = `https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/task/${this.taskId}/status`;
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
      }
    }
  };
  </script>




<template>
  <div class="container">
    <div class="text-container text-start">
      <p class="textheader">Search Result:</p>
      <div class="table-responsive">
        <table class="table results-table mx-auto">
          <tr v-for="(value, key) in jsonData" :key="key">
            <td class="key-column">{{ key }}</td>
            <td class="value-column" :class="{'status-green': key === 'Status' && (value === 'Researching...' || value === 'Completed'), 'status-red': key === 'Status' && value !== 'Researching...' && value !== 'Completed'}">{{ value }}</td>
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