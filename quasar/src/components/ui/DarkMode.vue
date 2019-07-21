<template>
    <q-toggle v-model="dark" color="black" />
</template>

<script>
export default {
  data() {
    return {
      darkMode: true
    }
  },
  computed: {
    dark: {
      get() {
        return this.$store.getters.isDarkMode;
      },
      set() {
        this.$store.commit('toggleDarkMode');
      }
    }
  }
};
</script>

<style lang="scss" scoped>
</style>