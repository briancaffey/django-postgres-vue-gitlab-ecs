<template>
  <div :style-fn="getStyle">
    <q-page-container>
      <q-page padding>
        <slot></slot>
      </q-page>
    </q-page-container>
  </div>
</template>

<script>
export default {
  methods: {
    getStyle() {
      return { color: "white" };
    }
  }
};
</script>

<style lang="scss" scoped></style>
