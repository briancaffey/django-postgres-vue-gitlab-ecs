import gql from "graphql-tag";
import { Cookies } from "quasar";

const state = {
  token: Cookies.get("user-token-gql") || "",
};

const getters = {
  getToken: (s) => s.token,
  isAuthenticated: (s) => !!s.token,
};

const actions = {
  async authRequest({ commit }, { email, password, vm }) {
    const resp = await vm.$apollo.mutate({
      mutation: gql`
        mutation($email: String!, $password: String!) {
          tokenAuth(email: $email, password: $password) {
            token
          }
        }
      `,
      variables: {
        email,
        password,
      },
    });
    commit("authSuccess", resp.data);
  },
};

const mutations = {
  authSuccess: (state, payload) => {
    Cookies.set("user-token-gql", payload.tokenAuth.token);
    state.token = payload.tokenAuth.token;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
