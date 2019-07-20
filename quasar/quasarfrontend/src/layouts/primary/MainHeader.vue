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
        no-caps
        @click="$store.commit('toggleLoginMenu')"
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
    toggleLeftDrawer() {
      this.$store.commit('toggleLeftDrawer')
    }
  }
};
</script>

<style lang="scss" scoped>
</style>