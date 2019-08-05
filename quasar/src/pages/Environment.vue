<template>
  <base-page>
    <h4>Environment Variables</h4>
    <div v-for="(value, key) in env" :key="key">
      <q-chip>{{ key }}</q-chip
      ><q-chip text-color="white" color="teal">{{ value }}</q-chip>
    </div>
  </base-page>
</template>

<script>
export default {
  data() {
    return {
      env: process.env
    };
  }
};
</script>

<style lang="scss" scoped></style>
