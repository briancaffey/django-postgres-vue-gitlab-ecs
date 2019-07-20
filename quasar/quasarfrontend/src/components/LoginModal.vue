<template>
  <div>
    <q-dialog @hide="hideLoginMenu" v-model="visible">
      <q-card style=" max-width: 95%; min-width: 320px;">
        <q-card-section>
          <div class="text-h6">Login</div>
        </q-card-section>
        <q-form @submit="login">
          <q-card-section>
            <q-input v-model="email" type="text" label="Email" autofocus />
            <q-input type="password" v-model="password" label="Password" />
          </q-card-section>

          <q-card-actions align="right" class="text-primary">
            <q-btn tabindex="-1" flat label="Cancel" v-close-popup />
            <q-btn flat label="Login" type="submit" v-close-popup />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: process.env.NODE_ENV === "production" ? "" : "admin@company.com",
      password: process.env.NODE_ENV === "production" ? "" : "password"
    };
  },
  computed: {
    visible: {
      get() {
        return this.$store.getters.loginModalVisible;
      },
      set() {}
    }
  },
  methods: {
    hideLoginMenu() {
      this.$store.commit("toggleLoginMenu");
    },
    login() {
      const vm = this
      this.$store
        .dispatch("AUTH_REQUEST", {
          email: this.email,
          password: this.password
        })
        .then(() => {
          const refreshFrequency =
            process.env.NODE_ENV === "development" ? 0.1 : 4;
          setInterval(() => {
            vm.$store.dispatch("AUTH_REFRESH");
          }, 1000 * 60 * refreshFrequency);
          console.log("Logged in...");
        });
      this.email = "";
      this.password = "";
    }
  }
};
</script>

<style lang="scss" scoped>
</style>