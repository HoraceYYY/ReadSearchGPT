<template>
    <div class="welcome-container">
      <div class="welcome-text">
        <h3>ReadSearch uses AI to do your online research. </h3>
        <h3>Think of it as your own research assistant. ReadSearch looks through 10's - 100's of websites on any topic you like, and summarize all the information for you while you do other things. </h3>
        <h3>When it's done, you can easily download the results.</h3>
      </div>

    </div>
    <div class="search-button">
        <button @click="goToNextPage">Let's Go</button>
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
  .welcome-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    text-align: center;
    background: #FFFFFF;
    box-shadow: 0px 0px 30px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    max-width: 1000px;
    margin: 30px auto;
    font-size: 20px;
  }
  
  .welcome-text {
    width: 90%;
    background-color: #ffffff;
    color:  rgb(0, 0, 0);
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 30px;
    font-style: italic;
  }

  .search-button button {
    padding: 15px 50px;
    font-size: 1.2em;
    cursor: pointer;
    transition: background-color 0.3s;
    border: 2px solid #0c952c;
    border-radius: 8px;
    background-color: #FFFFFF;
    color: #0c952c;
    font-weight: bold;
  }
  
  .search-button button:hover {
    background-color: #0c952c;
    color: #FFFFFF;
  }
  </style>
  