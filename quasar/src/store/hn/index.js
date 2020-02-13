import gql from "graphql-tag";
import upload from "./upload";

const state = {
  links: null,
  searchTerm: ""
};

const getters = {
  getLinks: s => s.links,
  getSearchTerm: s => s.searchTerm
};

const actions = {
  async getLinks({ commit, getters }, { vm }) {
    const resp = await vm.$apollo.query({
      query: gql`
        query GetLinks($search: String!) {
          links(search: $search) {
            url
            id
            description
            postedBy {
              email
              id
            }
            votes {
              id
              user {
                email
              }
            }
          }
        }
      `,
      variables: {
        search: getters.getSearchTerm
      }
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

const modules = {
  upload
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
  modules
};
