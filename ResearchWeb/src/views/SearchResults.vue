<template>
    <div class="container-fluid px-4">
        <div class="row d-flex">
            <div class="col-12 col-md-7 pr-md-2">
                <h2 class="card-header text-start">Research Summary</h2>
                <div class="card">
                    <div class="card-content">
                        <div class="overlay-wrapper">
                            <div class="mb-4 text-start text-black">
                                <h3 class="font-weight-bold query-title fst-italic">{{ queries[queryIDs[currentQueryId]] }}</h3>
                                <p v-html="urlSummaries[queryIDs[currentQueryId]]"></p>
                            </div>
                            <div class="overlay" v-show="searchState[queryIDs[currentQueryId]] === 'searching'">
                                <p class="loading-text">The additional search will take about 1-2 minutes.</p>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer">
                        <button @click="previousQuery" :class="{'invisible-button': currentQueryId === 0, 'btn-success': true}" >Previous</button>
                        <button @click="handleSearchClick" :class="{'btn-success': true}" :disabled="isButtonDisabled">{{ buttonText }}</button>
                        <button @click="nextQuery" :class="{'invisible-button': currentQueryId === maxQueryId - 1, 'btn-success': true}" >Next</button>
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
export default {
    data() {
      return {
        currentQueryId: 0,
        researchId: "",
        apiKey: "",
        queryIDs: [],
        queries: {},
        urlResults: {},
        urlSummaries: {},
        searchState: {},
        userDomain: "",
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
                return "Broader Search";
            case "broad":
                return "Deeper Search";
            case "searching":
                return "Searching...";
            default:
                return "Search is Done";
        }
    },
    isButtonDisabled() {
        const currentSearchState = this.searchState[this.queryIDs[this.currentQueryId]];
        return currentSearchState === "done" || currentSearchState === "searching";
    }
    },
    created() {
    this.parsedata();
    for (const queryId of this.queryIDs) {
        this.searchState[queryId] = "initial";
    }
},

methods: {
    parsedata(){
        if (this.jsonData){
            const data = this.jsonData;
            this.researchId = data[0];
            const queryData = data[1];
            this.apiKey = data[2];
            this.userDomain = data[3];
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
                const url1 = "http://localhost:8000/secondsearch";  // replace with your API endpoint
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
                const url2 = "http://localhost:8000/firstdeepsearch";  // replace with your API endpoint
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
        const url = `http://localhost:8000/task/${this.researchId}/webdownload`;  // Replace with your API endpoint URL
        try {
            const response = await fetch(url, { method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
            });
            if (!response.ok) {
                throw new Error("HTTP error " + response.status);
            }
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = downloadUrl;
            a.download = `${this.researchId}.docx`; // or any name you want to give to your file
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
  }
    }
}   
</script>

<style scoped>
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
.query-title {
  text-transform: capitalize;
}

</style>