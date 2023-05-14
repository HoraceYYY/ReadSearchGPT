<template>
    <div>
      <h1>Search Preference Page</h1>
      <p>Search queries: {{ searchQueries }}</p>
      <p>API Key: {{ apiKey }}</p>
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex';
  
  export default {
    computed: {
      ...mapGetters(['searchQueries', 'apiKey'])
    },
  };
  </script>
  

<style scoped>
</style>


<style scoped>

</style>