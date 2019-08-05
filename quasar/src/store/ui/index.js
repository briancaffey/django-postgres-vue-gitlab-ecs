const state = {
  visible: false,
  darkMode: false,
  leftDrawerOpen: false,
  nextLink: null
};

const getters = {
  leftDrawerOpen: s => s.leftDrawerOpen,
  authModalVisible: s => s.visible,
  getNextLink: s => s.nextLink
};

const mutations = {
  toggleLoginMenu: state => {
    state.visible = !state.visible;
  },
  toggleLeftDrawer: (state, payload) => {
    if (payload) {
      state.leftDrawerOpen = payload.leftDrawerOpen;
      return;
    }
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
