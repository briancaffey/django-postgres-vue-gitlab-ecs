<template>
  <div class="about">
    <h1>This is an about page!</h1>
    <p>Updates coming soon...</p>
    <p>Message from the backend API: {{ message | capitalize }}</p>
    <p>The commit SHA of the backend container: {{ gitSHA }}</p>
    <p>The commit SHA of the frontend site: {{ commit }}</p>

  </div>
</template>

<script>
  import apiCall from '@/utils/api';
  export default {
    data() {
      return {
        message: '...',
        gitSHA: '<backend git sha>',
        commit: process.env.VUE_APP_CI_COMMIT_SHORT_SHA || '<frontend git sha>',
      }
    },
    created(){
      this.fetchMessage();
    },
    methods: {
      fetchMessage: function(){
        apiCall.get('/api/hello-world').then(
          (resp) => {
            this.message = resp.data.message;
            this.gitSHA = resp.data.git_sha;
          }
        )
      }
    },
  }
</script>

<style scoped>

</style>