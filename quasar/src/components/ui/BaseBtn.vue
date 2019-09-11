<template>
  <q-btn :color="color" text-color="black"><slot></slot></q-btn>
</template>

<script>
export default {
  props: {
    color: {
      type: String,
      default: "white"
    }
  },
  textColor: {
    type: String,
    default: "black"
  }
};
</script>

<style lang="scss" scoped></style>
