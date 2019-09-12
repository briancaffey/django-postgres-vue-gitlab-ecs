<template>
  <base-page>
    <div class="login">
      <page-header>Login</page-header>
      <base-card class="card">
        <login-form></login-form>
      </base-card>
      <span class="signup">
        <router-link to="/signup"><page-text>Sign Up</page-text></router-link>
      </span>
    </div>
  </base-page>
</template>

<script>
import LoginForm from "components/auth/LoginForm.vue";
export default {
  components: {
    LoginForm
  }
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
