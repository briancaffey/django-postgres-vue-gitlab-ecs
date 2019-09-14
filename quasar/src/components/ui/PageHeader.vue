<template>
  <h3 :class="$store.getters.isDark ? 'dark-mode' : 'light-mode'">
    <slot></slot>
  </h3>
</template>

<script>
export default {};
</script>
