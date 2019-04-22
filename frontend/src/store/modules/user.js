/* eslint-disable no-unused-vars */

import Vue from 'vue';
import { AUTH_LOGOUT } from '../actions/auth';
import { USER_REQUEST, USER_ERROR, USER_SUCCESS } from '../actions/user';
import apiCall from '../../utils/api';
import store from '..';

const state = { status: '', profile: {} };

const getters = {
  getProfile: s => s.profile,
  isProfileLoaded: s => !!s.profile.name,
};

const actions = {
  [USER_REQUEST]: ({ commit, dispatch }) => {
    apiCall.get('/api/users/profile/')
      .then((resp) => {
        const profile = resp.data;
        commit(USER_SUCCESS, { email: profile.email });
      })
      .catch((resp) => {
        commit(USER_ERROR);
        dispatch(AUTH_LOGOUT);
      });
  },
};

const mutations = {
  [USER_REQUEST]: (requestState) => {
    const s = requestState;
    s.status = 'loading';
  },
  [USER_SUCCESS]: (successState, resp) => {
    const s = successState;
    s.status = 'success';
    Vue.set(state, 'profile', resp);
  },
  [USER_ERROR]: (errorState) => {
    const s = errorState;
    s.status = 'error';
  },
  [AUTH_LOGOUT]: (authState) => {
    const s = authState;
    s.profile = {};
    s.status = '';
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
