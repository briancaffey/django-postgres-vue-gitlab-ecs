import axios from "axios";

export default async ({ Vue, store, router }) => {
  const apiCall = axios.create({
    baseURL: process.env.API_URL
  });

  apiCall.interceptors.request.use(
    config => {
      const c = config;
      if (store.getters.isAuthenticated) {
        c.headers.Authorization = `Bearer ${store.getters.getToken}`;
      }
      return c;
    },
    error => {
      Promise.reject(error);
    }
  );

  function handleSuccess(response) {
    return { data: response.data };
  }

  function handleError(error) {
    console.log(error);
    switch (error.response.status) {
      case 400:
        break;
      case 401:
        // Log out user, remove token, clear state and redirect to login
        store.dispatch("AUTH_LOGOUT").then(router.push("/"));
        break;
      case 404:
        // Show 404 page
        break;
      case 500:
        // Serveur Error redirect to 500
        break;
      default:
        // Unknow Error
        break;
    }
    return Promise.reject(error);
  }

  apiCall.interceptors.response.use(handleSuccess, handleError);

  Vue.prototype.$axios = apiCall;
};
