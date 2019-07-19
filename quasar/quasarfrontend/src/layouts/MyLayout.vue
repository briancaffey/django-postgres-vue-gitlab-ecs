<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar>
        <q-btn flat dense round @click="leftDrawerOpen = !leftDrawerOpen" aria-label="Menu">
          <q-icon name="menu" />
        </q-btn>

        <q-toolbar-title>Verbose Equals True</q-toolbar-title>
        <q-toggle
          color="black"
          v-model="darkMode"
        />
        <q-btn
          :ripple="false"
          color="white"
          text-color="primary"
          label="Login"
          no-caps
          @click="$store.commit('toggleLoginMenu')"
        />
        <login-modal />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" content-class="bg-grey-5">
      <q-list>
        <q-item-label header>Menu</q-item-label>

        <left-menu-link label="Home" to="/" icon="home" caption="Start Here" />
        <left-menu-link label="About" to="/about" icon="info" caption="About this site" />
      </q-list>
    </q-drawer>

    <q-page-container>
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>
    </q-page-container>
  </q-layout>
</template>

<script>
import { openURL } from "quasar";
import LeftMenuLink from "components/LeftMenuLink.vue";
import LoginModal from "components/LoginModal.vue";
export default {
  name: "MyLayout",
  components: { LeftMenuLink, LoginModal },
  data() {
    return {
      darkMode: false,
      leftDrawerOpen: this.$q.platform.is.desktop
    };
  },
  methods: {
    openURL
  }
};
</script>
<style>
.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.15s;
  transition-property: opacity;
  transition-timing-function: ease;
}

.fade-enter,
.fade-leave-active {
  opacity: 0;
}
</style>
