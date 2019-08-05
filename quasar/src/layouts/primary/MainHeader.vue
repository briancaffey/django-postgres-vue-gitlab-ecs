<template>
  <q-header>
    <q-toolbar>
      <q-btn
        id="toggleLeftDrawer"
        flat
        dense
        round
        @click="toggleLeftDrawer"
        aria-label="Menu"
      >
        <q-icon name="menu" />
      </q-btn>

      <q-toolbar-title>Verbose Equals True</q-toolbar-title>
      <q-btn
        id="login"
        :ripple="false"
        color="white"
        text-color="primary"
        label="Login"
        v-if="!$store.getters.isAuthenticated"
        no-caps
        @click="$store.commit('toggleLoginMenu')"
      />
      <q-btn
        id="logout"
        :ripple="false"
        color="white"
        text-color="primary"
        label="Logout"
        v-if="$store.getters.isAuthenticated"
        no-caps
        @click="logout"
      />
      <auth-modal />
    </q-toolbar>
  </q-header>
</template>

<script>
import AuthModal from "components/AuthModal.vue";

export default {
  components: { AuthModal },
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
