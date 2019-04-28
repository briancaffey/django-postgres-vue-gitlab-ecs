<template>
  <div>
    <h1>Profile</h1>
    {{ profile.email }}
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  export default {
    name: 'account',
    computed: {
      ...mapState({profile: state => state.user.profile})
    }
  }
</script>

<style lang="scss" scoped>

</style>