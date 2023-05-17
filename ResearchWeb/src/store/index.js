import { createStore } from 'vuex'

export default createStore({
  state: {
    searchQueries: [""],
    apiKey: "",
    width: 5,
    depth: 1,
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
    setWidth(state, width) {
      state.width = width;
    },
    setDepth(state, depth) {
      state.depth = depth;
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
    setWidth({ commit }, width) {
      commit('setWidth', width);
    },
    setDepth({ commit }, depth) {
      commit('setDepth', depth);
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
    width: state => state.width,
    depth: state => state.depth,
    domain: state => state.domain,
    jsonData: state => state.jsonData,
    taskId: state => state.taskId
  }
})
