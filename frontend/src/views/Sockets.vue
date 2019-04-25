<template>
  <div>
    <h1>
    Sockets
    </h1>
    {{ isConnected }}
    <input placeholder="type message" v-model="message">
    <button @click="sendMessage">Click me</button>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        message: '',
        isConnected: false,
      }
    },
    methods: {
      sendMessage(message){
        console.log("clicking")
        this.$socket.send(JSON.stringify({"message":this.message}))
      }
    },
    created() {
    }
    // methods: {
    //   pingServer() {
    //     this.$socket.emit('', 'my message');
    //   }
    // }
  }
</script>

<style lang="scss" scoped>

</style>