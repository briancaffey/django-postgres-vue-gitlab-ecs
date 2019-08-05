import oauth from "../utils/oauth";

const state = {
  oauth
};

const getters = {
  oauthUrl: () => {
    return provider => state.oauth[provider].sender;
  },
  getProfile: s => s.status,
  getUrl: s => s.status
};

const actions = {};

const mutations = {};

export default {
  state,
  getters,
  actions,
  mutations
};
