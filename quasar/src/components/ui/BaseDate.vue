<template>
  <div>
    <q-date
      v-bind="$attrs"
      v-on="$listeners"
      :dark="$store.getters.isDark"
    ></q-date>
  </div>
</template>

<script>
export default {};
</script>

<style scoped></style>
