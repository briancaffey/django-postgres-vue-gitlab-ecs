import Vue from "vue";
import Vuex from "vuex";
import user from "./modules/user";
import auth from "./modules/auth";
import chat from "./modules/chat";
import socialAuth from "./modules/socialAuth";

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== "production";

export default new Vuex.Store({
  modules: {
    user,
    auth,
    chat,
    socialAuth
  },
  strict: debug
});
