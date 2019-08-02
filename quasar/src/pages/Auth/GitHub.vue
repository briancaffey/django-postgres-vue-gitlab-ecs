<template>
  <base-page>
    Logging in with GitHub...
  </base-page>
</template>

<script>
import * as Cookies from 'js-cookie'
import axios from 'axios';
  export default {
    methods: {
      githubAuth() {
        axios.post(
          '/api/social/github/',
          { "access_token": this.$route.query.code }
        )
          .then(resp => {
            Cookies.set("refresh-token", resp.data.refresh);
            Cookies.set("user-token", resp.data.access);
            window.reload();
        })
      }
    },
    created() {
      this.githubAuth();
    }
  }
</script>

<style lang="scss" scoped>

</style>