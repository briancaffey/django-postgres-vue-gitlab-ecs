<template>
  <div>
    <q-page class="flex flex-center">
          <h2>Hello</h2>
      <q-item>
        Welcome to Verbose Equals True
      </q-item>
      <q-color v-model="hexa" inline class="my-picker" />
    </q-page>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        hexa: '#000000'
      }
    },
  }
</script>

<style lang="scss" scoped>

</style>