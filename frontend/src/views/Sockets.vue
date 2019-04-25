<template>
  <div>
    <h1>
    WebSocket Chat Room
    </h1>
    <div ref="chat-area" class="chat-area">
      <p v-for="(m, i) in messages" :key="i">
        {{ m }}
      </p>
    </div>
    <input ref="message" placeholder="type your message..." v-model="message">
    <button @click="sendMessage(message)">Send</button>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        message: '',
        messages: []
      }
    },
    methods: {
      sendMessage(message){
        var outboundMessage = message;
        this.message = '';
        this.$socket.send(JSON.stringify({"message":outboundMessage}));
        this.$refs.message.focus();
      },
      scrollToBottom() {
        const messageDisplay = this.$refs["chat-area"];
        console.log(messageDisplay.scrollHeight);
        setTimeout(() => {messageDisplay.scrollTop = messageDisplay.scrollHeight;}, 1)
      }
    },
    created() {
      this.$options.sockets.onmessage = (data) => {
        const message = JSON.parse(data.data);
        this.messages.push(message['message']);
        this.scrollToBottom();
      }
    }
  }
</script>

<style lang="scss" scoped>
.chat-area {
  margin: auto;
  align-content: center;
  min-height: 200px;
  max-height: 200px;
  overflow: scroll;
  overflow-x: hidden;
  min-width: 300px;
  max-width: 50px;
}
input {
  margin-right: 5px;
  border-radius: 3px;
  padding: 3px;
  outline: none;
  border: 1px solid #dddddd;
}
</style>