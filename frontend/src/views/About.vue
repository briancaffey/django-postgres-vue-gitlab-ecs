<template>
  <div class="about">
    <h1>This is an about page</h1>
    <p>Updates coming soon...</p>
    <p>Message from the backend: {{ message }}</p>
    <p>No longer using CloudFront invalidations. Using cache control policies instead.</p>
  </div>
</template>

<script>
  import apiCall from '@/utils/api';
  export default {
    data() {
      return {
        message: '...',
      }
    },
    created(){
      this.fetchMessage();
    },
    methods: {
      fetchMessage: function(){
        apiCall.get('/api/hello-world').then(
          (resp) => {
            console.log(resp.data.message);
            this.message = resp.data.message;
          }
        )
      }
    },
  }
</script>

<style scoped>

</style>