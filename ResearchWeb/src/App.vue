<template>
  <div class="d-flex flex-column min-vh-100">
    <nav class="navbar navbar-expand-lg">
      <div class="container-fluid">
        <div class="navbar-nav me-auto mb-2 mb-lg-0 fw-bold">
          <router-link to="/newsearch" class="nav-link">New Search</router-link>
          <router-link to="/mysearch" class="nav-link">Find My Results</router-link>
        </div>
        <div class="navbar-nav mb-2 mb-lg-0 ">
          <a href="https://mirage-oval-bce.notion.site/Tutorials-FAQs-d026f83b53c1471589ba8ff49445dc3e" class="nav-link" target="_blank">Tutorials & FAQs</a>
          <router-link to="/feedback" class="nav-link">Provide Feedback</router-link>
        </div>
      </div>
    </nav>

    <main class="my-auto d-flex flex-column align-items-center justify-content-center text-center">
      <h1 class="display-4 mb-3 fw-bold">ReadSearch GPT</h1>
      <h2 class="h3 mb-5">Your AI Assistant for Online Research!</h2>
      <router-view  />
    </main>

    <nav class="navbar navbar-expand-lg">
      <div class="container-fluid justify-content-end navbar-nav">
        <!-- <a href="https://mirage-oval-bce.notion.site/Terms-8289e5d1596d45e49215df02bff2839f" class="nav-link" target="_blank">Privacy</a> -->
        <a href="https://mirage-oval-bce.notion.site/Terms-8289e5d1596d45e49215df02bff2839f" class="nav-link" target="_blank">Privacy & Terms</a>
      </div>
    </nav>
  </div>
</template>

<style scoped>
  .navbar, .navbar a, .navbar a:hover {
    background-color: #333; /* A dark grey color */
    color: #ddd; /* A light shade of grey */
    padding: 0.25rem 1rem; /* Reduce the vertical padding to make the navbar thinner */
  }

  .navbar a:hover {
    color: #0c952c; /* Primary color for hover effect */
  }

  main {
    background-color: #222; /* Very dark grey for main background */
    color: #ddd; /* A light shade of grey for main text */
  }

  h1, h2 {
    color: #5781c0; /* Using the primary color for headings */
  }

  .d-flex {
    background-color: #222; /* Same dark grey for the overall background */
  }
</style>
