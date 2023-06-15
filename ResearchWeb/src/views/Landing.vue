<template>
    <div class="container d-flex flex-column justify-content-center align-items-center text-center" style="min-height: 10vh;">
      <div class="card p-4 mb-4 rounded shadow" style="max-width: 800px;">
        <div class="card-body">
          <!-- <h3 class="mb-4"></h3> -->
          <p class="lead">As your personal AI research assistant, ReadSearch studies 10's - 100's of websites on any topic and summarizes all the information for you.</p>
          <p class="lead">ReadSearch frees you from spending hours sifting through online information and manually creating summaries.</p>
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
  