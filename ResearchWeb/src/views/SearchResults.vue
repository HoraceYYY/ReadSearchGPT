<template>
    <div>
      <h1>Research ID: {{ researchID }}</h1>
      <div v-for="queryId in queryIDs" :key="queryId">
        <h2>Query: {{ queries[queryId] }}</h2>
        <h3>Results:</h3>
        <div v-for="result in urlResults[queryId]" :key="result.url">
          <a :href="result.url">{{ result.title }}</a>
          <p>{{ result.content }}</p>
        </div>
        <h3>Summary:</h3>
        <p>{{ urlSummaries[queryId] }}</p>
      </div>
    </div>
  </template>

<script>
export default {
    data() {
      return {
        buttonText: "Search",
        researchID: "", // a string of research ID
        queryIDs: [], // a list of query ID 
        queries: {}, //a dictionary of queryID:query
        urlResults: {}, //a dict of queryID: [url, title, content]
        urlSummaries: {}, // a dict of queryID: summary
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
    },
    created() {
    this.parsedata();
},
methods: {
    parsedata(){
        const data = this.jsonData;
        this.researchID = data[0];
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
    }
}
}   
</script>

  
<style scoped>

</style>