<template>
    <div class="main-container">
      <div class="content-container">
        <div class="text-content">
          <p>Enter the search topic below: </p>
          <ul class="input-list">
            <li v-for="(item, index) in searchqueries" :key="index" class="input-item">
              <input v-model="searchqueries[index]" type="text" class="input" placeholder="Enter your search query here...">
              <button v-if="index !== 0" @click="removeItem(index)" class="minus-button">-</button>
              <button v-if="index === searchqueries.length - 1 && searchqueries.length < 5" @click="addItem" class="plus-button">+</button>
            </li>
          </ul>
        </div>
        <div class="button-container">
          <button class="search-button" @click="search">Search</button>
        </div>
      </div>
    </div>
  </template>

<script>
export default {
  data() {
    return {
      newItem: "", 
      searchqueries: [""]  // Initialize searchqueries with one empty string
    }
  },
  methods: {
    removeItem(index) {
      this.searchqueries.splice(index, 1);
    },
    addItem() {
    if (this.searchqueries.length < 5) {
      this.searchqueries.push(this.newItem);
      this.newItem = "";
    }
  },
    async makeAPIcall(requestData) {
      const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
      });

      const data = await response.json();
      return data;
    },
    async search() {
      try {
        const response = await this.makeAPIcall(this.searchqueries);
        console.log(response);
        this.$router.push('/searching');
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

  
<style scoped>
body {
    overflow: hidden; /* Prevent scrollbars */
  }
  .main-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  height: 100vh;
  padding-top: 50px; /* Adjust this as needed */
}

.content-container {
  margin-top: -40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

  .text-content {
  padding-left: 20px;
  padding-bottom: 40px
  
   /* This should match the left positioning of .input-item::before */
}

.text-content p, .input-item input {
  font-family: Arial, sans-serif; /* Substitute with your preferred font */
  font-size: 16px; /* Adjust size as needed */
}
.text-content p {
  margin-left: -20px;
  font-weight: bold; /* Makes the text bold */
  width: 800px;
}

.input-list {
  padding: 0;
  margin: 0;
  padding-bottom: 20px;
  padding-top: 5px
}

.input-item {
  list-style: none;
  position: relative;
  margin-bottom: 15px;
}

.input-item::before {
  content: "• ";
  position: absolute;
  left: -20px;
  top: 50%;
  transform: translateY(-50%);
}

.input-item input {
    font-style: italic;
  width: 600px;
  height: 30px;
  border: 1px solid transparent; /* Add transparent border */
  outline: none;
  word-wrap: break-word; /* Add this line */
  overflow-wrap: break-word; /* Add this line, for better compatibility with different browsers */
  white-space: pre-wrap; /* Add this line to preserve line breaks and spaces */
}

.input-item input:focus {
  border: 1px solid #515151;
}

.minus-button, .plus-button {
  
  border: none; /* Remove border */
  cursor: pointer; /* Hand cursor on hover */
  padding: 5px 10px; /* Padding around text */
  text-align: center; /* Center the text */
  text-decoration: none; /* Remove underline */
  display: inline-block; /* Make them inline elements */
  font-size: 14px; /* Increase font size */
  margin-left: 20px; /* Add some margin to the left side of the buttons */
  transition-duration: 0.4s; /* Add animation when hovering */
}


.minus-button {
    color:#ff4800; /* White text */
  background-color: #ffffff;
  border: 1px solid #ff4800; /* Adds a border */
  border-radius: 5px; /* Adds rounded corners */
}

.plus-button {
    color: #0c952c; /* White text */
  background-color: #ffffff;
  border: 1px solid #0c952c; /* Adds a border */
  border-radius: 5px; /* Adds rounded corners */

}

.minus-button:hover {
    color: #ffffff;
  background-color: #ff4800;
}

.plus-button:hover {
    color: #ffffff;
  background-color: #0c952c;
}
.search-button {
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-button {
  margin-top: 0px;
  padding: 15px 30px;
  font-size: 1.2em;
  cursor: pointer;
  transition: background-color 0.3s;
  border: 2px solid #0c952c;
  border-radius: 8px;
  background-color: #ffffff;
  color: #0c952c;
}

.search-button:hover {
  background-color: #0c952c;
  color: #ffffff;
}

</style>