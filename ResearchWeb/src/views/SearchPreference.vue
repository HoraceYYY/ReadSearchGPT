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
        // console.log(data)
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
    <div class="form-container">
      <form @submit.prevent="submitForm">
        <div class="input-group">
            <div class="radio-group">
              <input type="radio" id="quickSearch" value="Quick Search" v-model="searchType" class="radio-input_Quick"/>
              <label for="quickSearch" class="radio-label">
                Quick Search
                <span class="description">Search 10's of websites within a few minutes.</span>
            </label>

              <input type="radio" id="thoroughSearch" value="Thorough Search" v-model="searchType" class="radio-input_Thorough" />
              <label for="thoroughSearch" class="radio-label">
                Thorough Search
                <span class="description">Search 100's of websites in 10-20 mintues.</span>
            </label>
            </div>
        </div>
        <div class="input-group">
          <label for="domain" class="input-label">Limit Search Within A Domain (optional):</label>
          <input type="text" id="domain" v-model="domain" class="text-input" placeholder="https://..." />
        </div>
        <div class="button-container">
          <button type="submit" class="search-button">{{ buttonText }}</button>
          <button type="button" @click="startOver" class="startover-button">Start Over</button>
        </div>
      </form>
    </div>
</template>
  
  <style scoped>
  .form-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: -40px;
  }
.form-container p{
  font-family: Arial, sans-serif; /* Substitute with your preferred font */
  font-size: 20px; /* Adjust size as needed */
  margin-left: -160px;
  font-weight: bold; /* Makes the text bold */
  width: 800px;
  margin-bottom: 40px;
}

.input-group{
  width: 900px;
  margin-bottom: 50px;
  font-family: Arial, sans-serif; /* Substitute with your preferred font */
  font-size: 20px;
  font-weight: bold;
  }
 
 .text-input {
    margin: 10px 0;
    font-style: italic;
    font-family: Arial, sans-serif; /* Substitute with your preferred font */
  font-size: 18px;
  width: 96%;
  padding: 10px;
  }
  .radio-group {
  margin-top: 50px;
  display: flex;
  justify-content: center;
  margin-bottom: 1em;
  gap: 50px;
}
  .radio-label {
  display: block;
  padding: 3em 0.8em;
  margin: 0.5em;
  border: 2px solid #aaa;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  background: #bbb;
  color: #ffffff;
  font-size: 28px;
}
.description {
    display: block;
    font-size: 15px; /* Change this value to your desired size */
    margin-top: 20px;
    font-style: italic;
}
/* Style the input elements (hidden) */
.radio-input_Quick, .radio-input_Thorough {
  display: none;
}

/* Style when Quick Search is selected */
.radio-input_Quick:checked + .radio-label {
  background:#4e9dc2;
}

/* Style when Thorough Search is selected */
.radio-input_Thorough:checked + .radio-label {
  background: #4e9dc2;
}

/* If you want to grey out the unselected option, use these styles: */
.radio-input_Quick:not(:checked) + .radio-label {
  background: #bbb;
  cursor: pointer;
  color: #aaa;
}

.radio-input_Thorough:not(:checked) + .radio-label {
  background: #bbb;
  cursor: pointer;
  color: #aaa;
}

  .button-container {

    display: flex;
  justify-content: center;
  gap: 160px; /* Adjust the spacing between buttons as needed */
  margin-top: 40px; /* Add margin to the top */
  }
  
  .search-button {
    border: 2px solid #0c952c;
  border-radius: 8px;
  background-color: #ffffff;
  color: #0c952c;
    padding: 15px 28px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    font-weight: bold;
  }
  
  .startover-button {
    border: 2px solid #ff4800;
  border-radius: 8px;
  background-color: #ffffff;
  color: #ff4800;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
  }

  .search-button:hover {
  background-color: #0c952c;
  color: #ffffff;
}

.startover-button:hover {
  background-color: #ff4800;
  color: #ffffff;
}


  </style>
  


