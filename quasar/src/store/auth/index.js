/* eslint-disable no-unused-vars */

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
  token: Cookies.get("user-token") || "",
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
        .post("/api/auth/obtain_token/", user)
        .then((resp) => {
          Cookies.set("refresh-token", resp.data.refresh);
          Cookies.set("user-token", resp.data.access);
          commit(AUTH_SUCCESS, resp);
          dispatch(USER_REQUEST);
          resolve(resp);
        })
        .catch((err) => {
          commit(AUTH_ERROR, err);
          Cookies.remove("user-token");
          Cookies.remove("refresh-token");
          reject(err);
        });
    }),
  [AUTH_LOGOUT]: ({ commit, dispatch }) =>
    new Promise((resolve, reject) => {
      commit(AUTH_LOGOUT);
      Cookies.remove("user-token");
      Cookies.remove("refresh-token");
      resolve();
    }),
  [AUTH_REFRESH]: ({ commit, dispatch }) =>
    new Promise((resolve, reject) => {
      Vue.prototype.$axios
        .post("/api/auth/refresh_token/", {
          refresh: Cookies.get("refresh-token"),
        })
        .then((resp) => {
          Cookies.set("user-token", resp.data.access);
          commit(AUTH_SUCCESS, resp);
        });
    }),
};

const mutations = {
  [AUTH_REQUEST]: (requestState) => {
    const s = requestState;
    s.status = "loading";
  },
  [AUTH_SUCCESS]: (s, resp) => {
    s.status = "success";
    s.token = resp.data.access;
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
