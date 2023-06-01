<script>

export default {
  computed: {
    jsonData: {
        get() {
        //console.log("jsonData in component:", this.$store.state.jsonData);
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
        const taskId = this.jsonData['Research ID'];

        const url = `https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/task/${taskId}/webdownload`;

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
        a.download = `${taskId}.xlsx`; // or any name you want to give to your file
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
      const taskId = this.jsonData['Research ID'];
      const cancelUrl = `https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/task/${taskId}/stop`;
      const statusUrl = `https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/task/${taskId}/status`;
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
      const taskId = this.jsonData['Research ID'];
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
    }
  },
};
</script>


<template>
  <div class="container">
    <div class="text-container">
      <p class="textheader">Your AI assistant has begun your research!</p>
      <p class="textbody">Download partial results anytime during the search. Full results remain available for another 24 hours and will be automatically deleted after.</p>
      <p class="textbody">You need the Task ID to retrieve the results. <span class="important-notice">Make sure to save the Task ID to download the results later. It won't be displayed again.</span></p>
    </div>
    <div class="table-responsive text-start">
    <table class="table results-table mx-auto">
      <tr v-for="(value, key) in jsonData" :key="key">
        <td class="key-column">{{ key }}</td>
        <td :class="{'task-id-value': key === 'Research ID', 'refresh-button-cell': key === 'Status'}">
          {{ value }}
          <button v-if="key === 'Status'" @click="refreshData" class="refresh-button btn btn-sm btn-outline-success float-end">↺</button>
        </td>
      </tr>
    </table>
  </div>
    <div class="d-flex justify-content-center gap-5 mt-4">
      <button @click="downloadResults" class="download-button btn btn-outline-primary">Download Results</button>
      <button @click="handleButtonClick" :class="['btn btn-outline', buttonClass]">{{ buttonText }}</button>
    </div>
  </div>
</template>

<style scoped>
.refresh-button {
  padding: 0.25rem 0.5rem; /* make button smaller */
}

.refresh-button-cell {
  position: relative; /* needed for button positioning */
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
.textheader {
  font-size: 1.25rem;
  font-weight: bold;
  color: #fff;
}

.textbody {
  margin-top: 1rem;
  color: #fff;
}

.important-notice {
  font-weight: bold;
  color: red;
}

.results-table {
  margin-top: 1rem;
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

.task-id-value {
  font-weight: bold;
  color: red;
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
.download-button,
.cancel-button,
.newsearch-button {
  width: 200px; /* Make both buttons the same width */
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
