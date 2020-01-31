import Vue from "vue";

const state = {
  loading: true,
  files: [],
  count: 0,
  currentPage: 1,
  paginationLimit: 2,
  columns: [
    { align: "left", field: "id", label: "ID" },
    { align: "left", field: "month", label: "Month" },
    { align: "left", field: "statement_file", label: "File" }
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
  getFiles: s => s.files,
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
  getFiles: ({ commit, getters }) => {
    commit("setLoading", true);
    const params = getters.queryParams;
    Vue.prototype.$axios.get("/api/statements/", { params }).then(resp => {
      commit("getFiles", resp.data);
      commit("setLoading", false);
    });
  },
  setCurrentPage: ({ commit, dispatch }, payload) => {
    commit("setCurrentPage", payload);
    dispatch("getFiles");
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
  getFiles: (state, payload) => {
    state.files = payload.results;
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
