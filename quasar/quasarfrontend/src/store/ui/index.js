const state = { visible: false, darkMode: false, leftDrawerOpen: false };

const getters = {
  leftDrawerOpen: s => s.leftDrawerOpen,
  loginModalVisible: s => s.visible
};

const mutations = {
  toggleLoginMenu: state => {
    state.visible = !state.visible;
  },
  toggleLeftDrawer: state => {
    state.leftDrawerOpen = !state.leftDrawerOpen;
  }
};

export default {
  state,
  getters,
  mutations
};
