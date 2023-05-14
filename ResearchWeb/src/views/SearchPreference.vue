<template>
    <div>
      <h1>Search Preference Page</h1>
      <p>Search queries: {{ searchqueries }}</p>
      <p>API Key: {{ apikey }}</p>
    </div>
  </template>
  
  <script>
  export default {
    props: ['searchqueries', 'apikey'],
  data() {
    return {
      // no need to initialize 'searchqueries' and 'apikey' here
    }
  },
  created() {
    console.log(this.searchqueries);
    console.log(this.apikey);
  }
}

</script>

<style scoped>

</style>