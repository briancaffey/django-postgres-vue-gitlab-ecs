<template>
  <q-layout
    view="lHh Lpr lFf"
    :class="$store.getters.isDark ? 'bg-grey-10' : ''"
  >
    <q-ajax-bar ref="bar" position="top" color="info" size="4px" />
    <main-header />

    <main-left-drawer />

    <transition name="fade" mode="out-in">
      <router-view />
    </transition>
  </q-layout>
</template>

<script>
export default {
  name: "MainLayout",
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
