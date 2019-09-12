<template>
  <q-card
    :dark="$store.getters.isDark"
    :class="$store.getters.isDark ? 'bg-grey-8' : 'bg-grey-2'"
    ><slot></slot
  ></q-card>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped></style>
