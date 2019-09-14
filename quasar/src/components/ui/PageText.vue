<template>
  <p
    :style="`font-size:${size}rem`"
    :class="$store.getters.isDark ? 'dark-mode' : 'light-mode'"
  >
    <slot></slot>
  </p>
</template>

<script>
export default {
  props: {
    size: {
      type: Number,
      default: 1.25
    }
  }
};
</script>
