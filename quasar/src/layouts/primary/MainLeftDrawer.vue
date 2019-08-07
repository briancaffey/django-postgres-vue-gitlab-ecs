<template>
  <div>
    <q-drawer
      @hide="hideDrawer"
      v-model="leftDrawerOpen"
      content-class="bg-grey-5"
    >
      <q-list>
        <q-item-label header>Menu</q-item-label>

        <left-menu-link
          :label="$t('leftDrawer.home.main')"
          to="/"
          icon="home"
          :caption="$t('leftDrawer.home.sub')"
        />

        <left-menu-link
          :label="$t('leftDrawer.about.main')"
          to="/about"
          icon="info"
          :caption="$t('leftDrawer.about.sub')"
        />

        <left-menu-link
          :label="$t('leftDrawer.protected.main')"
          to="/protected"
          icon="lock"
          :caption="$t('leftDrawer.protected.sub')"
        />

        <left-menu-link
          :label="$t('leftDrawer.toDo.main')"
          to="/to-do"
          icon="check"
          :caption="$t('leftDrawer.toDo.sub')"
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
          icon="perm_identity"
          :label="$t('leftDrawer.examples.main')"
          :caption="$t('leftDrawer.tests.sub')"
        >
          <left-menu-link
            :label="$t('leftDrawer.examples.websockets.main')"
            to="/examples/websockets"
            icon="offline_bolt"
            :caption="$t('leftDrawer.examples.websockets.sub')"
          />
        </q-expansion-item>
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
        </q-expansion-item>
        <left-menu-link
          :label="$t('leftDrawer.environment.main')"
          to="/debug/environment-variables"
          icon="offline_bolt"
          :caption="$t('leftDrawer.environment.main')"
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
