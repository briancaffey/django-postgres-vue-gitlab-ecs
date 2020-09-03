import statements from "./statements";
import transactions from "./transactions";
import upload from "./upload";

export default {
  namespaced: true,
  modules: {
    statements,
    transactions,
    upload,
  },
};
