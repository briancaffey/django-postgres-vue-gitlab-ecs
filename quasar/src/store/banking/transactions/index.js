import Vue from "vue";

const state = {
  loading: true,
  transactions: [],
  count: 0,
  currentPage: 1,
  paginationLimit: 5,
  columns: [
    { align: "left", field: "id", label: "ID" },
    { align: "left", field: "date", label: "Date" },
    { align: "left", field: "description", label: "Description" },
    { align: "left", field: "amount", label: "Amount" },
    { align: "left", field: "location", label: "Location" },
    { align: "left", field: "source_file", label: "File" }
  ]
};

const getters = {
  getLoading: s => s.loading,
  getPagination: s => {
    return {
      pagination: {
        rowsPerPage: s.paginationLimit,
        pagesNumber: s.count
      }
    };
  },
  getPaginationLimit: s => s.paginationLimit,
  getTransactions: s => s.transactions,
  getCount: s => s.count,
  getTableColumns: s => s.columns,
  getCurrentPage: s => s.currentPage,
  queryParams: s => {
    return {
      offset: (s.currentPage - 1) * s.paginationLimit,
      limit: s.paginationLimit
    };
  }
};

const actions = {
  getTransactions: ({ commit, getters }) => {
    commit("setLoading", true);
    const params = getters.queryParams;
    Vue.prototype.$axios.get("/api/transactions/", { params }).then(resp => {
      commit("getTransactions", resp.data);
      commit("setLoading", false);
    });
  },
  setCurrentPage: ({ commit, dispatch }, payload) => {
    commit("setCurrentPage", payload);
    dispatch("getTransactions");
  }
};

const mutations = {
  setLoading: (state, payload) => {
    if (payload) {
      state.loading = payload;
    } else {
      state.loading = !state.loading;
    }
  },
  getTransactions: (state, payload) => {
    state.transactions = payload.results;
    state.count = payload.count;
  },
  setCurrentPage: (state, payload) => {
    state.currentPage = payload;
  },
  setPagination: (state, payload) => {
    // console.log(state);
    console.log("payload for pagination....");
    console.log(payload);
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
