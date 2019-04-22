<template>
  <div class="login">
    <h1 data-test="signin-message">Login</h1>
    <form>
      <div class="login">
        <input class="signin" id="email" placeholder="Email" v-model="email">
        <input class="signin" id="password" placeholder="Password" type="password" v-model="password">
        <button
          @click.prevent="login">
          Login
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { AUTH_REQUEST } from '@/store/actions/auth';
import { mapGetters } from 'vuex';

export default {
  name: 'login',
  data() {
    return {
      email: process.env.NODE_ENV === 'production' ? '' : 'admin@company.com',
      password: process.env.NODE_ENV === 'production' ? '' : 'password',
    };
  },
  methods: {
    login() {
      const { email, password } = this;
      this.$store.dispatch(AUTH_REQUEST, { email, password }).then(() => {
        this.$router.push('/');
      });
    },
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'authStatus']),
    loading() {
      return this.authStatus === 'loading' && !this.isAuthenticated;
    },
  },
};
</script>

<style scoped>
  .login {
    text-align: center;
    display: flex;
    flex-direction: column;
    width: 300px;
    padding: 10px;
    margin:auto;
  }
  .signin {
    -webkit-appearance: none;
    margin-bottom: 5px;
    border:1 solid black;
    display:block;
    text-align:center;
    outline: none !important;
    box-shadow: none !important;
    border-radius: 3px;
  }
</style>
