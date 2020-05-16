import VueApollo from "vue-apollo";

import { ApolloClient } from "apollo-client";
import { createHttpLink } from "apollo-link-http";
import { setContext } from "apollo-link-context";
import { InMemoryCache } from "apollo-cache-inmemory";

// HTTP connection to the API
const httpLink = createHttpLink({
  uri: `/graphql/`,
});

// Cache implementation
const cache = new InMemoryCache();

export default ({ app, Vue, store }) => {
  const authLink = setContext((_, { headers }) => {
    let authorization = "";
    if (store.getters.isAuthenticated) {
      authorization = `JWT ${store.getters["gqljwt/getToken"]}`;
    }
    return {
      headers: {
        ...headers,
        authorization,
      },
    };
  });

  const apolloClient = new ApolloClient({
    link: authLink.concat(httpLink),
    cache,
  });

  const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
  });

  Vue.use(VueApollo);
  app.apolloProvider = apolloProvider;
};
