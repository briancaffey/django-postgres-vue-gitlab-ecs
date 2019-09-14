<template>
  <base-page>
    <div class="login">
      <page-header>Sign Up</page-header>
      <base-card style="max-width: 95%; min-width: 320px; padding: 20px;">
        <sign-up-form></sign-up-form>
      </base-card>
      <span class="login_link">
        <router-link to="/login"><page-text>Login</page-text></router-link>
      </span>
    </div>
  </base-page>
</template>

<script>
import SignUpForm from "components/auth/SignUpForm.vue";
export default {
  components: {
    SignUpForm
  }
};
</script>

<style scoped>
.login {
  text-align: center;
  display: grid;
  justify-content: center;
}

.login_link {
  text-align: right;
  margin-top: 10px;
}
</style>
