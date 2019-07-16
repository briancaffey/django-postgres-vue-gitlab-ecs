<template>
  <div class="nav">
    <h1>Services</h1>

    <a href="/admin">Django Admin</a> |
    <a :href=flowerUrl>Flower</a>
    <span v-if="!production"> | <a href="http://localhost:8025">Mailhog</a></span>
    <span v-if="!production"> | <a href="http://localhost:8081">Redis Commander</a></span>

    <h1>Debugging</h1>

    <button @click="sendTestEmail">Send a test email</button>

  </div>
</template>

<script>
  import apiCall from '@/utils/api';
  export default {
    data() {
      return {
        production: process.env.NODE_ENV === 'production',
      }
    },
    computed: {
      flowerUrl() {
        return this.production
        ? `https://flower.${process.env.VUE_APP_SITE_DOMAIN}`
        : `http://localhost/flower`;
      }
    },
    methods: {
      sendTestEmail() {
        apiCall.get('/api/debug/send-test-email/').then(
          () => {
            if (process.env.NODE_ENV !== 'production') {
              window.open('http://localhost:8025', '_blank');
            }
          }
        ).catch(
          () => {
            this.$router.push('/');
          }
        )
      }
    }
  }
</script>

<style lang="scss" scoped>

</style>