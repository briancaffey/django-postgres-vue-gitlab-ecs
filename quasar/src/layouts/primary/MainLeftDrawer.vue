<template>
  <q-drawer
    @hide="hideDrawer"
    @show="showDrawer"
    v-model="leftDrawerOpen"
    content-class="bg-grey-5"
  >
    <q-list>
      <q-item-label header>Main Menu</q-item-label>

      <left-menu-link
        :label="$t('leftDrawer.home.main')"
        to="/"
        icon="home"
        :caption="$t('leftDrawer.home.sub')"
      />
      <left-menu-link
        :label="$t('Banking')"
        to="/banking"
        icon="money"
        :caption="$t('Banking info')"
      />
      <left-menu-link
        :label="$t('HN Clone')"
        to="/hn-clone"
        icon="info"
        :caption="$t('HN Clone Using GraphQL')"
      />

      <left-menu-link
        :label="$t('leftDrawer.about.main')"
        to="/about"
        icon="info"
        :caption="$t('leftDrawer.about.sub')"
      />

      <left-menu-link
        v-if="$store.getters.isAuthenticated"
        :label="$t('leftDrawer.services.main')"
        to="/services"
        icon="insert_chart_outlined"
        :caption="$t('leftDrawer.services.sub')"
      />

      <q-expansion-item
        :content-inset-level="0.5"
        v-if="$store.getters.isAuthenticated"
        expand-separator
        icon="check_circle"
        :label="$t('leftDrawer.tests.main')"
        :caption="$t('leftDrawer.tests.main')"
      >
        <left-menu-link
          :label="$t('leftDrawer.tests.redis.main')"
          to="/examples/redis"
          icon="offline_bolt"
          :caption="$t('leftDrawer.tests.redis.sub')"
        />
        <left-menu-link
          :label="$t('leftDrawer.examples.websockets.main')"
          to="/examples/websockets"
          icon="offline_bolt"
          :caption="$t('leftDrawer.examples.websockets.sub')"
        />
        <left-menu-link
          :label="$t('leftDrawer.environment.main')"
          to="/debug/environment-variables"
          icon="offline_bolt"
          :caption="$t('leftDrawer.environment.sub')"
        />
        <left-menu-link
          :label="$t('leftDrawer.celery.main')"
          to="/examples/celery"
          icon="local_florist"
          :caption="$t('leftDrawer.celery.sub')"
        />
      </q-expansion-item>
    </q-list>
  </q-drawer>
</template>

<script>
export default {
  computed: {
    leftDrawerOpen: {
      get() {
        return this.$store.getters.leftDrawerOpen;
      },
      set() {},
    },
  },
  methods: {
    showDrawer() {
      this.$store.commit("toggleLeftDrawer", {
        leftDrawerOpen: true,
      });
    },
    hideDrawer() {
      this.$store.commit("toggleLeftDrawer", {
        leftDrawerOpen: false,
      });
    },
    toggleLeftDrawer() {
      this.$store.commit("toggleLeftDrawer");
    },
  },
};
</script>

<style lang="scss" scoped></style>
