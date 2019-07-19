<template>
  <div>
    <q-page class="flex flex-center">
      <q-color v-model="hexa" inline class="my-picker" />
    </q-page>
  </div>
</template>

<script>
export default {
  data() {
    return {
      hexa: "#000000"
    };
  }
};
</script>

<style lang="css" scoped>
</style>