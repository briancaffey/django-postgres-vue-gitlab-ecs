import VueNativeSock from "vue-native-websocket";

export default ({ store, Vue }) => {
  // something to do
  Vue.use(VueNativeSock, "ws://localhost:9000", {
    store,
    format: "json",
    connectManually: true,
    reconnection: true, // (Boolean) whether to reconnect automatically (false)
    reconnectionAttempts: 5, // (Number) number of reconnection attempts before giving up (Infinity),
    reconnectionDelay: 3000 // (Number) how long to initially wait before attempting a new (1000)
  });
};
