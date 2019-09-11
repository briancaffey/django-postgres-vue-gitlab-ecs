<template>
  <h4 :class="$store.getters.isDark ? 'dark-mode' : 'light-mode'">
    <slot></slot>
  </h4>
</template>

<script>
export default {};
</script>
