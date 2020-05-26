<template>
  <base-page>
    <page-header>Banking</page-header>
    <statement-upload-widget />
    <br />
    <router-link :to="`/transactions`">
      <base-btn>View transactions</base-btn>
    </router-link>
    <statement-file-table />
  </base-page>
</template>

<script>
import StatementFileTable from "./StatementFileTable.vue";
import StatementUploadWidget from "./StatementUploadWidget.vue";
export default {
  components: {
    StatementFileTable,
    StatementUploadWidget,
  },
};
</script>

<style lang="scss" scoped></style>
