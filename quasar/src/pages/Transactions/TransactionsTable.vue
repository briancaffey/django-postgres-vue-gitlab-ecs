<template>
  <div>
    <q-table
      :loading="$store.getters['banking/transactions/getLoading']"
      :dark="$store.getters.isDark"
      :data="$store.getters['banking/transactions/getTransactions']"
      :columns="$store.getters['banking/transactions/getTableColumns']"
      :pagination.sync="pagination"
      row-key="id"
      :hide-bottom="true"
    >
    </q-table>
    <q-pagination
      :dark="$store.getters.isDark"
      v-model="current"
      :max-pages="10"
      :max="
        Math.ceil(
          $store.getters['banking/transactions/getCount'] /
            $store.getters['banking/transactions/getPaginationLimit']
        )
      "
    >
    </q-pagination>
  </div>
</template>

<script>
export default {
  created() {
    this.$store.dispatch("banking/transactions/getTransactions");
  },
  computed: {
    pagination: {
      get() {
        return this.$store.getters["banking/transactions/getPagination"];
      },
      set(v) {
        console.log(v);
        this.$store.commit("banking/transactions/setPagination", v);
      }
    },
    current: {
      get() {
        return this.$store.getters["banking/transactions/getCurrentPage"];
      },
      set(v) {
        this.$store.dispatch("banking/transactions/setCurrentPage", v);
      }
    }
  }
};
</script>

<style scoped></style>
