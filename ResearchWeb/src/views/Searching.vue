<script>

export default {
  data() {
  return {
    // Other data properties...
    copyMessage: '',
    copyMessageTheme: '',
    email1: '',
    email2: '',
    email3: '',
    showModal: false,
  };
},
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
    async sendResultsToEmail() {
      const emails = [this.email1, this.email2, this.email3];
      const taskId = this.jsonData['Research ID'];

      // add a post request to the back end to take the research Id and emails to handle the function of sending emails'
      // const response = await fetch(`https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/task/${taskId}/webdownload`, {
      //   headers: { 'Content-Type': 'application/json' },
      // });
      // const results = await response.json(); // or blob(), depending on the format of the response

      // After sending the emails, you can clear the email inputs and hide the modal
      this.email1 = '';
      this.email2 = '';
      this.email3 = '';
      this.showModal = false;
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
  },
};
</script>


<template>
  <div class="container">
    <div class="text-container">
      <div v-if="copyMessage" class="copy-message-popup" :class="copyMessageTheme">{{ copyMessage }}</div>
      <p class="textheader">Your AI assistant has begun your research!</p>
      <p class="textbody">Download partial results anytime during the search. Full results remain available for another 24 hours and will be automatically deleted after.</p>
      <p class="textbody">You need the Task ID to retrieve the results. <span class="important-notice">Make sure to save the Task ID to download the results later. It won't be displayed again.</span></p>
    </div>
    <div class="table-responsive text-start">
    <table class="table results-table mx-auto">
      <tr v-for="(value, key) in processedJsonData" :key="key">
        <td class="key-column">{{ key }}</td>
        <td :class="{'task-id-value': key === 'Research ID', 'refresh-button-cell': key === 'Status'}">
          {{ value }}
          <button v-if="key === 'Status'" @click="refreshData" class="refresh-button btn btn-sm btn-outline-success float-end">↺</button>
          <button v-if="key === 'Research ID'" @click="copyToClipboard(value)" class="copy-button btn btn-sm btn-outline-primary float-end">&#x1F4CB</button>
        </td>
      </tr>
    </table>
  </div>
  <div class="d-flex justify-content-center gap-5 mt-2 mb-4">
    <button @click="showModal = true" class="email-button btn btn-outline-primary">Email Results</button>
    <button @click="handleButtonClick" :class="['btn btn-outline', buttonClass]">{{ buttonText }}</button>
  </div>

  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <h2 class="modal-title">The complete results will be emailed to the following recipients. </h2>
      <form @submit.prevent="sendResultsToEmail">
        <input v-model="email1" type="email" placeholder="Email 1" required>
        <input v-model="email2" type="email" placeholder="Email 2" >
        <input v-model="email3" type="email" placeholder="Email 3" >
        <button type="submit">Send</button>
      </form>
      <button @click="showModal = false">Close</button>
    </div>
  </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: #fff;
  padding: 2rem;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 400px;

}

.modal-content form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.modal-content form input {
  padding: 0.5rem;
  border-radius: 0.25rem;
  border: 1px solid #ced4da;
}

.modal-content form button {
  padding: 0.5rem;
  border-radius: 0.25rem;
  border: 1px solid #ced4da;
  background-color: #8e8ef7;
  color: #fff;
  cursor: pointer;
}

.modal-content form button:hover {
  background-color: #6c6ce3;
}

.modal-content button {
  margin-top: 1rem;
  padding: 0.5rem;
  border-radius: 0.25rem;
  border: 1px solid #ced4da;
  background-color: #f8f9fa;
  color: #212529;
  cursor: pointer;
}

.modal-content button:hover {
  background-color: #e9ecef;
}
.modal-title {
  color: #585858;  /* Change this to any color you want */
}
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
  .modal-content {
    max-width: 350px;  /* Modal will be wider on screens larger than 576px */
  }
}

</style>
