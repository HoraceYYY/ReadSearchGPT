import { createStore } from 'vuex'

export default createStore({
  state: {
    searchQueries: [""],
    apiKey: "",
    domain: "",
    jsonData: {},
    taskId: ""
  },
  mutations: {
    setSearchQueries(state, searchQueries) {
      state.searchQueries = searchQueries;
    },
    setApiKey(state, apiKey) {
      state.apiKey = apiKey;
    },
    setDomain(state, domain) {
      state.domain = domain;
    },
    setJsonData(state, jsonData) {
      //state.jsonData = { ...jsonData };
      state.jsonData = jsonData;
    },
    setTaskId(state, taskId) {
      state.taskId = taskId;
    },
  },
  actions: {
    SearchQueries({ commit }, searchQueries) {
      commit('setSearchQueries', searchQueries);
    },
    ApiKey({ commit }, apiKey) {
      commit('setApiKey', apiKey);
    },
    setDomain({ commit }, domain) {
      commit('setDomain', domain);
    },
    setJsonData({ commit }, jsonData) {
      commit('setJsonData', jsonData);
    },
    setTaskId({ commit }, taskId) {
      commit('setTaskId', taskId);
    }
  },
  getters: {
    searchQueries: state => state.searchQueries,
    apiKey: state => state.apiKey,
    domain: state => state.domain,
    jsonData: state => state.jsonData,
    taskId: state => state.taskId
  }
})
