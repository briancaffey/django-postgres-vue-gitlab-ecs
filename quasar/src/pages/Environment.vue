<template>
  <base-page>
    <p v-for="(value, key) in env" :key="key">{{ key }}: {{ value }}</p>
  </base-page>
</template>

<script>
export default {
  created() {
    console.log(JSON.stringify(process.env));
  },
  data() {
    return {
      env: process.env
    };
  }
};
</script>

<style lang="scss" scoped></style>
