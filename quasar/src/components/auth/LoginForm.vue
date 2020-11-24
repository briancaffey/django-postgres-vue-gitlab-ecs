<template>
  <q-form @submit.prevent="login">
    <q-input
      :color="$store.getters.isDark ? 'black' : 'primary'"
      :dark="$store.getters.isDark"
      id="email"
      v-model="email"
      type="text"
      label="Email"
      autofocus
    />
    <q-input
      :color="$store.getters.isDark ? 'black' : 'primary'"
      :dark="$store.getters.isDark"
      id="password"
      type="password"
      v-model="password"
      label="Password"
    />

    <q-card-actions align="right" class="text-primary">
      <q-btn
        :color="$store.getters.isDark ? 'black' : 'primary'"
        id="login-btn"
        flat
        label="Login"
        type="submit"
        v-close-popup
      />
    </q-card-actions>
  </q-form>
</template>

<script>
export default {
  data() {
    return {
      email: process.env.NODE_ENV === "production" ? "" : "admin@company.com",
      password: process.env.NODE_ENV === "production" ? "" : "password",
    };
  },
  methods: {
    login() {
      const vm = this;
      const { email, password } = this;
      this.$store
        .dispatch("AUTH_REQUEST", {
          email,
          password,
        })
        .then(() => {
          vm.$router.push("/");
          console.log("login success");
        });
      this.email = "";
      this.password = "";
    },
  },
};
</script>

<style lang="scss" scoped></style>
