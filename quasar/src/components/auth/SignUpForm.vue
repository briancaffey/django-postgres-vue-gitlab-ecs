<template>
  <div>
    <q-form @submit="register">
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
          label="Sign Up"
          type="submit"
        />
      </q-card-actions>
    </q-form>
    <q-inner-loading :showing="visible">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      visible: false
    };
  },
  methods: {
    register() {
      this.visible = true;
      this.$registerUser(this.email, this.password)
        .then(() => {
          this.$q.notify({
            title: "User registered",
            message: "Thank you for registering!"
          });
          this.visible = false;
          this.$router.push("/");
        })
        .catch(() => {
          this.visible = false;
          this.$q.notify("There was an error.");
        });
    }
  }
};
</script>

<style lang="scss" scoped></style>
