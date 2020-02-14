<template>
  <div id="q-app">
    <transition name="fade" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script>
export default {
  name: "App",

  created: function() {
    // if (this.$store.getters.isAuthenticated) {
    //   this.$store.dispatch("USER_REQUEST");
    //   // refresh the token every 4 minutes while the user is logged in in production
    //   // refresh every six seconds in development to ensure user stays logged in
    //   const refreshFrequency = process.env.NODE_ENV === "development" ? 2 : 4;
    //   setInterval(() => {
    //     this.$store.dispatch("AUTH_REFRESH");
    //   }, 1000 * 60 * refreshFrequency);
    // }
  }
  // TODO: set this in Vuex
  // const isDesktop = this.$q.platform.is.desktop;
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.15s;
  transition-property: opacity;
  transition-timing-function: ease;
}

.fade-enter,
.fade-leave-active {
  opacity: 0;
}
</style>
