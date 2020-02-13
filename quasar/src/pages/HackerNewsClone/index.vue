<template>
  <base-page>
    <page-header>Hacker News Clone</page-header>
    <div v-for="(link, i) in $store.getters['hn/getLinks']" :key="i">
      {{ link.url }}

      <div v-for="(vote, j) in link.votes" :key="j">
        {{ vote.id }} {{ vote.user.email }}
      </div>
    </div>
  </base-page>
</template>

<script>
export default {
  created() {
    this.$store.dispatch("hn/getLinks", { vm: this });
  }
};
</script>

<style scoped></style>
