<template>
  <q-toggle v-model="dark" :color="$store.getters.isDark ? 'black' : 'white'" />
</template>

<script>
export default {
  computed: {
    dark: {
      get() {
        return this.$store.getters.isDark;
      },
      set() {
        this.$store.commit("toggleDarkMode");
      },
    },
  },
};
</script>

<style lang="scss" scoped></style>
