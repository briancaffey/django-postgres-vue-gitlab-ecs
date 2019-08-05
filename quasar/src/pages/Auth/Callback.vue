<template>
  <base-page>Logging in with GitHub...</base-page>
</template>

<script>
import * as Cookies from "js-cookie";
import axios from "axios";
export default {
  methods: {
    githubAuth() {
      const provider = this.$route.params.provider;
      axios
        .post(`/api/social/${provider}/`, { code: this.$route.query.code })
        .then(resp => {
          Cookies.set("refresh-token", resp.data.refresh);
          Cookies.set("user-token", resp.data.access);
          window.location.href = "/";
        });
    }
  },
  created() {
    this.githubAuth();
  }
};
</script>

<style lang="scss" scoped></style>
