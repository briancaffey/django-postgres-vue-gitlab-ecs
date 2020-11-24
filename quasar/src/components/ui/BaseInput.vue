<template>
  <q-input v-bind="$attrs" v-on="$listeners" :dark="$store.getters.isDark">
    <template v-slot:prepend> <slot></slot> </template
  ></q-input>
</template>

<script>
export default {};
</script>

<style scoped></style>
