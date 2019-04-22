/* eslint-disable promise/param-names, no-unused-vars */
import { AUTH_REQUEST, AUTH_ERROR, AUTH_SUCCESS, AUTH_LOGOUT, AUTH_REFRESH } from '../actions/auth';
import { USER_REQUEST } from '../actions/user';
import apiCall from '../../utils/api';

const state = { token: localStorage.getItem('user-token') || '', status: '', hasLoadedOnce: false };

const getters = {
  getToken: s => s.token,
  isAuthenticated: s => !!s.token,
  authStatus: s => s.status,
};

const actions = {
  [AUTH_REQUEST]: ({ commit, dispatch }, user) => new Promise((resolve, reject) => {
    commit(AUTH_REQUEST);
    apiCall.post(
      '/api/auth/obtain_token/',
      user,
    )
      .then((resp) => {
        localStorage.setItem('user-token', resp.data.access);
        localStorage.setItem('refresh-token', resp.data.refresh);
        commit(AUTH_SUCCESS, resp);
        dispatch(USER_REQUEST);
        resolve(resp);
      })
      .catch((err) => {
        commit(AUTH_ERROR, err);
        localStorage.removeItem('user-token');
        reject(err);
      });
  }),
  [AUTH_LOGOUT]: ({ commit, dispatch }) => new Promise((resolve, reject) => {
    commit(AUTH_LOGOUT);
    localStorage.removeItem('user-token');
    resolve();
  }),
  [AUTH_REFRESH]: ({ commit, dispatch }) => new Promise((resolve, reject) => {
    apiCall.post(
      '/api/auth/refresh_token/',
      { refresh: localStorage.getItem('refresh-token') },
    ).then((resp) => {
      localStorage.setItem('user-token', resp.data.access);
      commit(AUTH_SUCCESS, resp);
    });
  }),
};

const mutations = {
  [AUTH_REQUEST]: (requestState) => {
    const s = requestState;
    s.status = 'loading';
  },
  [AUTH_SUCCESS]: (successState, resp) => {
    const s = successState;
    s.status = 'success';
    s.token = resp.data.access;
    s.hasLoadedOnce = true;
  },
  [AUTH_ERROR]: (errorState) => {
    const s = errorState;
    s.status = 'error';
    s.hasLoadedOnce = true;
  },
  [AUTH_LOGOUT]: (logoutState) => {
    const s = logoutState;
    s.token = '';
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
