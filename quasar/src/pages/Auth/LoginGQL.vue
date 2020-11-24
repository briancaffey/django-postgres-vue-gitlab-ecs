<template>
  <base-page>
    <div class="login">
      <page-header>Login</page-header>
      <gql-login-form />
    </div>
  </base-page>
</template>

<script>
import GqlLoginForm from "./GqlLoginForm.vue";
export default {
  components: {
    GqlLoginForm,
  },
};
</script>

<style scoped>
.login {
  text-align: center;
  display: grid;
  justify-content: center;
}

.card {
  max-width: 95%;
  min-width: 320px;
  padding: 20px;
}

.signup {
  text-align: right;
  margin-top: 10px;
}
</style>
