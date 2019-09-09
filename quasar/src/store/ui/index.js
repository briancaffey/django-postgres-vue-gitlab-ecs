const state = {
  visible: false,
  darkMode: false,
  leftDrawerOpen: false,
  nextLink: null,
  authPanel: "login"
};

const getters = {
  leftDrawerOpen: s => s.leftDrawerOpen,
  authModalVisible: s => s.visible,
  getNextLink: s => s.nextLink,
  getAuthPanel: s => s.authPanel
};

const mutations = {
  setAuthPanel: (state, payload) => {
    console.log("change panel...");
    console.log(payload);
    state.authPanel = payload;
  },
  toggleLoginMenu: state => {
    console.log("firing toggleLoginMenu mutation");
    state.visible = !state.visible;
  },
  toggleLeftDrawer: (state, payload) => {
    if (payload) {
      console.log("toggling drawer");
      console.log(payload);
      state.leftDrawerOpen = payload.leftDrawerOpen;
      return;
    }
    console.log("toggling");
    state.leftDrawerOpen = !state.leftDrawerOpen;
  },
  setNextLink: (state, payload) => {
    state.nextLink = payload.nextLink;
  }
};

export default {
  state,
  getters,
  mutations
};
