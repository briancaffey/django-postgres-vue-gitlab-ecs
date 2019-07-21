import Vue from "vue";
import Vuex from "vuex";
import ui from "./ui";
import auth from "./auth.js";
import user from "./user.js";

// import example from './module-example'

Vue.use(Vuex);

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

export default new Vuex.Store({
  modules: {
    ui,
    auth,
    user
  },

  // enable strict mode (adds overhead!)
  // for dev mode only
  strict: process.env.DEV
});
