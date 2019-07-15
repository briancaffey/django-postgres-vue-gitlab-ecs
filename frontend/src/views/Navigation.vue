<template>
  <div class="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <span><router-link to="/chat">Chat</router-link> | </span>
      <span v-if="$store.getters.isAuthenticated"><router-link to="/profile">Profile</router-link> | </span>
      <span v-if="$store.getters.isAuthenticated"><router-link to="/services">Services</router-link> | </span>
      <router-link v-if="!$store.getters.isAuthenticated" to="/login">Login</router-link>
      <span><a v-if="$store.getters.isAuthenticated" href="#logout" @click="logout">Logout</a></span>
  </div>
</template>

<script>
import { AUTH_LOGOUT } from '@/store/actions/auth';
import { mapGetters } from 'vuex'

export default {
  methods: {
    logout: function () {
      this.$store.dispatch(AUTH_LOGOUT).then(() => {
        this.$router.push('/login')
      });
      location.reload();
    },

  },
  computed: {
    ...mapGetters(['isAuthenticated']),
  }
}
</script>

<style lang="scss">

</style>