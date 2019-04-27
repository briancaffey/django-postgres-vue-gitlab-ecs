<template>
  <div>
    <h1>
    {{ roomName }}
    </h1>
    <div ref="chat-area" class="chat-area">
      <div v-for="(m, i) in messages" :key="i">
        <div class="userMessageWrapper"  v-if="userIsSender(m['sender'])">
          <span class="userMessage">{{ m.message }}</span>
        </div>
        <div class="otherMessageWrapper" v-else>
          <span class="otherMessage">{{ m.message }}</span>
        </div>
      </div>
    </div>
    <input ref="message" placeholder="type your message..." v-model="message">
    <button @click="sendMessage(message)">Send</button>
  </div>
</template>

<script>
  import Vue from 'vue';
  import uuid from 'uuid';
  export default {
    data() {
      return {
        message: '',
        messages: [],
        sender: '',
        connection: null,
        roomName: ''
      }
    },
    methods: {
      userIsSender(sender){
        return this.sender === sender
      },
      sendMessage(message){
        var outboundMessage = message;
        this.message = '';
        this.$socket.send(JSON.stringify(
          {
            "message": outboundMessage,
            "sender": this.sender,
          })
        );
        this.$refs.message.focus();
      },
      scrollToBottom() {
        const messageDisplay = this.$refs["chat-area"];
        setTimeout(() => {
            messageDisplay.scrollTop = messageDisplay.scrollHeight;
          }, 1
        );
      }
    },
    created() {
      const protocol = process.env.VUE_APP_WS_PROTOCOL;
      const host = process.env.VUE_APP_BASE_HOST;
      this.roomName = this.$route.params.room;
      this.connection = new Vue();
      this.connection.$connect(
        `${protocol}${host}/ws/chat/${this.roomName}/`
      );
      this.sender = uuid();
      this.$options.sockets.onmessage = (data) => {
        const message = JSON.parse(data.data);
        this.messages.push(message);
        this.scrollToBottom();
      }
    },
    destroyed(){
      this.connection.$disconnect();
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
  margin-top: 5px;
  margin-right: 5px;
  border-radius: 3px;
  padding: 3px;
  outline: none;
  border: 1px solid #dddddd;
}
.userMessageWrapper {
  margin-bottom: 4px;
  text-align: right;
  background-color: #2c3e50;
  border-radius: 3px;
  padding: 5px;
}
.otherMessageWrapper {
  margin-bottom: 4px;
  text-align: left;
  background-color: #42b983;
  border-radius: 3px;
  padding: 5px;
}
.userMessage {
  text-align: left;
  color:white;

}
.otherMessage {
  text-align: left;
  color:white;
}
</style>