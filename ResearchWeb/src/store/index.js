import { createStore } from 'vuex'

export default createStore({
  state: {
    searchQueries: [""],
    apiKey: ""
  },
  mutations: {
    setSearchQueries(state, searchQueries) {
      state.searchQueries = searchQueries;
    },
    setApiKey(state, apiKey) {
      state.apiKey = apiKey;
    }
  },
  actions: {
    SearchQueries({ commit }, searchQueries) {
      commit('setSearchQueries', searchQueries);
    },
    ApiKey({ commit }, apiKey) {
      commit('setApiKey', apiKey);
    }
  },
  getters: {
    searchQueries: state => state.searchQueries,
    apiKey: state => state.apiKey
  }
})
