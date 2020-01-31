<template>
  <base-page>
    <page-header>Transactions</page-header>
    <transactions-table />
  </base-page>
</template>

<script>
import TransactionsTable from "./TransactionsTable.vue";
export default {
  components: {
    TransactionsTable
  }
};
</script>

<style scoped></style>
