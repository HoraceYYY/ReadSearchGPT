<script>
import { mapGetters } from 'vuex';

export default {
    data() {
      return {
        buttonText: "Search"
      };
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
      if (!this.validateFormData()) {
        return;
      }
      // add these lines

    await this.callApi();
    },
    validateFormData() {
      if (this.depth == 3 && this.domain == "") {
        if (!confirm("You are about to perform a deep search without limiting the search domain. This may take hours with high Open AI api cost. Do you wish to proceed?")) {
          return false;
        }
      }

      if (this.domain != "" && !this.domain.startsWith("http")) {
        alert("Please enter a valid domain starting with http or https");
        return false;
      }

      return true;
    },
    async callApi() {
        const url = "http://127.0.0.1:800/search";  // replace with your API endpoint
        const data = {
            width: this.width,
            depth: this.depth,
            domain: this.domain,
            searchQueries: this.searchQueries,
            apiKey: this.apiKey,
        };
        try {
            this.buttonText = "Searching...";
            console.log(data);
            const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            });

            if (!response.ok) {
            this.buttonText = "Search"
            throw new Error(`HTTP error! status: ${response.status}`);

            }

            const jsonData = await response.json();
            await this.$store.dispatch('setJsonData', jsonData);

            console.log(jsonData);
            this.$router.push({ path: '/searching' });
            //handle your response here
        } catch (error) {
            this.buttonText = "Search"
            console.error(error);
            alert(`There is an error duing the search: ${error}`);// handle error here
        }
    },
    }
};
</script>

  
<template>
    <div class="form-container">
      <form @submit.prevent="submitForm">
        <div class="input-group">
          <label for="width" class="input-label">
            <span class="tooltip">ℹ️
            <span class="tooltip-text">This sets the number of search engine results for each search topic.</span>
            </span> 
            # of Initial Search Results (Per Topic): {{ width }}
        </label>
          <input type="range" id="width" min="1" max="10" v-model="width" class="slider" />
        </div>
        <div class="input-group">
            <label for="depth" class="input-label">
                <span class="tooltip">ℹ️
                <span class="tooltip-text">Level of webpage exploration by following links found on webpages.</span>
                </span>
                Additional Search results:
            </label>
            <select id="depth" v-model="depth" class="dropdown">
                <option value="0">None: Only search initial results (~1min, 10s URLs)</option>
                <option value="1">Quick: Search relevant links found from the initial results (>10min, 100s URLs)</option>
                <option value="2">Thorough: Search relevant links from Quick Option (>1h, 1000s URLs)</option>
                <option value="3">Deep: Search relevant links from Thorough Option (do NOT recommend without limiting the search domain) </option>
            </select>
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
    <!-- <p>Search queries: {{ searchQueries }}</p>
    <p>API Key: {{ apiKey }}</p> -->
</template>
  
  <style scoped>
  .form-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  .input-group, .dropdown{
    width: 900px;
    margin-bottom: 20px;
    font-family: Arial, sans-serif; /* Substitute with your preferred font */
  font-size: 20px;
  }
 
  .slider, .dropdown{
    width: 100%; 
  }
  .text-input {
    width: 96%;
  }
  .slider, .dropdown, .text-input {
    margin: 10px 0;
    font-style: italic;
    font-family: Arial, sans-serif; /* Substitute with your preferred font */
  font-size: 18px;
  }
  
  .text-input, .dropdown{
    padding: 10px;
  }

  .tooltip {
  position: relative;
  display: inline-block;
  margin-left: 4px;
}

.tooltip .tooltip-text {
  visibility: hidden;
  width: 180px;
  background-color: #000;
  color: #fff;
  text-align: center;
  border-radius: 4px;
  padding: 4px;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltip:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}
  
  .button-container {

    display: flex;
  justify-content: center;
  gap: 120px; /* Adjust the spacing between buttons as needed */
  margin-top: 80px; /* Add margin to the top */
  }
  
  .search-button {
    border: 2px solid #0c952c;
  border-radius: 8px;
  background-color: #ffffff;
  color: #0c952c;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
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
  


