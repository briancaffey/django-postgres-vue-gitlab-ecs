import gql from "graphql-tag";

const state = {
  url: "",
  description: "",
  showUploadForm: false
};

const getters = {
  getUrl: s => s.url,
  getDescription: s => s.description,
  getShowUploadForm: s => s.showUploadForm
};

const actions = {
  async submitLink({ getters }, { vm }) {
    const resp = await vm.$apollo.mutate({
      mutation: gql`
        mutation($url: String!, $description: String!) {
          createLink(url: $url, description: $description) {
            id
            url
            description
            postedBy {
              email
              id
            }
          }
        }
      `,
      variables: {
        url: getters.getUrl,
        description: getters.getDescription
      }
    });
    console.log(resp);
    // commit("toggleUploadForm");
  }
};

const mutations = {
  setUrl: (state, payload) => {
    state.url = payload;
  },
  setDescription: (state, payload) => {
    state.description = payload;
  },
  toggleUploadForm: state => {
    state.showUploadForm = !state.showUploadForm;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
