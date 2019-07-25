import axios from "axios";
import store from "../store";
import router from "../router";

/* eslint no-unused-vars: ["error", { "args": "none" }] */

// TODO: Change API_URL to BASE_URL and prepare for production env
const apiCall = axios.create({
  baseURL: process.env.API_URL || "http://localhost"
});

apiCall.interceptors.request.use(
  config => {
    const c = config;
    // Do something before each request is sent
    if (store.getters.isAuthenticated) {
      // Take the token from the state and attach it to the request's headers
      c.headers.Authorization = `Bearer ${store.getters.getToken}`;
    }
    return c;
  },
  error => {
    // Do something with the request error
    Promise.reject(error);
  }
);

function handleSuccess(response) {
  return { data: response.data };
}

function handleError(error) {
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

export default apiCall;
