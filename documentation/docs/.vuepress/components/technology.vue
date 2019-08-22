<template>
  <div>
    <img :src="$withBase(`/${image}`)" alt="Logo">
  </div>
</template>

<script>
  export default {
    props: {
      image: {
        type: String,
        default: ''
      },
    },
    name: "technology"
  }
</script>

<style scoped>
img {
  width: 100px;
  margin-top: 20px;
}
</style>