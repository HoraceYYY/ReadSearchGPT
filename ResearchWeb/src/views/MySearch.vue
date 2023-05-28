<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      buttonText: "Find My Results"
    };
  },
  created() {
  this.taskId = '' //clear the input from previous input of the same session
},
  computed: {
    ...mapGetters(['jsonData']),
    taskId: {
      get() {
        return this.$store.state.taskId;
      },
      set(value) {
        this.$store.dispatch('setTaskId', value);
      }
    }
  },
  methods: {
    async findSearch() {
      const url = `https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/task/${this.taskId}/status`;  // replace with your API endpoint
      try {
        this.buttonText = "Retriveing...";
        const response = await fetch(url,{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const jsonData = await response.json();

        console.log(jsonData);
        this.$store.dispatch('setJsonData', jsonData);
        await this.$router.push({ path: '/results' });
      } catch (error) {
        this.buttonText = "Find My Search"
        console.error(error);
        alert(`There is an error during the search: ${error}`);
      }
    }
  }
};
</script>

<template>
  <div class="container">
    <form @submit.prevent="findSearch">
      <div class="form-group">
        <label for="task_id" class="form-label">Enter Task ID to Retrive Results:</label>
        <input type="text" id="task_id" v-model="taskId" class="form-control" placeholder="Enter Task ID ..." />
      </div>
      <div class="button-container">
        <button type="submit" class="btn search-button">{{ buttonText }}</button>
      </div>
    </form>
  </div>
</template>


<style scoped>
.form-group {
  max-width: 1000px;
  margin: auto;
}

.form-label {
  display: block;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: left;
  font-size: 20px;
}

.form-control {
  width: 100%;
  font-style: italic;
  padding: 10px;
  font-size: 18px;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 80px;
}

.search-button {
  border-color: #0c952c;
  color: #0c952c;
}

.search-button:hover {
  background-color: #0c952c;
  color: #fff;
}
</style>
