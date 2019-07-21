<template>
  <q-header>
    <q-toolbar>
      <q-btn flat dense round @click="toggleLeftDrawer" aria-label="Menu">
        <q-icon name="menu" />
      </q-btn>

      <q-toolbar-title>Verbose Equals True</q-toolbar-title>
      <q-btn
        :ripple="false"
        color="white"
        text-color="primary"
        label="Login"
        v-if="!$store.getters.isAuthenticated"
        no-caps
        @click="$store.commit('toggleLoginMenu')"
      />
      <q-btn
        :ripple="false"
        color="white"
        text-color="primary"
        label="Logout"
        v-if="$store.getters.isAuthenticated"
        no-caps
        @click="logout"
      />
      <login-modal />
    </q-toolbar>
  </q-header>
</template>

<script>
import LoginModal from "components/LoginModal.vue";

export default {
  components: { LoginModal },
  methods: {
    logout() {
      this.$store.dispatch("AUTH_LOGOUT").then(() => this.$router.push("/"));
      this.$router.go();
    },
    toggleLeftDrawer() {
      this.$store.commit("toggleLeftDrawer");
    }
  }
};
</script>

<style lang="scss" scoped></style>
