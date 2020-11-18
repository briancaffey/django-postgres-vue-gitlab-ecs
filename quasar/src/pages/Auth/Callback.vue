<template>
  <base-page>
    <page-text> Logging in with {{ provider }}... </page-text>
  </base-page>
</template>

<script>
export default {
  methods: {
    handleOauthCallback() {
      const provider = this.$route.params.provider;
      this.$axios
        .post(`/api/social/${provider}/`, { code: this.$route.query.code })
        .then((resp) => {
          localStorage.setItem("user-token", "success");
          window.location.href = "/";
        });
    },
  },
  created() {
    this.handleOauthCallback();
  },
  computed: {
    provider() {
      return this.$route.params.provider;
    },
  },
};
</script>

<style lang="scss" scoped></style>
