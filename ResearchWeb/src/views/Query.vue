<template>
  <div class="container pt-0 d-flex justify-content-center align-items-center" style="min-height: 1vh;">
    <div class="card p-4 mb-4 rounded shadow" style="max-width: 1000px; width: 100%;">
      <div class="card-body">
        <h5 class="fw-bold mb-3 text-start ">Research Topics:</h5>
        <div class="input-group mb-3" v-for="(item, index) in searchqueries" :key="index">
          <input type="text" class="form-control" v-model="searchqueries[index]" @input="addItemAuto" placeholder="Up to 5 research topics..." aria-label="Research Topic">
        </div>
        <h5 class="fw-bold mb-3 text-start ">Open AI API Key:</h5>
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
        buttonText: "Start",
        passwordFieldType: "password"
      };
    },
    created() {
  this.searchqueries = [""]//clear the input from previous input of the same session
  this.apiKey = "" //clear the input from previous input of the same session
},
computed: {
  searchqueries: {
    get() {
      return this.$store.getters.searchQueries;
    },
    set(value) {
      this.$store.dispatch('SearchQueries', value);
    }
  },
  apiKey: {
    get() {
      return this.$store.getters.apiKey;
    },
    set(value) {
      this.$store.dispatch('ApiKey', value);
    }
  }
},
methods: {
  
    togglePasswordField() {
     this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
   },
    removeItem(index) {
      this.searchqueries.splice(index, 1);
      this.searchqueries = [...this.searchqueries];
    },
    addItem() {
    if (this.searchqueries.length < 5) {
        this.searchqueries.push("");
        this.searchqueries = [...this.searchqueries];
        }
    },
    addItemAuto() {
      if (this.searchqueries.length < 5 && this.searchqueries[this.searchqueries.length - 1] !== "") {
          this.searchqueries.push("");
          this.searchqueries = [...this.searchqueries];
      }
    },
async search() {
  try {
    const filteredQueries = this.searchqueries.filter(query => query.trim() !== "");
    // Check if any of the search queries are empty
    if (filteredQueries.length === 0) {
      alert("Please enter at least one research topic before submitting.");
      return;
    }

    if (this.apiKey.trim() === "") {
      alert("Please fill in the API key field before submitting.");
      return;
    }
    // If all fields are filled in, proceed to the next page
    this.searchqueries = [...filteredQueries];
    this.buttonText = "Checking Key...";

    const response = await this.callApi();
    if (response['Key'] === 'Valid') {
      console.log(this.searchqueries)
      this.$router.push({ path: '/preference' });
    } else {
      this.buttonText = "Start";
      alert("Please enter a valid API key");
      return;
    }
  } catch (error) {
    console.error(error);
  }
},
async callApi() {
    // console.log(this.searchqueries)
    const trimmedApiKey = this.apiKey.trim();
    const url = "https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/testapi";  // replace with your API endpoint
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
        this.buttonText = "Search"
        console.error(error);
        alert(`There is an error when checking the api key. Please try again! `);// handle error here
    }
},
  }
};
</script>

  
<style scoped>
.form-control{
  font-style: italic;
}
@media (max-width: 768px) {
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
</style>