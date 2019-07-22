<template>
  <div>
    <h4>Websockets example</h4>
    <h6>Ping Pong</h6>

    <q-btn @click="sendPing">Send Ping</q-btn>
  </div>
</template>

<script>
export default {
  created() {
    this.$connect(
      `ws://${process.env.LOCAL_IP}/ws/chat/pingpong/`, { format: "json" });
    const vm = this;
    this.$socket.onmessage = data => {
      console.log(data);
      vm.$q.notify("PONG");
    };
  },
  data() {
    return {
      ip: process.env.LOCAL_IP
    }
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
