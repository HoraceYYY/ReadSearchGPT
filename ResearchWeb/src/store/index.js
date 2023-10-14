import { createStore } from 'vuex'

export default createStore({
  state: {
    queryIDs: [],
    searchQueries: [""], 
    apiKey: "",
    domain: "",
    jsonData: {},
    researchId: "",
    queries: {}, //a dictionary of queryID:query
    urlResults: {}, //a dict of queryID: [url, title, content]
    urlSummaries: {}, // a dict of queryID: summary
  },
  mutations: {
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
    setResearchId(state, researchId) {
      state.researchId = researchId;
    },
    setSearchQueries(state, searchQueries) {
      state.searchQueries = searchQueries;
    },
  },
  actions: {
    ApiKey({ commit }, apiKey) {
      commit('setApiKey', apiKey);
    },
    setDomain({ commit }, domain) {
      commit('setDomain', domain);
    },
    setJsonData({ commit }, jsonData) {
      commit('setJsonData', jsonData);
    },
    setResearchId({ commit }, researchId) {
      commit('setResearchId', researchId);
    },
    setSearchQueries({ commit }, searchQueries) {
      commit('setSearchQueries', searchQueries);
    },
  },
  getters: {
    apiKey: state => state.apiKey,
    domain: state => state.domain,
    jsonData: state => state.jsonData,
    researchId: state => state.researchId,
    searchQueries: state => state.searchQueries,
  }
})
