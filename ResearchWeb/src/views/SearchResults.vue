<template>
    <div v-if="showApiKeyModal" class="modal d-block">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title text-black">Enter API Key</h5>
          <button type="button" class="btn-close" aria-label="Close" @click="closeApiKeyModal"></button>
        </div>
        <div class="modal-body">
          <input type="text" v-model="apiKeyInput" class="form-control" placeholder="API Key">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeApiKeyModal">Cancel</button>
          <button type="button" class="btn btn-primary" @click="submitApiKey">{{ apibuttonText }}</button>
        </div>
      </div>
    </div>
  </div>
    <div class="container-fluid px-4">
        <div class="d-flex flex-column flex-md-row align-items-center justify-content-center mb-2 mt-0 gap-2">
            <div class="text-center text-md-start mt-3 mt-md-0">
                <h1 class="display-12 mb-1 fw-bold">ReadSearch</h1>
            </div>
            <div class="col-12 col-md-6">
                <div class="input-group">
                    <input type="text" v-model="inputValue" class="form-control" placeholder="Enter new search topic...">
                    <div clas5s="input-group-append">
                        <button @click="newSearch" class="btn-success btn-outline-primary">New Search</button>
                    </div>
                </div>
                <search-status-notification
                    :visible="searchStatusVisible"
                    :message="searchStatusMessage"
                    :completed="searchStatusCompleted"
                ></search-status-notification>
            </div>
        </div>
        <div class="row d-flex mt-3">
            <div class="col-12 col-md-7 pr-md-2">
                <h2 class="card-header text-start">Research Summary</h2>
                <div class="card mb-2">
                    <div class="card-content">
                        <div class="overlay-wrapper">
                            <div class="mb-4 text-start text-black">
                                <h3 class="font-weight-bold query-title fst-italic">{{ queries[queryIDs[currentQueryId]] }}</h3>
                                <p v-html="urlSummaries[queryIDs[currentQueryId]]"></p>
                            </div>
                            <div class="overlay" v-show="searchState[queryIDs[currentQueryId]] === 'searching'"></div>
                        </div>
                        
                        <p class="loading-text text-center" v-show="searchState[queryIDs[currentQueryId]] === 'searching'">The additional search will take about 1-2 minutes.</p>
                    </div>
                    <div class="card-footer">
                        <button @click="previousQuery" :class="{'invisible-button': currentQueryId === 0, 'btn-success': true}" >&#10550</button>
                        <button @click="handleSearchClick" :class="buttonClass" :disabled="isButtonDisabled">{{ buttonText }}</button>
                        <button @click="nextQuery" :class="{'invisible-button': currentQueryId === maxQueryId - 1, 'btn-success': true}" >&#10551</button>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-5 pl-md-2">
                <h2 class="card-header">Individual Web Results</h2>
                <div class="card">
                    <div class="card-content">
                        <div>
                            <div v-for="result in urlResults[queryIDs[currentQueryId]]" :key="result.url" class="mb-0 text-start">
                                <a :href="result.url" target="_blank" class="fs-5 font-weight-bold fst-italic">{{ result.title }}</a>
                                <p class="text-black" v-html="result.content"></p>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer">
                        <button class="btn-success" @click="handleDownloadReport">Download Report</button>
                        <a href="https://www.buymeacoffee.com/readsearch" target="_blank">
                            <button class="coffee-button">Buy Me A Coffee</button>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import SearchStatusNotification from './SearchStatusNotification.vue';

export default {
    components: {
        SearchStatusNotification,
    },
    data() {
      return {
        currentQueryId: 0, // index used for [queryid]
        apiKey: "", // api key from the query page
        apiKeyInput:"", // api key from the current page user input
        queryIDs: [], // a list of query ids [queryid]
        queries: {}, // {queryid : query}
        urlResults: {}, // {queryid : [title, url, content]}
        urlSummaries: {}, // {queryid: summary}
        searchState: {}, // {queryid: "state"}
        userDomain: "",
        inputValue: [], //[query]
        showApiKeyModal: false,
        apibuttonText: "Submit",
        searchStatusVisible: false, // Whether the search status notification is visible
        searchStatusMessage: '', // Message to display in the search status notification
        searchStatusCompleted: false, // Whether the search is completed
        searchCount: 0,
        completedCount: 0,
        };
    },
    computed: {
    maxQueryId() {
      return this.queryIDs.length;
    },
    jsonData: {
        get() {
            return this.$store.state.jsonData;
        },
        set(value) {
            this.$store.dispatch('setJsonData', value);
        }
    },
    buttonText() {
        // Check the searchState for the current queryId
        switch (this.searchState[this.queryIDs[this.currentQueryId]]) {
            case "initial":
                return "Explore More";
            case "broad":
                return "Dive Deeper";
            case "searching":
                return "Searching...";
            default:
                return "Search is Done";
        }
    },
    isButtonDisabled() {
        const currentSearchState = this.searchState[this.queryIDs[this.currentQueryId]];
        return currentSearchState === "done" || currentSearchState === "searching";
    },
    buttonClass() {
    const currentSearchState = this.searchState[this.queryIDs[this.currentQueryId]];
    if (currentSearchState === "done" || currentSearchState === "searching") {
        return 'btn-disabled';
    } else {
        return 'btn-success' ;
    }
}
    },
    created() {
    this.parsedata();
    if (this.apiKey === ""){ // if there is no api, it means user comes from the the history page, so all the search should be final
        for (const queryId of this.queryIDs) {
        this.searchState[queryId] = "done";
    }
    }else{ // if there is api, it means user comes from the the history page, so all the search should be final
        for (const queryId of this.queryIDs) {
        this.searchState[queryId] = "initial";
    }
    }
    
},

methods: {
    parsedata(){
        if (this.jsonData){
            const data = this.jsonData;
            const queryData = data[0];
            this.apiKey = data[1];
            if (queryData) {
                for (const [queryId, value] of Object.entries(queryData)) {
                    const query = value[0];
                    const results = value[1];
            
                        // Check if the queryId already exists in the list of queryIds
                    if (!this.queryIDs.includes(queryId)) {
                        // Add the queryId to the list of queryIds
                        this.queryIDs.push(queryId);
                    }
                    // Add the query to the queries dictionary
                    this.queries[queryId] = query;
                    this.urlResults[queryId] = []; // Initialize an empty list for the results of this queryId
                    
                    for (const result of results) { // Go through the results
                        if ('Summary' in result) {
                            // If the result is a summary, add it to the summaries dictionary
                            this.urlSummaries[queryId] = result.Summary;
                        } else {
                            // Otherwise, add it to the list of results for this queryId
                            this.urlResults[queryId].push(result);
                        }
                    }
                }
            }else{
                this.$router.push({ path: '/newsearch' });
            }
        }else{
        this.$router.push({ path: '/newsearch' });
    }   
    },
    async handleSearchClick() {
        const queryId = this.queryIDs[this.currentQueryId];
        switch (this.searchState[queryId]) {
            case "initial":
                const url1 = "https://api.readsearchgpt.com/secondsearch";  // replace with your API endpoint
                const data1 = {
                    queryID: queryId,
                    apiKey: this.apiKey,
                    };
                this.searchState[queryId] = "searching";
                //console.log(data); 
                try {
                    const response = await fetch(url1, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data1),
                    });
                    const searchResult1 = await response.json();
                    this.updateJsonData(searchResult1,this.jsonData)
                    this.parsedata()
                    this.searchState[queryId] = "broad";
                } catch (error) {
                    console.error(error);
                    alert(`There is an error duing the search: ${error}`);// handle error here
                    this.searchState[queryId] = "initial"
                }
                break;
            case "broad":
                const url2 = "https://api.readsearchgpt.com/firstdeepsearch";  // replace with your API endpoint
                const data2 = {
                    queryID: queryId,
                    searchDomain: this.userDomain,
                    apiKey: this.apiKey,
                    };
                this.searchState[queryId] = "searching";
                try {
                    const response = await fetch(url2, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data2),
                    });
                    const searchResult2 = await response.json();
                    this.updateJsonData(searchResult2,this.jsonData)
                    this.parsedata()
                    this.searchState[queryId] = "done";
                } catch (error) {
                    console.error(error);
                    alert(`There is an error duing the search: ${error}`);// handle error here
                    this.searchState[queryId] = "broad"
                }
                break;
            default:
                // The search is already done, do nothing
                break;
        }
    },
    updateJsonData(searchResult, jsondata) {
        // Get the new data from the searchResult
        const newQueryData = searchResult[0]; // As per your data structure

        // Iterate over the keys in newQueryData (i.e., the query ids)
        for (let queryId in newQueryData) {
            // Find the corresponding query id in jsondata
            const jsonDataIndex = jsondata.findIndex((element, index) => {
                // Check if element is an object (to avoid error with string elements)
                if (typeof element === 'object' && element !== null) {
                    // Return true (i.e., we've found our index) if the query id exists in the object
                    return element.hasOwnProperty(queryId);
                }
            });

            // If we found a matching query id in jsondata
            if (jsonDataIndex !== -1) {
                // Replace the value for that query id in jsondata with the new data from searchResult
                jsondata[jsonDataIndex][queryId] = newQueryData[queryId];
            }else {
                jsondata[0][queryId] = newQueryData[queryId];
            }
        }

        return jsondata;
    },
    nextQuery() {
            if (this.currentQueryId < this.maxQueryId - 1) {
                this.currentQueryId += 1;
            }
        },
    previousQuery() {
        if (this.currentQueryId > 0) {
            this.currentQueryId -= 1;
        }
    },
    async handleDownloadReport() {
        const url = `https://api.readsearchgpt.com/webdownload`;  // Replace with your API endpoint URL
        const  downloadQuerise= {
            queryIDs: this.queryIDs
        }
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(downloadQuerise),
                });
            if (!response.ok) {
                throw new Error("HTTP error " + response.status);
            }
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = downloadUrl;
            a.download = `Readsearch_Report.docx`; // or any name you want to give to your file
            document.body.appendChild(a);
            a.click();
            // After a timeout, remove the element and revoke the object URL
            setTimeout(() => {
                a.remove();
                window.URL.revokeObjectURL(downloadUrl);
            }, 0);
            } 
        catch (error) {
            console.error(error);
            }
  },
  showSearchStatusNotification(message, completed) {
      // Show the search status notification with the provided message and completion status
      this.searchStatusMessage = message;
      this.searchStatusCompleted = completed;
      this.searchStatusVisible = true;
    },
    completeSearch() {
      // Increase the completed count
      this.completedCount++;

      // If all searches are completed
      if (this.completedCount === this.searchCount) {
        // Update the completion status of the search notification
        this.showSearchStatusNotification('ReadSearch Completed', true);

        // Hide the notification after 2 seconds
        setTimeout(() => {
            this.searchStatusVisible = false;;
        }, 2000);
      } else {
        // Update the search status message
        this.showSearchStatusNotification(`ReadSearching ${this.searchCount - this.completedCount} New Topics...`, false);
      }
    },
  async newSearch() {
    if (this.inputValue.trim() !== ""){
        if (this.apiKey === ""){
            //show a pop up window for user to enter the api - use can choose to close this window
            this.showApiKeyModal = true;
            return            
            //call testapi endpoint to check if api is valid
        }
        const url = "https://api.readsearchgpt.com/firstsearch";  // replace with your API endpoint000
        const data = {
            searchqueries: [this.inputValue],
            apiKey: this.apiKey,
        };
        //console.log(data)
        try {
            await this.checkCookie();
            this.searchCount++;
            this.showSearchStatusNotification(`ReadSearching ${this.searchCount - this.completedCount}  New Topics...`, false);
            const response = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            });
            const searchResult = await response.json();
            let queryids = Object.keys(searchResult[0]);
            for (let queryid of queryids) {
                this.searchState[queryid] = 'initial'; // add the queryid to the status dictionary and Set its value to 'initial'
            }
            this.updateJsonData(searchResult, this.jsonData)// add this new jsondata to the exising jsondata 
            this.parsedata() // this will add the queryid in to the existing 
            this.completeSearch()
        } catch (error) {
            this.searchCount--;
            console.error(error);
            alert(`There is an error duing the search: ${error}`);// handle error here
        }
    }
    },
    async submitApiKey() {
    if (this.apiKeyInput.trim() !== "") {
      // Perform API key validation (e.g., by calling the testapi endpoint)
      this.apibuttonText = "Checking..."
      try{
        const response = await this.testApi();
        if (response['Key'] === 'Valid') {
            this.apiKey = this.apiKeyInput; // If the API key is valid, assign it to the `apiKey` data property
            this.showApiKeyModal = false; // Hide the API key modal
        }else{
            alert("Please enter a valid API key");
            return;
        }
      }catch (error) {
        console.error(error);
        alert("There was an error validating the API key.");
        return;
      } finally {
      this.apibuttonText = "Submit"; // Change the button text back to "Submit"
      }
      this.newSearch(); // Call the newSearch method to proceed with the search
    } else {
      alert("Please enter a valid API key."); // Show an error message if the API key is empty
    }
  },
  closeApiKeyModal() {
    this.showApiKeyModal = false; // Hide the API key modal without submitting the key
  },
  async testApi() {
    // console.log(this.searchQueries)
    const trimmedApiKey = this.apiKeyInput.trim();
    const url = "https://api.readsearchgpt.com/testapi";  // replace with your API endpoint
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
async checkCookie() {
      const url = "https://api.readsearchgpt.com/read-cookie"; // replace with your API endpoint
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
      const url = "https://api.readsearchgpt.com/create-cookie"; // replace with your API endpoint
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
@media (max-width: 576px) {
    .modal-dialog {
    max-width: 80%;
    margin: 0 auto
  }
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}
.coffee-button {
background-color: #FFDD00; /* Yellow background */
color: black; /* Black text */
border-radius: 5px; /* Add rounded corners */
padding: 5px 10px;
text-align: center; /* Centered text */
text-decoration: none; /* No underline */
display: inline-block;
font-size: 16px;
transition-duration: 0.4s; /* Transition effect */
cursor: pointer; /* Add a mouse pointer on hover */
}

.coffee-button:hover {
background-color: black; /* Black background */
color: white; /* White text */
}
@keyframes fade {
  0% {opacity: 1;}
  50% {opacity: 0.2;}
  100% {opacity: 1;}
}

.overlay-wrapper {
  position: relative;
  flex-grow: 1;
  overflow-y: auto;
  padding: 12px;
}

.loading-text {
  position: absolute;  /* Update from absolute to fixed */
  top: 50%;        /* New addition - Centering on viewport */
  left: 50%;       /* New addition - Centering on viewport */
  transform: translate(-50%, -50%); /* New addition - Centering on viewport */
  margin-bottom: 40px;
  color: #032152;
  font-size: 2em;
  animation: fade 3s linear infinite; 
  z-index: 1001;
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
a {
  color: #007bff;
  text-decoration: none;
}
a:hover {
  color: #0056b3;
}
.text-black {
  color: #000000;
}
h3, p {
  word-wrap: break-word;
}
.card {
    height: calc(100vh - 16rem); /* Adjust as needed */
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
}
.card-content {
 position: relative;
 overflow-y: auto;
 padding: 12px;
 flex-grow: 1;
}
.card-footer {
    display: flex;
  justify-content: space-between;
  background-color: transparent;
}
.invisible-button {
  opacity: 0;
  pointer-events: none;
}
.btn-success {
  background-color: #0c952c;
  border-color: #0c952c;
  color: #ffffff;
  border-radius: 5px; /* Add rounded corners */
  padding: 5px 10px; /* Add some padding */
}
.btn-success:hover {
  background-color: #006c22;
  border-color: #006c22;
}
.btn-disabled {
    color: #5f5f5f;
    background-color: #ccc;
    border-color: #ccc;
    border-radius: 5px; /* Add rounded corners */
    padding: 5px 10px; /* Add some padding */
}
.query-title {
  text-transform: capitalize;
}
h1 {
    color: #5781c0; /* Using the primary color for headings */
  }
</style>