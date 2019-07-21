<template>
  <div>
    <q-drawer
      @hide="hideDrawer"
      v-model="leftDrawerOpen"
      content-class="bg-grey-5"
    >
      <q-list>
        <q-item-label header>Menu</q-item-label>

        <left-menu-link label="Home" to="/" icon="home" caption="Start Here" />

        <left-menu-link
          label="About"
          to="/about"
          icon="info"
          caption="About this site"
        />

        <left-menu-link
          label="Protected"
          to="/protected"
          icon="lock"
          caption="This page is private"
        />

        <left-menu-link
          label="To-Do"
          to="/to-do"
          icon="check"
          caption="Site To-Do List"
        />

        <left-menu-link
          v-if="$store.getters.isAuthenticated"
          label="Services"
          to="/services"
          icon="insert_chart_outlined"
          caption="Monitoring, admin, metadata"
        />
      </q-list>
    </q-drawer>
  </div>
</template>

<script>
export default {
  computed: {
    leftDrawerOpen: {
      get() {
        return this.$store.getters.leftDrawerOpen;
      },
      set() {}
    }
  },
  methods: {
    hideDrawer() {
      this.$store.commit("toggleLeftDrawer", {
        leftDrawerOpen: false
      });
    },
    toggleLeftDrawer() {
      this.$store.commit("toggleLeftDrawer");
    }
  }
};
</script>

<style lang="scss" scoped></style>
