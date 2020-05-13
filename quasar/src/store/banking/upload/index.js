const state = {
  date: null,
  file: null,
};

const getters = {
  getDate: (s) => s.date,
  getFile: (s) => s.file,
};

const actions = {
  uploadFile: ({ getters }, payload) => {
    const formData = new FormData();
    formData.append("file", getters.getFile);
    formData.append("form", JSON.stringify({ month: getters.getDate }));
    payload.vm.$axios.post("/api/statements/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

const mutations = {
  setDate: (state, payload) => {
    state.date = payload;
  },
  setFile: (state, payload) => {
    state.file = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
