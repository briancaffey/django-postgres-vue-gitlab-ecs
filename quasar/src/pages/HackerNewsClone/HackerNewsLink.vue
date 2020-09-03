<template>
  <div>
    <base-card class="link">
      <div class="link-contents">
        <b>{{ linkInfo.description }}</b> (<a :href="linkInfo.url">{{
          linkInfo.url
        }}</a
        >)
        <span style="float: right;" v-if="linkInfo.postedBy">
          posted by {{ linkInfo.postedBy.email }}
        </span>
      </div>
    </base-card>
  </div>
</template>

<script>
export default {
  props: {
    linkInfo: {
      type: Object,
      default: () => {},
    },
  },
};
</script>

<style scoped>
.link {
  padding: 10px;
}
a {
  text-decoration: none;
  color: white;
}
</style>
