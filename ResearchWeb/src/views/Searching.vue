<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['jsonData']),
  },
  created() {
    console.log("jsonData in component:", this.jsonData);
  },
  methods: {
    newSearch() {
      this.$router.push({ path: '/' });
    },
  },
};
</script>

<template>
  <div class="results-container">
    <p>Search Results:</p>
    <pre>{{ jsonData }}</pre>
    <div class="button-container">
      <button type="button" @click="newSearch" class="startover-button">New Search</button>
    </div>
  </div>
</template>

<style scoped>
.results-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.results-container p {
  font-family: Arial, sans-serif;
  font-size: 20px;
  margin-left: -100px;
  font-weight: bold;
  width: 800px;
  margin-bottom: 40px;
}

pre {
  width: 900px;
  font-family: Arial, sans-serif;
  font-size: 20px;
  margin-bottom: 20px;
  overflow: auto;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 120px;
  margin-top: 80px;
}

.startover-button {
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

.startover-button:hover {
  background-color: #0c952c;
  color: #ffffff;
}
</style>
