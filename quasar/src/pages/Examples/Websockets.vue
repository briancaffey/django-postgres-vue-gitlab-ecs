<template>
  <div>
    <h4>Websockets example</h4>
    <h6>Ping Pong: {{ wsUrl }}</h6>

    <q-btn id="ping" @click="sendPing">Send Ping</q-btn>
  </div>
</template>

<script>
export default {
  data() {
    return {
      wsUrl: process.env.WS_PING_PONG
    }
  },
  created() {
    this.$connect(
      this.wsUrl, { format: "json" });
    const vm = this;
    this.$socket.onmessage = () => {
      vm.$q.notify({
        message: "PONG",
        classes: "pong"
      });
    };
  },
  methods: {
    sendPing() {
      this.$socket.send(
        JSON.stringify({
          message: "ping",
          sender: 1
        })
      );
    }
  },
  destroyed() {
    this.$disconnect();
  },
};
</script>

<style lang="scss" scoped></style>
