<template>
  <base-page>
    Loging in with Google...
  </base-page>
</template>

<script>
import * as Cookies from "js-cookie";
export default {
  methods: {
    googleAuth() {
      this.$axios
        .post("/api/social/google/", {
          code: this.$route.query.code,
        })
        .then((resp) => {
          Cookies.set("refresh-token", resp.data.refresh);
          Cookies.set("user-token", resp.data.access);
          window.location.href = "/";
        });
    },
  },
  created() {
    this.googleAuth();
  },
};
</script>

<style lang="scss" scoped></style>
