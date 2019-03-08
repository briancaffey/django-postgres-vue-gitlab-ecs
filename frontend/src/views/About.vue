<template>
  <div class="about">
    <h1>This is an about page</h1>
    <p>Updates coming soon...</p>
    <p>Message from the backend: {{ message }}</p>
  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        message: '',
      }
    },
    created(){
      this.fetchMessage();
    },
    methods: {
      fetchMessage: function(){
        axios.get('/api/hello-world').then(
          (resp) => {
            this.message = resp.data.message;
          }
        )
      }
    },
  }
</script>

<style scoped>

</style>