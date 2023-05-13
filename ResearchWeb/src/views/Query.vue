<template>
    <div class="container">
      <div class="text-content">
        <p>Here are the search topics I will focus on: </p>
        <ul class="input-list">
          <li v-for="(item, index) in apiData" :key="index" class="input-item">
            <input v-model="apiData[index]" type="text" class="input">
            <button v-if="index !== 0" @click="removeItem(index)" class="minus-button">-</button>
            <button v-if="index === apiData.length - 1 && apiData.length < 5" @click="addItem" class="plus-button">+</button>
          </li>
        </ul>
        <p>Feel free to modify the search topic above. Once ready, click 'Search', or 'Start Over' to go back the previous page</p>
      </div>
      <div class="buttons">
      <button class="search-button">Search</button>
      <button class="start-over-button">Start Over</button>
    </div>
    </div>
  </template>


<script>
export default {
  data() {
    return {
      newItem: "", // For adding new items
      apiData: []  // Now apiData is a data property
    }
  },
  created() {
    // When the component is created, parse the API data and store it in apiData
    this.apiData = JSON.parse(this.$route.query.data || "[]");
  },
  computed: {
    newItemPlaceholder() {
      // If newItem is empty, return "Enter new item here.dssds.."
      // Otherwise, return an empty string
      return this.newItem === "" ? "Enter new item here.dssds.." : "";
    },
  },
  methods: {
    removeItem(index) {
      this.apiData.splice(index, 1);
    },
    addItem() {
    
    if (this.apiData.length < 5) {
      this.apiData.push(this.newItem);
      this.newItem = ""; // Clear the input field after adding the item
    }
  }
  }
};
</script>

  
<style scoped>
body {
    overflow: hidden; /* Prevent scrollbars */
  }
  
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 1vh; /* Use min-height instead of height */
    width: 100vw;
    margin-top: -25vh;
    padding: 0;
  }
  .text-content {
  padding-left: 20px;
  padding-bottom: 60px
  
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

.input-item input {
  font-style: italic; /* Makes the text italic */
}

.input-list {
  padding: 0;
  margin: 0;
  padding-bottom: 20px;
  padding-top: 20px
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
  width: 600px;
  height: 30px;
  border: 1px solid transparent; /* Add transparent border */
  outline: none;
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
.search-button, .start-over-button {
 margin-top: 30px;
    margin: 0 40px; /* Increase the left and right margin */
  padding: 15px 30px;
  font-size: 1.2em;
  
  cursor: pointer;
  transition: background-color 0.3s;
}
.start-over-button {
    border: 2px solid #ff4800;
  border-radius: 8px;
  background-color: #ffffff;
  color:  #ff4800;
}
.search-button{
    border: 2px solid #0c952c;
  border-radius: 8px;
  background-color: #ffffff;
  color:  #0c952c;
}
.search-button:hover{
background-color: #0c952c;
  color:  #ffffff;
}
.start-over-button:hover {
    background-color: #ff4800;
  color:  #ffffff;
}
</style>
