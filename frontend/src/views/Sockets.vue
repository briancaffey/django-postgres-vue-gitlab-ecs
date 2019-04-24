<template>
  <div>
    <h1>
    Sockets
    </h1>
    {{ isConnected }}
  </div>
</template>

<script>
  export default {
    data() {
      return {
        isConnected: false,
      }
    },
    sockets: {
      connect: function () {
        this.isConnected = true;
        console.log('socket connected')
      },
    },
    // methods: {
    //   pingServer() {
    //     this.$socket.emit('', 'my message');
    //   }
    // }
  }
</script>

<style lang="scss" scoped>

</style>