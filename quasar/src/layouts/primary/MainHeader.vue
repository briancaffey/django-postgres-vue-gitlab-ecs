<template>
  <q-header
    :style="
      $store.getters.isDark
        ? 'background:linear-gradient(45deg, purple, teal)'
        : 'background:linear-gradient(135deg, red, orange)'
    "
  >
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

      <dark-mode></dark-mode>
      <span class="lang">
        <emoji
          :native="false"
          height="100%"
          :sheetSize="64"
          :emoji="lang.emoji"
          :size="28"
        />
      </span>
      <q-select dark dense color="white" v-model="lang" :options="langs" />

      <q-btn
        id="login"
        :ripple="false"
        color="white"
        text-color="primary"
        label="Login"
        v-if="!$store.getters.isAuthenticated"
        no-caps
        @click="$router.push('/login')"
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
    </q-toolbar>
  </q-header>
</template>

<script>
export default {
  data() {
    return {
      showing: false,
      lang: {
        label: "US English",
        value: "en-us",
        emoji: ":flag-us:"
      },
      langs: [
        {
          label: "US English",
          value: "en-us",
          emoji: ":flag-us:"
        },
        {
          label: "Chinese",
          value: "cn-cn",
          emoji: ":flag-cn:"
        }
      ]
    };
  },
  methods: {
    setLang(lang) {
      console.log(lang);
      this.lang = lang;
    },
    logout() {
      this.$store.dispatch("AUTH_LOGOUT").then(() => this.$router.push("/"));
      this.$router.go();
    },
    toggleLeftDrawer() {
      this.$store.commit("toggleLeftDrawer");
    }
  },
  created() {
    this.$i18n.locale = "en-us";
  },
  watch: {
    lang(lang) {
      console.log(lang);
      this.$i18n.locale = lang.value;
      // import(`quasar/i18n/${lang}`).then(language => {
      //   this.$q.lang.set(language.default)
      // })
    }
  }
};
</script>

<style scoped>
.lang {
  margin-right: 15px;
  cursor: pointer;
  height: 28px;
}
.q-select {
  margin-right: 20px;
}
</style>
