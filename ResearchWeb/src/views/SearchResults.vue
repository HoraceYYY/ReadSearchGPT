<template>
    <div class="container-fluid px-4">
        <div class="row d-flex">
            <div class="col-12 col-md-7 pr-md-2">
                <h2 class="card-header text-start">Research Summary</h2>
                <div class="card">
                    <div class="card-content">
                        <div class="mb-4 text-start text-black">
                            <h3 class="font-weight-bold query-title">{{ queries[queryIDs[currentQueryId]] }}</h3>
                            <p>{{ urlSummaries[queryIDs[currentQueryId]] }}</p>
                        </div>
                    </div>
                    <div class="card-footer">
                        <button @click="previousQuery" :class="{'invisible-button': currentQueryId === 0, 'btn-success': true}" >Previous</button>
                        <button @click="nextQuery" :class="{'invisible-button': currentQueryId === maxQueryId - 1, 'btn-success': true}" >Next</button>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-5 pl-md-2">
                <h2 class="card-header">Relevant Websites and Information</h2>
                <div class="card">
                    <div class="card-content">
                        <div>
                            <div v-for="result in urlResults[queryIDs[currentQueryId]]" :key="result.url" class="mb-4 text-start">
                                <a :href="result.url" target="_blank" style="font-weight: bold;">{{ result.title }}</a>
                                <p class="text-black">{{ result.content }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer">
                        <button class="btn-success">Download Report</button>
                        <button class="btn-success">Email Report</button>
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
        currentQueryId: 0,
        researchId: "",
        queryIDs: [],
        queries: {},
        urlResults: {},
        urlSummaries: {},
        };
    },
    computed: {
    maxQueryId() {
      return this.queryIDs.length;
    },
    jsonData: {
        get() {
            return this.$store.state.jsonData;
        },
        set(value) {
            this.$store.dispatch('setJsonData', value);
        }
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
    height: calc(100vh - 16rem); /* Adjust as needed */
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
}
.card-content {
    overflow-y: auto;
    padding: 12px;
  flex-grow: 1;
}
.card-footer {
    display: flex;
  justify-content: space-between;
  background-color: transparent;
}
.invisible-button {
  opacity: 0;
  pointer-events: none;
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
.query-title {
  text-transform: capitalize;
}

</style>