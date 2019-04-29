<template>
  <div>
    <h1>{{ roomName }}</h1>
    <chat-area :sender="sender" :messages="messages" />
    <input ref="message" placeholder="type your message..." v-model="message">
    <button @click="sendMessage(message)">Send</button>
  </div>
</template>

<script>
  import Vue from 'vue';
  import faker from 'faker';
  import {
    CHAT_GET_OR_CREATE_ROOM,
    CHAT_GET_MESSAGE
  } from '@/store/actions/chat';
  import uuid from 'uuid';
  import ChatArea from './ChatArea.vue';

  export default {
    components: {ChatArea},
    data() {
      return {
        message: '',
        connection: null,
        roomName: ''
      }
    },
    computed: {
      messages() {
        return this.$store.getters.messages(this.roomName);
      },
      sender() {
        return this.$store.getters.sender(this.roomName);
      }
    },
    methods: {
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
    },
    created() {
      this.roomName = this.$route.params.room;

      this.connection = new Vue();
      this.connection.$connect(
        `ws://localhost/ws/chat/${this.roomName}/`
      );
      const _this = this
      this.$options.sockets.onmessage = (data) => {
        const message = JSON.parse(data.data);
        this.$store.commit(
          CHAT_GET_MESSAGE,
          {'message': message, 'roomName': this.roomName}
        );
      }
      const sender = uuid();
      this.$store.commit(
        CHAT_GET_OR_CREATE_ROOM,
        {'roomName': this.roomName, 'sender': sender}
      );
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

</style>