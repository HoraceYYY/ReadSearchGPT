<template>
  <div class="d-flex flex-column min-vh-100">
    <nav class="navbar navbar-expand-lg">
        <div class="navbar-nav flex-row me-auto mb-2 mb-lg-0 fw-bold">
          <router-link to="/newsearch" class="nav-link">New Search</router-link>
          <router-link to="/mysearch" class="nav-link">Search History</router-link>
      </div>
    </nav>

    <main class="my-auto d-flex flex-column align-items-center justify-content-center text-center">
      <router-view  />
    </main>

    <nav class="navbar navbar-expand-lg">
      <div class="container-fluid navbar-buttom justify-content-between  mb-2 mb-lg-0">
        <div class="row-flex">
          <a href="https://mirage-oval-bce.notion.site/Tutorials-FAQs-d026f83b53c1471589ba8ff49445dc3e" class="nav-link" target="_blank">Tutorials & FAQs</a>
          <router-link to="/feedback" class="nav-link" >Provide Feedback</router-link>
        </div>
        <div>
          <a href="https://mirage-oval-bce.notion.site/Terms-8289e5d1596d45e49215df02bff2839f" class="nav-link" target="_blank">Privacy & Terms</a>
        </div>
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
  .row-flex {
    display: flex;
    flex-direction: row;
  }
  @media (max-width: 767px) {
    .navbar-nav {
    width: 100%; /* Ensures that the container of the links takes the full width */
    justify-content: space-between; /* Distributes space evenly between the links */
  }
  
  .navbar-nav .nav-link {
    text-align: center;
  }
  .navbar-buttom {
      flex-direction: row;
    }

    .navbar-buttom div {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
}

</style>
