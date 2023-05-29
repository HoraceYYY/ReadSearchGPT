<template>
    <div class="container d-flex flex-column justify-content-center align-items-center text-center" style="min-height: 10vh;">
      <div class="card p-4 mb-4 rounded shadow" style="max-width: 800px;">
        <div class="card-body">
          <h3 class="fw-bold mb-4">ReadSearch uses AI to do your online research.</h3>
          <p class="lead">Consider it as your personal research assistant. ReadSearch looks through 10's - 100's of websites on any topic you choose and summarizes all the information for you in a sharable format.</p>
          <p class="lead">ReadSearch frees you from spending hours sifting through online data and manually creating summaries. When the research is done, you can come back and simply download the results.</p>
        </div>
      </div>
      <button @click="goToNextPage" class="btn btn-lg btn-success">Let's Go</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      goToNextPage() {
        this.$router.push({ path: '/newsearch' });
      },
    },
  };
  </script>
  
  <style scoped>
  h3, .lead {
    color: #333;
  }
  .btn-success {
    background-color: #0c952c;
    border-color: #0c952c;
  }
  .btn-success:hover {
    background-color: #006c22;
    border-color: #006c22;
  }
  </style>
  