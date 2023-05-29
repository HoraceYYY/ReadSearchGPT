<script>
import { mapGetters } from 'vuex';

export default {
    data() {
      return {
        buttonText: "Start Searching",
        searchType: 'Quick Search',
      };
    },
created() {
  if (this.searchType === 'Quick Search') {
    this.$store.dispatch('setWidth', 8);
    this.$store.dispatch('setDepth', 0);
  } else if (this.searchType === 'Thorough Search') {
    this.$store.dispatch('setWidth', 5);
    this.$store.dispatch('setDepth', 1);
  }
  this.domain = "" 
},

watch: {
  searchType(newVal) {
    if (newVal === 'Quick Search') {
      this.$store.dispatch('setWidth', 8);
      this.$store.dispatch('setDepth', 0);
    } else if (newVal === 'Thorough Search') {
      this.$store.dispatch('setWidth', 5);
      this.$store.dispatch('setDepth', 1);
    }
  }
},

  computed: {
    ...mapGetters(['searchQueries', 'apiKey']),
    width: {
        get() {
            return this.$store.state.width;
        },
        set(value) {
            this.$store.dispatch('setWidth', value);
        }
    },
    depth: {
        get() {
            return this.$store.state.depth;
        },
        set(value) {
            this.$store.dispatch('setDepth', value);
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
startOver() {
      this.$router.push({ path: '/' });
    },

async submitForm() {
      if (!this.validateInput()) {
        return;
      }
      // add these lines

    await this.callApi();
    },

    validateInput() {
    var domain = this.domain; // Assuming 'this.domain' contains the user input

    // Trim leading and trailing white spaces
    domain = domain.trim();

    // Convert to lowercase
    domain = domain.toLowerCase();

    if (domain !== "") {

    // Regular expression for URL validation
    var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
        '(\\#[-a-z\\d_]*)?$','i'); // fragment locator

    // Check if URL is valid
    if (!pattern.test(domain)) {
        alert("Please enter a valid URL.");
        return false
    }
    }
    return true;
    },

    async callApi() {
        this.validateInput()
        const url = "https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/search";  // replace with your API endpoint
        const data = {
            searchWidth: this.width,
            max_depth: this.depth,
            searchDomain: this.domain.trim().toLowerCase(),
            searchqueries: this.searchQueries,
            apiKey: this.apiKey,
        };
        console.log(data)
        try {
            
            this.buttonText = "Searching...";
            //console.log(data);
            const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            });

            const jsonData = await response.json();

            // console.log(jsonData);
            this.jsonData = jsonData;  // assign jsonData directly
            // this.$store.dispatch('jsonData', jsonData);
            this.$router.push({ path: '/searching' });
            //handle your response here
        } catch (error) {
            this.buttonText = "Start Searching"
            console.error(error);
            alert(`There is an error duing the search: ${error}`);// handle error here
        }
    },
    }
}
</script>
 
<template>
  <div class="d-flex flex-column align-items-center justify-content-center">
        <form @submit.prevent="submitForm">
            <div class="input-group mb-3 radio-button-container">
                <div class="d-flex justify-content-center mb-3 gap-1">
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="quickSearch" value="Quick Search" v-model="searchType"/>
                        <label class="form-check-label" for="quickSearch">
                            <b>Quick Search</b><br />
                            <span class="form-text">Search 10's of websites within a few minutes.</span>
                        </label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="thoroughSearch" value="Thorough Search" v-model="searchType" />
                        <label class="form-check-label" for="thoroughSearch">
                            <b>Thorough Search</b><br />
                            <span class="form-text">Search 100's of websites in 10-20 mintues.</span>
                        </label>
                    </div>
                </div>
            </div>
            <div class="form mb-5 h5 text-start fw-bold w-100 domain-container">
              <label for="domain">Limit Search Within A Domain (optional):</label>
              <input type="text" id="domain" v-model="domain" class="form-control" placeholder="https://..." />
            </div>
            <div class="button-container d-flex justify-content-between mt-3">
              <div class="col-6">
                  <button type="submit" class="btn btn-outline-success btn-lg fw-bold w-100 narrower-button">{{ buttonText }}</button>
              </div>
              <div class="col-6">
                  <button type="button" @click="startOver" class="btn btn-outline-danger btn-lg w-100 narrower-button">Start Over</button>
              </div>
          </div>
        </form>
    </div>
</template>
  
<style scoped>
  .form-check-label{
      padding: 2em 0.4em;
      margin: 0.5em;
      border-radius: 10px;
      text-align: center;
      background: #bbb;
      color: #ffffff; 
      font-size: 28px;
      cursor: pointer;
      max-width: 400px;
  }
    .form-check-input {
    position: absolute;
    display: none;
    outline: none;
  }
  .form-text{
      font-style: italic;
      color: #ffffff;
    }
    .form-check-input:checked + .form-check-label {
        background: #4e9dc2;
    }
    .form-check-input:not(:checked) + .form-check-label {
        background: #bbb;
    }
    .form-check-input:not(:checked) + .form-check-label  {
    color: #aaa; /* change the text color to grey when not selected */
    }
    .form-check-input:checked + .form-check-label{
        color: #ffffff; /* change the text color to white when selected */
    }
    .form-check-input:not(:checked) + .form-check-label .form-text {
        color: #aaa; /* change the text color to grey when not selected */
    }
    .form-check-input:checked+.form-check-label .form-text{
        color: #ffffff; /* change the text color to white when selected */
    }
    .btn:hover {
        color: #ffffff;
    }

    .btn-outline-success:hover {
        background-color: #0c952c;
    }

    .btn-outline-danger:hover {
        background-color: #ff4800;
    }
    .domain-container {
    max-width: 1000px;  /* Set max-width as needed */
    margin: auto;
    text-align: left;
    padding: 0 15px;  /* Add padding */
    color: #ffffff;
    
  }
  .radio-button-container {
    max-width: 1000px;  /* Set max-width as needed */
    margin: auto;
  }
  .button-container {
    max-width: 1000px;  /* Set max-width */
    margin: auto;  /* Center the container */
    padding: 0 30px;  /* Add padding */
}

.button-container .col-6 {
    margin-bottom: 15px;
  
}
.narrower-button {
    max-width: 200px; /* Adjust the max-width as needed */
    width: 100%; /* Make the buttons occupy the full width of their containers */
  }

    @media (max-width: 576px) {
    .domain-container {
      font-size: 0.8rem;
      width: 85%;  /* Reduce width */
      margin: 10px auto;  /* Add some vertical margin */
    }

    .btn {
      font-size: 0.8rem;
      padding: 0.25rem 0.5rem;
      
    }

    .form-check-label {
      font-size: 0.8rem;
    }

    .narrower-button {
      max-width: 150px; /* Adjust the max-width as needed */
    }
    .button-container .col-6 {
        margin-bottom: 10px;
    }
}
  
</style>