<template>
  <base-card class="card">
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

      <q-card-actions align="right" class="text-primary login-btn">
        <q-btn
          class="full-width login-btn"
          :color="$store.getters.isDark ? 'black' : 'primary'"
          id="login-btn"
          label="Login"
          type="submit"
          v-close-popup
        />
      </q-card-actions>
    </q-form>
  </base-card>
</template>

<script>
export default {
  data() {
    return {
      email: process.env.NODE_ENV === "production" ? "" : "admin@company.com",
      password: process.env.NODE_ENV === "production" ? "" : "password"
    };
  },
  methods: {
    login() {
      this.$store.dispatch("gqljwt/authRequest", {
        email: this.email,
        password: this.password,
        vm: this
      });
    }
    // login() {
    //   const vm = this;
    //   this.$store
    //     .dispatch("AUTH_REQUEST", {
    //       email: this.email,
    //       password: this.password
    //     })
    //     .then(() => {
    //       vm.$router.push("/");
    //       const refreshFrequency =
    //         process.env.NODE_ENV === "development" ? 0.1 : 4;
    //       setInterval(() => {
    //         vm.$store.dispatch("AUTH_REFRESH");
    //       }, 1000 * 60 * refreshFrequency);
    //     });
    //   this.email = "";
    //   this.password = "";
    // }
  }
};
</script>

<style scoped>
.card {
  max-width: 95%;
  min-width: 320px;
  padding: 20px;
}
.login-btn {
  padding: 8px 0px;
}
</style>
