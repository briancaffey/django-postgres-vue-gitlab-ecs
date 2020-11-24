export const AUTH_REQUEST = "AUTH_REQUEST";
export const AUTH_SUCCESS = "AUTH_SUCCESS";
export const AUTH_ERROR = "AUTH_ERROR";
export const AUTH_LOGOUT = "AUTH_LOGOUT";
export const AUTH_REFRESH = "AUTH_REFRESH";

// import axios from "axios";
import Vue from "vue";
import { Cookies } from "quasar";
import { USER_REQUEST } from "../user";
import gqljwt from "./gqljwt";

const state = {
  token: localStorage.getItem("user-token") || "",
  status: "",
  hasLoadedOnce: false,
};

const getters = {
  getToken: (s) => s.token,
  isAuthenticated: (s) => !!s.token,
  authStatus: (s) => s.status,
};

const actions = {
  [AUTH_REQUEST]: ({ commit, dispatch }, user) =>
    new Promise((resolve, reject) => {
      commit(AUTH_REQUEST);
      Vue.prototype.$axios
        .post("/api/login/", user)
        .then((resp) => {
          localStorage.setItem("user-token", "success");
          commit(AUTH_SUCCESS, resp);
          dispatch(USER_REQUEST);
          resolve(resp);
        })
        .catch((err) => {
          commit(AUTH_ERROR, err);
          localStorage.removeItem("user-token");
          reject(err);
        });
    }),
  [AUTH_LOGOUT]: ({ commit, dispatch }) =>
    new Promise((resolve, reject) => {
      commit(AUTH_LOGOUT);
      localStorage.removeItem("user-token");
      resolve();
    }),
};

const mutations = {
  [AUTH_REQUEST]: (requestState) => {
    const s = requestState;
    s.status = "loading";
  },
  [AUTH_SUCCESS]: (s, resp) => {
    s.status = "success";
    s.token = "success";
    s.hasLoadedOnce = true;
  },
  [AUTH_ERROR]: (errorState) => {
    const s = errorState;
    s.status = "error";
    s.hasLoadedOnce = true;
  },
  [AUTH_LOGOUT]: (logoutState) => {
    const s = logoutState;
    s.token = "";
  },
};

const modules = {
  gqljwt,
};

export default {
  state,
  getters,
  actions,
  mutations,
  modules,
};
