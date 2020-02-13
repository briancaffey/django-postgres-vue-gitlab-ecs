<template>
  <base-page>
    <page-header>Hacker News Clone</page-header>
    <upload-form />
    <base-btn @click.native="$store.commit('hn/upload/toggleUploadForm')"
      >New Link</base-btn
    ><br /><br />

    <div class="links-wrapper">
      <hacker-news-link
        v-for="(link, i) in $store.getters['hn/getLinks']"
        :key="i"
        :linkInfo="link"
      />
    </div>
  </base-page>
</template>

<script>
import HackerNewsLink from "./HackerNewsLink.vue";
import UploadForm from "./UploadForm.vue";
export default {
  components: {
    HackerNewsLink,
    UploadForm
  },
  created() {
    this.$store.dispatch("hn/getLinks", { vm: this });
  }
};
</script>

<style scoped>
.links-wrapper {
  display: grid;
  gap: 10px;
}
</style>
