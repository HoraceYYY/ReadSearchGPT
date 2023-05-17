<template>
    <div class="container">
      <form @submit.prevent="startSearch">
        <div class="form-row">
          <label for="userAsk" class="input-label">What would you like to (re)search?</label>
          <textarea id="userAsk" v-model="userAsk" rows="15" cols="100" wrap="soft" spellcheck="false" class="textbox"></textarea>
        </div>
        <div class="form-row">
          <label for="apikey" class="input-label">Enter Open AI API Key</label>
          <input id="apikey" v-model="apikey" type="text" autocomplete="off" class="textbox">
        </div>
        <div class="center-button">
          <button type="submit" class="start-button">{{ buttonText }}</button>
        </div>
      </form>
    </div>
  </template>
  
  

  <script>
  export default {
    data() {
      return {
        userAsk: "",
        apikey: "",
        buttonText: "Start"  // Initial button text
      };
    },
    methods: {
      async startSearch() {
        try {
          // Perform API call with form data
          
          const requestData = {
            userAsk: this.userAsk,
            //apikey: this.apikey
          };
          // chech if userAsk is empty
          if (this.userAsk === "") {
            alert("Please enter a question");
            return;
          }
          // if (this.apikey === "") {
          //   alert("Please enter a question");
          //   return;
          // }

          // Make the asynchronous API call
          const response = await this.makeAPIcall(requestData);

          // Handle the response and navigate to another page if needed
          if (response.success) {
            this.$router.push({
            path: "/query",
            query: { data: JSON.stringify(response.data) } // Pass the data as a query parameter
          });
          } else {
            // Handle error or display error message
            console.log(response.error);
          }
        } catch (error) {
          // Handle error or display error message
          console.log(error);
          this.buttonText = "Start"; 
        }
      },
      async makeAPIcall(requestData) {
        // TODO: Implement your API call logic here using the requestData
        // Example using fetch API:
        this.buttonText = "Searching...";
        const response = await fetch("http://127.0.0.1:8000/queries", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(requestData)
        });
  
        const data = await response.json();
        return data; // Return the API response data
      }
    }
  };
  </script>
  

<style scoped>
.container {
  margin-top: 3vh; /* Adjust this value to move the form lower */
}
body {
  background-color: #ffffff;
}

.form-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.textbox {
  border: 1.5px solid #007bff;
  font-size: 16px;
}
.input-label {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #007bff;
}


.center-button {

  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.start-button {
    padding: 15px 30px;
  font-size: 1.2em;
  border: 2px solid #007bff;
  border-radius: 8px;
  background-color: #ffffff;
  color:  #007bff;
  cursor: pointer;
  transition: background-color 0.3s;
}

.start-button:hover {
  background-color: #0056b3;
  color:  #ffffff;
}


</style>