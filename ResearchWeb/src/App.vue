<script>

</script>

<template>
  <div class="container">
    <nav class="navbar">
      <div class="navbar-top">
        <div class="navbar-left">
          <router-link to="/newsearch" class="nav-link">New Search</router-link>
          <router-link to="/mysearch" class="nav-link">Find My Results</router-link>
        </div>
        <div class="navbar-right">
          <!-- <router-link to="/tutorial" class="nav-link">Tutorials & FAQs</router-link> -->
          <a href="https://mirage-oval-bce.notion.site/Tutorials-FAQs-d026f83b53c1471589ba8ff49445dc3e" class="nav-link" target="_blank">Tutorials & FAQs</a>
          <router-link to="/feedback" class="nav-link">Provide Feedback</router-link>
        </div>
      </div>
    </nav>

    <div class="content">
      <h1 class="title">ReadSearch</h1>
      <h2 class="subtitle">Your AI Assistant for Online Research!</h2>
      <router-view class="router-view-class" />
    </div>
    
    <nav class="navbar">  
      <div class="navbar-bottom-right">
        <a href="https://mirage-oval-bce.notion.site/Terms-8289e5d1596d45e49215df02bff2839f" class="nav-link" target="_blank">Terms</a>
      <a href="https://mirage-oval-bce.notion.site/Privacy-354ba4e4b7f94e218ea4cbfad27b751a" class="nav-link" target="_blank">Privacy</a>
        <!-- <router-link to="/privacy" class="nav-link">Privacy</router-link>
        <router-link to="/terms" class="nav-link">Terms</router-link> -->
      </div>
    </nav>
  </div>
</template>


<style scoped>

html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}

h1 {
  font-size: 3em; /* Adjust this value to change the size of the text */
}
.container {
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  justify-content: space-between;
}

.navbar {
  flex-shrink: 0;
  background-color: #ffffff;
  padding: 15px;
  max-height: 10vh; /* Adjust this value based on your needs */
  overflow-y: auto; 
  font-family: Arial, sans-serif;
  font-style: italic;
  color: #2e2b2b;
  
}
.navbar-left{
  font-size: 20px;
  font-weight: bold;
  text-decoration: underline;
  text-underline-offset: 0.2em;
}
.navbar-right{
  font-size: 20px;
  font-weight: bold;
}

.navbar-bottom-right {
  font-size: 18px;
  display: flex;
  gap: 20px;
}
.navbar-top {
  margin-top: 0px;
  display: flex;
  justify-content: space-between;
}

.navbar-left, .navbar-right, .navbar-bottom-right {
  display: flex;
  gap: 20px;
}

.navbar-bottom-right {
  flex-shrink: 0;
  justify-content: flex-end;
}

.nav-link {
  text-decoration: none;
  color: #333;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  flex-grow: 1;
  overflow-y: auto; 
  padding-top: 1vh; /* Adjust this value to move content up or down */
  max-height: 80vh;
}

.title {
  font-size: 3em;
  margin-bottom: -20px; /* Adjust the value to make the spacing smaller */
  color: rgb(0, 26, 130);
}

.subtitle {
  font-size: 1.8em;
  margin-bottom: 60px;
  color:  rgb(0, 26, 130);
}
</style>
