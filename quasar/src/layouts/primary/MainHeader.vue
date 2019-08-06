<template>
  <q-header>
    <q-toolbar>
      <q-btn
        id="toggleLeftDrawer"
        flat
        dense
        round
        @click="toggleLeftDrawer"
        aria-label="Menu"
      >
        <q-icon name="menu" />
      </q-btn>

      <q-toolbar-title>Verbose Equals True</q-toolbar-title>

      <q-select v-model="lang" :options="langs" />
      <q-btn
        id="login"
        :ripple="false"
        color="white"
        text-color="primary"
        label="Login"
        v-if="!$store.getters.isAuthenticated"
        no-caps
        @click="$store.commit('toggleLoginMenu')"
      />
      <q-btn
        id="logout"
        :ripple="false"
        color="white"
        text-color="primary"
        label="Logout"
        v-if="$store.getters.isAuthenticated"
        no-caps
        @click="logout"
      />
      <auth-modal />
    </q-toolbar>
  </q-header>
</template>

<script>
import AuthModal from "components/AuthModal.vue";

export default {
  data() {
    return {
      lang: this.$i18n.locale,
      langs: [
        {
          label: "Chinese",
          value: "cn-cn"
        },
        {
          label: "US English",
          value: "en-us"
        }
      ]
    };
  },
  components: { AuthModal },
  methods: {
    logout() {
      this.$store.dispatch("AUTH_LOGOUT").then(() => this.$router.push("/"));
      this.$router.go();
    },
    toggleLeftDrawer() {
      this.$store.commit("toggleLeftDrawer");
    }
  },
  created() {
    this.$i18n.locale = "cn-cn";
  },
  watch: {
    lang(lang) {
      this.$i18n.locale = lang;
      // import(`quasar/i18n/${lang}`).then(language => {
      //   this.$q.lang.set(language.default)
      // })
    }
  }
};
</script>

<style lang="scss" scoped></style>
