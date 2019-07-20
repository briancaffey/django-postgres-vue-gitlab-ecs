<template>
  <q-btn :to="link" :icon="icon" :type="type" :target="target" :href="href">{{ name }}</q-btn>
</template>

<script>
export default {
  props: {
    href: {
      type: String,
      default: "#"
    },
    name: {
      type: String,
      default: ""
    },
    icon: {
      type: String,
      default: ""
    },
    target: {
      type: String,
      default: "_blank"
    },
    type: {
      type: String,
      default: "button"
    }
  }
};
</script>

<style lang="scss" scoped>
</style>