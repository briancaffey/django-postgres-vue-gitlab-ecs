<template>
  <base-page>Logging in with {{ provider }}...</base-page>
</template>

<script>
import * as Cookies from "js-cookie";
import apiCall from "../../utils/api";
export default {
  methods: {
    handleOauthCallback() {
      const provider = this.$route.params.provider;
      apiCall
        .post(`/api/social/${provider}/`, { code: this.$route.query.code })
        .then(resp => {
          Cookies.set("refresh-token", resp.data.refresh);
          Cookies.set("user-token", resp.data.access);
          window.location.href = "/";
        });
    }
  },
  created() {
    this.handleOauthCallback();
  },
  computed: {
    provider() {
      return this.$route.params.provider;
    }
  }
};
</script>

<style lang="scss" scoped></style>
