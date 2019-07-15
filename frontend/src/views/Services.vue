<template>
  <div class="nav">
    <h1>Services</h1>

    <a href="/admin">Django Admin</a> |
    <a href="/flower">Flower</a> |
    <a href="http://localhost:8025">Mailhog</a> |
    <a href="http://localhost:8081">Redis Commander</a>

    <h1>Debugging</h1>

    <button @click="sendTestEmail">Send a test email</button>

  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    methods: {
      sendTestEmail() {
        axios.get('/api/debug/send-test-email/').then(
          () => {
            window.open('http://localhost:8025', '_blank');
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