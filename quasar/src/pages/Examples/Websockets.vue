<template>
  <base-page>
    <h4>Websockets example</h4>
    <h6>Ping Pong: {{ wsUrl }}</h6>
    <q-btn id="ping" @click="sendPing">Send Ping</q-btn>

    <q-chip
      color="teal"
      text-color="white"
      class="pong"
      v-for="(pong, i) in pongs"
      :key="i"
      >PONG</q-chip
    >
  </base-page>
</template>

<script>
export default {
  data() {
    return {
      wsUrl: process.env.WS_PING_PONG,
      pongs: []
    };
  },
  created() {
    this.$connect(this.wsUrl, { format: "json" });
    this.$socket.onmessage = () => {
      this.pongs.push("PONG");
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
  }
};
</script>

<style lang="scss" scoped></style>
