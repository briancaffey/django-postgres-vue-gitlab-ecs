import buildURL from "axios/lib/helpers/buildURL";

const state = {
  githubClientId: "d6639d522598d6bf20f4"
};

const getters = {
  githubOauth2Link: s => {
    return "test-link";
  }
};

export default {
  state,
  getters
};
