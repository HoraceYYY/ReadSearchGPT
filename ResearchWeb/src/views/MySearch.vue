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
  <div class="form-container">
    <form @submit.prevent="findSearch">
      <div class="input-group">
        <label for="task_id" class="input-label">Enter Task ID to Retrive Results:</label>
        <input type="text" id="task_id" v-model="taskId" class="text-input" placeholder="Enter Task ID ..." />
      </div>
      <div class="button-container">
        <button type="submit" class="search-button">{{ buttonText }}</button>
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
}

.form-container p {
  font-family: Arial, sans-serif;
  font-size: 20px;
  margin-left: -100px;
  font-weight: bold;
  width: 800px;
  margin-bottom: 40px;
}

.input-group {
  width: 900px;
  margin-bottom: 20px;
  font-family: Arial, sans-serif;
  font-size: 20px;
}
.input-label{
  font-weight: bold;
  margin-bottom: 10px;
}
.text-input {
  width: 96%;
  margin: 10px 0;
  font-style: italic;
  font-family: Arial, sans-serif;
  font-size: 18px;
  padding: 10px;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 120px;
  margin-top: 80px;
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

.search-button:hover {
  background-color: #0c952c;
  color: #ffffff;
}
</style>
