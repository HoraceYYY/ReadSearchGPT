<template>
    <div class="container-fluid px-4">
        <div class="row d-flex">
            <div class="col-12 col-md-7 pr-md-2">
                <div class="card">
                    <div class="card-content">
                        <div class="mb-4 text-start text-black">
                            <h3 class="font-weight-bold ">{{ queries[queryIDs[currentQueryId]] }}</h3>
                            <p>{{ urlSummaries[queryIDs[currentQueryId]] }}</p>
                        </div>
                    </div>
                    <div class="card-footer">
                        <button @click="previousQuery" :disabled="currentQueryId == 0" class="btn-prev">Previous question</button>
                        <button @click="nextQuery" :disabled="currentQueryId == maxQueryId - 1" class="btn-next">Next question</button>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-5 pl-md-2">
                <div class="card overflow-auto">
                    <div class="card-body ">
                        <div>
                            <div v-for="result in urlResults[queryIDs[currentQueryId]]" :key="result.url" class="mb-4 text-start">
                                <a :href="result.url" target="_blank" style="font-weight: bold;">{{ result.title }}</a>
                                <p class="text-black">{{ result.content }}</p>
                            </div>
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
        buttonText: "Search",
        currentQueryId: 0
        };
    },
    computed: {
    jsonData: {
        get() {
        console.log("jsonData:", this.$store.state.jsonData);
          return this.$store.state.jsonData;
        },
        set(value) {
          this.$store.dispatch('setJsonData', value);
        }
      },
    researchId: {
    get() {
      return this.$store.getters.researchId;
    },
    set(value) {
      this.$store.dispatch('setResearchId', value);
    }
  },
  queryIDs: {
      get() {
        return this.$store.state.queryIDs;
      },
      set(value) {
        this.$store.dispatch('setQueryID', value);
      }
    },
    queries: {
      get() {
        return this.$store.state.queries;
      },
      set(value) {
        this.$store.dispatch('setQueries', value);
      }
    },
    urlResults: {
      get() {
        return this.$store.state.urlResults;
      },
      set(value) {
        this.$store.dispatch('setUrlResults', value);
      }
    },
    urlSummaries: {
      get() {
        return this.$store.state.urlSummaries;
      },
      set(value) {
        this.$store.dispatch('setUrlSummaries', value);
      }
    },
    maxQueryId() {
      return this.queryIDs.length;
    }
    },
    created() {
    this.parsedata();
},
methods: {
    parsedata(){
        const data = this.jsonData;
        this.researchId = data[0];
        const queryData = data[1];
        for (const [queryId, value] of Object.entries(queryData)) {
            const query = value[0];
            const results = value[1];
    
            // Add the queryId to the list of queryIds
            this.queryIDs.push(queryId);
            // Add the query to the queries dictionary
            this.queries[queryId] = query;
            this.urlResults[queryId] = []; // Initialize an empty list for the results of this queryId
            
            for (const result of results) { // Go through the results
                if ('Summary' in result) {
                    // If the result is a summary, add it to the summaries dictionary
                    this.urlSummaries[queryId] = result.Summary;
                } else {
                    // Otherwise, add it to the list of results for this queryId
                    this.urlResults[queryId].push(result);
                }
            }
        }
    },
    nextQuery() {
            if (this.currentQueryId < this.maxQueryId - 1) {
                this.currentQueryId += 1;
            }
        },
        previousQuery() {
            if (this.currentQueryId > 0) {
                this.currentQueryId -= 1;
            }
        }
}
}   
</script>

<style scoped>
a {
  color: #007bff;
  text-decoration: none;
}
a:hover {
  color: #0056b3;
}
.text-black {
  color: #000000;
}
h3, p {
  word-wrap: break-word;
}
.card {
    height: calc(100vh - 18rem); /* Adjust as needed */
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
}
.card-content {
    overflow-y: auto;
  flex-grow: 1;
}
.card-footer {
    display: flex;
  justify-content: space-between;
}
.btn-prev {
  margin-left: 10px; /* Adjust as needed */
}

.btn-next {
  margin-right: 10px; /* Adjust as needed */
}
</style>