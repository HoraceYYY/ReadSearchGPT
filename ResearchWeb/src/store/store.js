import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    searchQueries: [],
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
