<template>
  <div class="nav">
    <h1>Services</h1>

    <a href="/admin">Django Admin</a> |
    <a :href=flowerUrl>Flower</a>
    <span v-if="!production"> |<a href="http://localhost:8025">Mailhog</a></span>
    <span v-if="!production"> |<a href="http://localhost:8081">Redis Commander</a></span>

    <h1>Debugging</h1>

    <button @click="sendTestEmail">Send a test email</button>

  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        production: env.process.NODE_ENV === 'production',
      }
    },
    methods: {
      sendTestEmail() {
        axios.get('/api/debug/send-test-email/').then(
          () => {
            if (env.process.NODE_ENV !== 'production') {
              window.open('http://localhost:8025', '_blank');
            }
          }
        ).catch(
          (err) => {
            console.log("error sending test email");
            this.$router.push('/');
          }
        )
      }
    }
  }
</script>

<style lang="scss" scoped>

</style>