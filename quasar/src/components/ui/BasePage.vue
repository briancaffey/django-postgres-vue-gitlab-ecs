<template>
  <div :style-fn="getStyle">
    <q-page-container :class="$store.getters.isDark ? 'bg-grey-10' : ''">
      <q-page padding :class="$store.getters.isDark ? 'bg-grey-10' : ''">
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
    },
  },
};
</script>

<style></style>
