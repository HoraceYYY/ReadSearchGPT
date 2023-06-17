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
    setQueryID(state, queryIDs) {
      state.queryIDs = queryIDs;
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
    setResearchId(state, researchId) {
      state.researchId = researchId;
    },
    setQueries(state, queries) {
      state.queries = queries;
    },
    setUrlResults(state, urlResults) {
      state.urlResults = urlResults;
    },
    setUrlSummaries(state, urlSummaries) {
      state.urlSummaries = urlSummaries;
    },
    setSearchQueries(state, searchQueries) {
      state.searchQueries = searchQueries;
    },
  },
  actions: {
    setQueryID({ commit }, queryIDs) {
      commit('setQueryID', queryIDs);
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
    setResearchId({ commit }, researchId) {
      commit('setResearchId', researchId);
    },
    setQueries({ commit }, queries) {
      commit('setQueries', queries);
    },
    setUrlResults({ commit }, urlResults) {
      commit('setUrlResults', urlResults);
    },
    setUrlSummaries({ commit }, urlSummaries) {
      commit('setUrlSummaries', urlSummaries);
    },
    setSearchQueries({ commit }, searchQueries) {
      commit('setSearchQueries', searchQueries);
    },
  },
  getters: {
    searchQueries: state => state.queryIDs,
    apiKey: state => state.apiKey,
    domain: state => state.domain,
    jsonData: state => state.jsonData,
    researchId: state => state.researchId,
    queries: state => state.queries,
    urlResults: state => state.urlResults,
    urlSummaries: state => state.urlSummaries,
    searchQueries: state => state.searchQueries,
  }
})
