import buildURL from "axios/lib/helpers/buildURL";
import oauth from "../utils/oauth";

const state = {
  oauth
};

const getters = {
  oauthUrl: () => {
    return provider => {
      const url = state.oauth[provider].url;
      const params = state.oauth[provider].params;

      return buildURL(url, params);
    };
  }
};

const actions = {};

const mutations = {};

export default {
  state,
  getters,
  actions,
  mutations
};
