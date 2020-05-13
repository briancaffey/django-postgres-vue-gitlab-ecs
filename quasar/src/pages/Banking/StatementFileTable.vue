<template>
  <div>
    <q-table
      :loading="$store.getters['banking/statements/getLoading']"
      :dark="$store.getters.isDark"
      :data="$store.getters['banking/statements/getFiles']"
      :columns="$store.getters['banking/statements/getTableColumns']"
      :pagination.sync="pagination"
      row-key="id"
      :hide-bottom="true"
    >
    </q-table>
    <q-pagination
      :dark="$store.getters.isDark"
      v-model="current"
      :max="
        $store.getters['banking/statements/getCount'] /
          $store.getters['banking/statements/getPaginationLimit']
      "
    >
    </q-pagination>
  </div>
</template>

<script>
export default {
  created() {
    this.$store.dispatch("banking/statements/getFiles");
  },
  computed: {
    pagination: {
      get() {
        return this.$store.getters["banking/statements/getPagination"];
      },
      set(v) {
        this.$store.commit("banking/statements/setPagination", v);
      }
    },
    current: {
      get() {
        return this.$store.getters["banking/statements/getCurrentPage"];
      },
      set(v) {
        this.$store.dispatch("banking/statements/setCurrentPage", v);
      }
    }
  }
};
</script>

<style lang="scss" scoped></style>
