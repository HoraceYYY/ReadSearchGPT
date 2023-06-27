<template>
  <div class="container history-container">
    <h1 class="display-4 mb-1 fw-bold">ReadSearch GPT</h1>  
    <h2 class="h3 mb-1 fw-bold" style="font-style: italic;">Historical Research Reports</h2>
    <div class="card">
        <div class="card-content">
          <div v-if="isLoading" class="d-flex justify-content-center align-items-center">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading queries...</span>
            </div>
          </div>
          <div v-else>
            <div v-for="(query, id) in queries" :key="id" class="mb-2">
              <div class="singlecard mb-2">
                <button class="btn w-100 text-primary query-button" @click="handleQueryClick(id)">
                  {{ query }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>


<script>

export default {
  data() {
    return {
      isLoading: true,
      queries: {}
    }
  },
  async created() {
    await this.fetchQueries();
  },
  computed:{
    jsonData: {
        get() {
            return this.$store.state.jsonData;
        },
        set(value) {
            this.$store.dispatch('setJsonData', value);
        }
    }
  },
  methods: {
    async fetchQueries() {
      const url = "https://readsearchgpt.com/api/queryhistory";
      try {
        const response = await fetch(url, {
          method: 'GET',
          credentials: 'include', // to include cookies
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        //console.log(data)
        if (data === null) {
          this.queries = {}
        } else {
          this.queries = data;
        }
        
        this.isLoading = false;
      } catch (error) {
        console.error('API call failed:', error);
      }
    },
    async handleQueryClick(queryId) {
      const url = "https://readsearchgpt.com/api/historicalresults";  // Replace with your backend URL
      const queryIdArray = {queryIDs : [queryId]}
      try {
        const response = await fetch(url, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(queryIdArray)
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        //console.log(data);
        // Do something with the data
        this.jsonData = data;  // assign jsonData directly
        this.$router.push({ path: '/searchresults' });
      } catch (error) {
        console.error('API call failed:', error);
      }
    },
  },
};
</script>
<style scoped>

h1, h2 {
  color: #5781c0;
}

.btn.query-button {
  color: #5781c0;
  border: none;
  background-color: transparent;
}

.btn.query-button:hover {
  color: #333;
  background-color: #ddd;
}

.singlecard {
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.card {
    height: calc(100vh - 16rem); /* Adjust as needed */
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
}
.card-content {
 position: relative;
 overflow-y: auto;
 padding: 12px;
 flex-grow: 1;
}
.card-footer {
  display: flex;
  justify-content: center;
  align-items: center;
}
.btn-success {
  background-color: #0c952c;
  border-color: #0c952c;
  color: #ffffff;
  border-radius: 5px; /* Add rounded corners */
  padding: 5px 10px; /* Add some padding */
}
.btn-success:hover {
  background-color: #006c22;
  border-color: #006c22;
}
</style>
