<template>
  <div>
    <q-dialog @hide="hideLoginMenu" v-model="visible">
      <q-card style=" max-width: 95%; min-width: 320px;">
        <q-card-section>
          <div class="text-h6">Login</div>
        </q-card-section>
        <q-form @submit="login">
          <q-card-section>
            <q-input
              id="email"
              v-model="email"
              type="text"
              label="Email"
              autofocus
            />
            <q-input
              id="password"
              type="password"
              v-model="password"
              label="Password"
            />
          </q-card-section>

          <q-card-actions align="right" class="text-primary">
            <q-btn tabindex="-1" flat label="Cancel" v-close-popup />
            <q-btn
              id="login-btn"
              flat
              label="Login"
              type="submit"
              v-close-popup
            />
          </q-card-actions>
                <a  class="q-btn"
        :href="githuboath2link"
      >GitHub</a>
          <br>

        </q-form>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
// import axios from 'axios';
import buildURL from 'axios/lib/helpers/buildURL';
export default {
  data() {
    return {
      params: {
        client_id: 'd6639d522598d6bf20f4',
        redirect_uri: "http://localhost/auth/github/callback",
        login: "",
        scope: "user",
        state: "eworifjeovivoiej",
      },
      githuboath2link: '',
      githuboauth2: "https://github.com/login/oauth/authorize",
      email: process.env.NODE_ENV === "production" ? "" : "admin@company.com",
      password: process.env.NODE_ENV === "production" ? "" : "password"
    };
  },
  created() {
    this.githuboath2link = buildURL(this.githuboauth2, this.params);
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
      const vm = this;
      this.$store
        .dispatch("AUTH_REQUEST", {
          email: this.email,
          password: this.password
        })
        .then(() => {
          if (vm.$store.getters.getNextLink) {
            vm.$router.push(vm.$store.getters.getNextLink);
          }
          const refreshFrequency =
            process.env.NODE_ENV === "development" ? 0.1 : 4;
          setInterval(() => {
            vm.$store.dispatch("AUTH_REFRESH");
          }, 1000 * 60 * refreshFrequency);
        });
      this.email = "";
      this.password = "";
    }
  }
};
</script>

<style lang="scss" scoped></style>
