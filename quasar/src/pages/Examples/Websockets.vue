<template>
  <base-page>
    <page-header>Websockets example</page-header>
    <page-sub-header>Ping Pong: {{ wsUrl }}</page-sub-header>
    <base-btn id="ping" @click.native="sendPing">Send Ping</base-btn>
    <br /><br />
    <div class="cards">
      <base-card
        dark
        color="teal"
        text-color="white"
        class="pong"
        v-for="(pong, i) in pongs"
        :key="i"
      >
        Cached Value: {{ pong["cached_value"] }}<br />
        Vue Ping: 0 ({{ pong["vue_ping"] }}) <br />
        Server Recv: +{{ pong["server_recv_ping"] - pong["vue_ping"] }} ms<br />
        Server Send Pong: +{{
          pong["server_send_pong"] - pong["vue_ping"]
        }}
        ms<br />
        Vue Recv Pong: +{{ pong["vue_recv_pong"] - pong["vue_ping"] }} ms
      </base-card>
    </div>
  </base-page>
</template>

<script>
export default {
  data() {
    return {
      wsUrl: process.env.WS_PING_PONG,
      pongs: [],
      showLatency: false
    };
  },
  created() {
    this.$connect(this.wsUrl, { format: "json" });
    this.$socket.onmessage = i => {
      console.log(i);
      const data = JSON.parse(i["data"]);
      data.vue_recv_pong = new Date().getTime();
      this.pongs.unshift(data);
    };
  },
  methods: {
    sendPing() {
      this.$socket.send(
        JSON.stringify({
          message: "ping",
          sender: 1,
          ts: new Date().getTime()
        })
      );
    }
  },
  destroyed() {
    this.$disconnect();
  }
};
</script>

<style scoped>
.cards {
  display: grid;
  grid-gap: 10px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.pong {
  padding: 10px;
}
</style>
