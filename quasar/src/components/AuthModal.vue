<template>
  <div>
    <q-dialog @hide="hideAuthMenu" v-model="visible">
      <q-card style=" max-width: 95%; min-width: 320px;">
        <q-tabs
          v-model="tab"
          dense
          align="justify"
          class="bg-primary text-white shadow-2"
          :breakpoint="0"
        >
          <q-tab name="login" icon="vpn_key">Login</q-tab>
          <q-tab name="signup" icon="account_circle">Sign Up</q-tab>
        </q-tabs>
        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="login">
            <q-form @submit="login">
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
              <q-btn type="a" class="full-width q-mt-md" :href="githuboath2link"
                >GitHub</q-btn
              >
              <br />
            </q-form>
          </q-tab-panel>

          <q-tab-panel name="signup">
            <div class="text-h6">TODO</div>
            Implement Sign up with Email + Email Verification
            <q-btn
              :href="$store.getters.oauthUrl('github')"
              type="a"
              class="full-width q-mt-md"
              label="Sign Up with GitHub"
            />
            <q-btn
              :href="$store.getters.oauthUrl('google')"
              type="a"
              class="full-width q-mt-md"
              label="Sign Up with Google"
            />
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
// import axios from 'axios';
import buildURL from "axios/lib/helpers/buildURL";
export default {
  data() {
    return {
      tab: "login",
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
        return this.$store.getters.authModalVisible;
      },
      set() {}
    }
  },
  methods: {
    hideAuthMenu() {
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
