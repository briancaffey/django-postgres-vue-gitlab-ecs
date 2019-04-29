<template>
    <div ref="chat-area" class="chat-area">
      <div v-for="(m, i) in messages" :key="i">
        <div :key="sender + i" class="userMessageWrapper"  v-if="m['sender'] === sender">
          <div v-if="m['user']" class="user-name"><small>{{ m['user'] }}</small></div>
          <div v-else class="user-name"><small>guest</small></div>
          <span class="userMessage">{{ m.message }}</span>
        </div>
        <div :key="sender + i" class="otherMessageWrapper" v-else>
          <div v-if="m['user']" class="user-name"><small>{{ m['user'] }}</small></div>
          <div v-else class="user-name"><small>guest</small></div>
          <span class="otherMessage">{{ m.message }}</span>
        </div>
      </div>
    </div>
</template>

<script>
  export default {
    props: ['messages', 'sender'],
    methods: {
      scrollDown(){
        const messageDisplay = this.$refs["chat-area"];
        setTimeout(() => {
            messageDisplay.scrollTop = messageDisplay.scrollHeight;
          }, 1
        );
      }
    },
    watch: {
      messages: function() {
        this.scrollDown();
      }
    },
    mounted: function() {
      this.scrollDown();
    }
  }
</script>

<style lang="scss" scoped>
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

.user-name {
  color: white;
  font-size: .5em;
}
</style>