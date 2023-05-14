<script>

</script>

<template>
  <div class="container">
    <nav class="navbar">
      <div class="navbar-top">
        <div class="navbar-left">
          <router-link to="/" class="nav-link">New Search</router-link>
          <router-link to="/mysearch" class="nav-link">Find My Search</router-link>
        </div>
        <div class="navbar-right">
          <router-link to="/tutorial" class="nav-link">Watch Tutorial</router-link>
          <router-link to="/feedback" class="nav-link">Provide Feedback</router-link>
        </div>
      </div>
    </nav>

    <div class="content">
      <h1> (Re)Search </h1>
      
      <router-view class="router-view-class"/>

    </div>
    
    <nav class="navbar">  
      <div class="navbar-bottom-right">
        <router-link to="/privacy" class="nav-link">Privacy</router-link>
        <router-link to="/terms" class="nav-link">Terms</router-link>
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
  background-color: #f8f9fa;
  padding: 10px;
  max-height: 10vh; /* Adjust this value based on your needs */
  overflow-y: auto; 
}

.navbar-top {
  
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
  gap: 20px;
  overflow-y: auto; 
  padding-top: 9vh; /* Adjust this value to move content up or down */
  max-height: 80vh;
}
</style>
