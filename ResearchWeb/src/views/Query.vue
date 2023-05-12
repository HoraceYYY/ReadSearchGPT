<template>
    <div>
      <h2>Data from API:</h2>
      <pre>{{ apiData }}</pre>
    </div>
  </template>
  
  <script>
  export default {
    computed: {
      apiData() {
        return JSON.parse(this.$route.query.data || "{}");
      }
    }
  };
  </script>
  

<style scoped>

</style>