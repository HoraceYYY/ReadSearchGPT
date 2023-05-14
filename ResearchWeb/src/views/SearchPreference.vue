<template>
    <div>
      <h1>Search Preference Page</h1>
      <p>Search queries: {{ SearchQueries }}</p>
      <p>API Key: {{ apiKey }}</p>
    </div>
</template>
  
<script>
export default {
  
  data() {
    return {
        SearchQueries: [],
        apiKey: ""
    }
  },
  created() {
    this.SearchQueries = JSON.parse(this.$route.query.searchqueries || "[]")
    this.apiKey = this.$route.query.apikey || ""
  }
}
</script>

<style scoped>
</style>


<style scoped>

</style>