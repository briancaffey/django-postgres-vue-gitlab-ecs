const state = { visible: false };

const getters = {
  loginModalVisible: s => s.visible
};

const mutations = {
  toggleLoginMenu: state => {
    state.visible = !state.visible;
  }
};

export default {
  state,
  getters,
  mutations
};
