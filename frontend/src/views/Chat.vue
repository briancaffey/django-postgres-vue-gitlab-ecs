<template>
  <div>
    <div v-if="!$route.params.room">
    <h1>Create or join a new chat room</h1>
      <input type="text" v-model="roomName" placeholder="Select a chat room..">
      <button @click="enterChatRoom">Enter Room</button>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
  import slugify from 'slugify';
  export default {
    data() {
      return {
        roomName: '',
      }
    },
    methods: {
      enterChatRoom(){
        const slug = slugify(this.roomName, {remove: /[*+~.()'"!:@]/g});
        this.$router.push(`/chat/${slug}`);
      }
    },
  }
</script>

<style lang="scss" scoped>

</style>