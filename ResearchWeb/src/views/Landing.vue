<template>
    <div class="container d-flex flex-column justify-content-center align-items-center text-center" style="min-height: 10vh;">
      <h1 class="display-4 mb-1 fw-bold">ReadSearch GPT</h1>  
      <h2 class="h3 mb-1 fw-bold" style="font-style: italic;">Use AI for online research</h2>
      <div class="card p-4 mb-4 mt-2 rounded shadow" style="max-width: 800px;">
        <div class="card-body">
          <!-- <h3 class="mb-4"></h3> -->
          <p class="lead">ReadSearch studies 10's - 100's of websites within 1 - 2 minutes to free you from spending hours sifting through online information.</p>
          <p class="lead">Your Privacy Matters. We DO NOT Track Your Personal Information.</p>
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
  h1, h2 {
    color: #5781c0; /* Using the primary color for headings */
  }
  </style>
  