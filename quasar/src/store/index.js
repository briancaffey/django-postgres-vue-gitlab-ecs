import Vue from "vue";
import Vuex from "vuex";
import ui from "./ui";
import auth from "./auth";
import user from "./user";
import social from "./social";
import banking from "./banking";

// import example from './module-example'

Vue.use(Vuex);

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */
export default function(/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      ui,
      auth,
      user,
      social,
      banking
    },

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEV
  });
  return Store;
}
