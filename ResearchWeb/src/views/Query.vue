<template>
  <h1 class="display-4 mb-1 fw-bold">ReadSearch GPT</h1>  
  <h2 class="h3 mb-1 fw-bold" style="font-style: italic;">Use AI for online research</h2>
  <div class="container pt-0 d-flex justify-content-center align-items-center" style="min-height: 1vh;"> 
    <div class="card p-4 mb-4 mt-1 rounded shadow" style="position: relative; max-width: 1000px; width: 100%;">
      <div v-if="isLoading" class="overlay">
        <p class="loading-text">Your research will take about 1-2 minutes.</p>
      </div>
      <div class="card-body">
        <h5 class="fw-bold mb-3 text-start ">Enter Research Topics:</h5>
        <div class="input-group mb-3" v-for="(item, index) in searchQueries" :key="index">
          <input type="text" class="form-control" v-model="searchQueries[index]" @input="addItemAuto" placeholder="Up to 3 Research Topics... " aria-label="Research Topic">
        </div>
        <!-- <h5 class="fw-bold mb-3 text-start ">Enter A Website Domain to Narrow the Search:</h5>
        <div class="input-group mb-3">
          <input type="text" class="form-control" v-model="domain" placeholder="https://example.com or leave blank to search the enter internet" aria-label="Domain">
        </div> -->
        <h5 class="fw-bold mb-3 text-start ">Enter Open AI API Key:</h5>
        <div class="input-group mb-3">
          <input :type="passwordFieldType" v-model="apiKey" class="form-control" placeholder="API Key..." aria-label="API Key">
          <button class="btn btn-outline-dark" type="button" @click="togglePasswordField">{{ passwordFieldType === 'password' ? 'Show' : 'Hide' }}</button>
        </div>
        <a href="https://mirage-oval-bce.notion.site/Tutorials-FAQs-d026f83b53c1471589ba8ff49445dc3e" target="_blank" rel="noopener noreferrer" aria-label="Opens in a new tab" class="mb-3 d-inline-block text-center w-100">How to get an API key?</a>
        <div class="d-grid gap-2">
          <button class="btn btn-lg btn-success text-white" @click="search">{{ buttonText }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    data() {
      return {
        buttonText: "Search",
        passwordFieldType: "password",
        isLoading: false
      };
    },
    created() {
  this.searchQueries = [""],//clear the input from previous input of the same session
  this.apiKey = "", //clear the input from previous input of the same session
  this.domain = "" 
},
computed: {
  searchQueries: {
    get() {
      return this.$store.state.searchQueries;
    },
    set(value) {
      this.$store.dispatch('setSearchQueries', value);
    }
  },
  apiKey: {
    get() {
      return this.$store.getters.apiKey;
    },
    set(value) {
      this.$store.dispatch('ApiKey', value);
    }
  },
  domain: {
      get() {
          return this.$store.state.domain;
      },
      set(value) {
          this.$store.dispatch('setDomain', value);
      }
  },
  jsonData: {
        get() {
            return this.$store.state.jsonData;
        },
        set(value) {
            this.$store.dispatch('setJsonData', value);
        }
    }
},
methods: {
    togglePasswordField() {
     this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
   },
    addItemAuto() {
      if (this.searchQueries.length < 3 && this.searchQueries[this.searchQueries.length - 1] !== "") {
          this.searchQueries.push("");
          this.searchQueries = [...this.searchQueries];
      }
    },
    validateInput() {
    var domain = this.domain; // Assuming 'this.domain' contains the user input
    domain = domain.trim();
    domain = domain.toLowerCase();
    if (domain !== "") { // Regular expression for URL validation
    var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
        '(\\#[-a-z\\d_]*)?$','i'); // fragment locator

    // Check if URL is valid
    if (!pattern.test(domain)) {
        return false
      }
    }
    return true;
    },
async search() {
  try {
    const filteredQueries = this.searchQueries.filter(query => query.trim() !== "");
    // Check if any of the search queries are empty
    if (filteredQueries.length === 0) { 
      alert("Please enter at least one research topic before submitting.");
      return;
    }
    //check if web url makes sense
    if (!this.validateInput()) {
      alert("Please enter a valid url.");
        return;
      }

    //check if api key is good
    if (this.apiKey.trim() === "") {
      alert("Please fill in the API key field before submitting.");
      return;
    }
    this.isLoading = true;
    // If all fields are filled in, start calling api
    this.searchQueries = [...filteredQueries];
    this.buttonText = "Checking Key...";

    const response = await this.testApi();
    if (response['Key'] === 'Valid') {
      // console.log(this.searchQueries)
      // console.log(this.domain)
      await this.checkCookie();
      await this.firstSearch()
      this.isLoading = false;
    } else {
      this.buttonText = "Search";
      this.isLoading = false;
      alert("Please enter a valid API key");
      return;
    }
  } catch (error) {
    console.error(error);
  }
},
async testApi() {
    // console.log(this.searchQueries)
    const trimmedApiKey = this.apiKey.trim();
    const url = "https://readsearchgpt.com/api/testapi";  // replace with your API endpoint
    const payload = {
        apiKey: trimmedApiKey,
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
      this.buttonText = "Search";
    console.error('API key check failed:', error); // Print detailed error information
    alert(`There is an error when checking the API key. Please try again! Error: ${error}`); // Show detailed error message
  }
},
async firstSearch(){
  const url = "https://readsearchgpt.com/api/firstsearch";  // replace with your API endpoint
  const data = {
      searchqueries: this.searchQueries,
      searchDomain: this.domain.trim().toLowerCase(),  
      apiKey: this.apiKey,
    };
    //console.log(data)
    try {
      this.buttonText = "Searching...";
      const response = await fetch(url, {
      method: 'POST',
      credentials: 'include',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      });
      const jsonData = await response.json();
      this.jsonData = jsonData;  // assign jsonData directly
      this.$router.push({ path: '/searchresults' });
      } catch (error) {
          this.isLoading = false;
          this.buttonText = "Search"
          console.error(error);
          alert(`There is an error duing the search: ${error}`);// handle error here
      }
  },
  async checkCookie() {
      const url = "https://readsearchgpt.com/api/read-cookie"; // replace with your API endpoint
      try {
          const response = await fetch(url, {
              method: 'GET',
              credentials: 'include', // to include cookies
          });

          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const data = await response.json();
          if (!data.userid || data.userid === null) {
              await this.createCookie(); // If no cookie is present, create one.
          }

      } catch (error) {
          console.error('API call failed:', error);
      }
  },
  async createCookie() {
      const url = "https://readsearchgpt.com/api/create-cookie"; // replace with your API endpoint
      try {
          const response = await fetch(url, {
              method: 'GET',
              credentials: 'include', // to include cookies
          });

          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }

      } catch (error) {
          console.error('API call failed:', error);
      }
  },
}
}
</script>
  
<style scoped>
@keyframes fade {
  0% {opacity: 1;}
  50% {opacity: 0.2;}
  100% {opacity: 1;}
}

.loading-text {
  margin-bottom: 40px;
  color: #032152;
  font-size: 2em;
  animation: fade 3s linear infinite; 
}
.overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.form-control{
  font-style: italic;
}
@media (max-width: 768px) {
  .loading-text {
    font-size: 1.2em; /* size for smaller screens */
  }
  h5, .btn, .form-control {
    font-size: 0.9rem;
  }
}
h5, .btn, .form-control {
  color: #333;
}
.btn-success {
  background-color: #0c952c;
  border-color: #0c952c;
  color: #ffffff;
}
.btn-success:hover {
  background-color: #006c22;
  border-color: #006c22;
}
h1, h2 {
    color: #5781c0; /* Using the primary color for headings */
  }
</style>