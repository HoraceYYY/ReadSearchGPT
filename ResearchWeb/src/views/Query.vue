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
          <p>Enter Open AI API Key: </p>
          <div class="input-item extra-input-item">
            <input v-model="apiKey" type="text" class="input" placeholder="API Key..">
        </div>

        </div>
        <div class="button-container">
          <button class="search-button" @click="search">{{ buttonText }}</button>
        </div>
      </div>
    </div>
  </template>

<script>
export default {
    
    data() {
      return {
        buttonText: "Search"
      };
    },

  created() {
    // Initialize data from the Vuex store
    this.searchqueries = this.$store.getters.searchQueries;
    this.apiKey = this.$store.getters.apiKey;
    },
  methods: {
    
    removeItem(index) {
      this.searchqueries.splice(index, 1);
    },
    addItem() {
    if (this.searchqueries.length < 5) {
        this.searchqueries.push("");
        }
    },
   async search() {
  try {
    // Check if any of the search queries are empty
    for (let i = 0; i < this.searchqueries.length; i++) {
            if (this.searchqueries[i].trim() === "") {
                alert("Please fill in all search query fields before submitting or remove the empty fields.");
                return;
            }
    }

    if (this.apiKey.trim() === "") {
      alert("Please fill in the API key field before submitting.");
      return;
    }
    // If all fields are filled in, proceed to the next page
    this.$store.dispatch('SearchQueries', this.searchqueries);
    this.$store.dispatch('ApiKey', this.apiKey);

    this.buttonText = "Checking...";

    const response = await this.callApi();
    if (response['Open AI Key'] === 'Valid') {
      this.$router.push({ path: '/preference' });
    } else {
      this.buttonText = "Search";
      alert("Please enter a valid API key");
      return;
    }

  } catch (error) {
    console.error(error);
  }
},
async callApi() {
    const url = "http://127.0.0.1:8000/testapi";  // replace with your API endpoint
    const payload = {
        apiKey: this.apiKey,
    };
    try {
        const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
     
        return data;
        //handle your response here
    } catch (error) {
        this.buttonText = "Search"
        console.error(error);
        alert(`There is an error which cheking the api key: ${error}. Please try again! `);// handle error here
    }
},

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
  margin-top: -40px;
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
  font-size: 20px; /* Adjust size as needed */
}
.text-content p {
  margin-left: -20px;
  font-weight: bold; /* Makes the text bold */
  width: 800px;
}

.input-list {
  padding: 0;
  margin: 0;
  padding-bottom: 5px;
  padding-top: 5px;
  height: 200px;
}

.input-item {
  list-style: none;
  position: relative;
  margin-bottom: 5px;

}

.input-item::before {
  content: "• ";
  position: absolute;
  left: -20px;
  top: 50%;
  transform: translateY(-50%);
}
.input-item.extra-input-item::before {
  content: ""; /* Overriding the bullet point */
}
.input-item.extra-input-item {
  margin-left: -20px;
  width:100% ;
}
.input-item input {
    font-style: italic;
  width:80% ;
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
  margin-top: -10px;
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
