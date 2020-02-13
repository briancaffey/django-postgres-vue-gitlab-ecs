import gql from "graphql-tag";

const state = {
  links: null
};

const getters = {
  getLinks: s => s.links
};

const actions = {
  async getLinks({ commit }, { vm }) {
    const resp = await vm.$apollo.query({
      query: gql`
        query {
          links {
            url
            id
            votes {
              id
              user {
                email
              }
            }
          }
        }
      `
    });

    const links = resp.data.links;
    commit("setLinks", { links });
  }
};

const mutations = {
  setLinks: (state, { links }) => {
    state.links = links;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
