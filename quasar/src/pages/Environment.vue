<template>
  <base-page>
    <page-header>Environment Variables</page-header>
    <q-table
      compact
      :hide-bottom="true"
      :dark="$store.getters.isDark"
      dense
      row-key="name"
      :data="env"
      :pagination.sync="pagination"
      :columns="columns"
    />
  </base-page>
</template>

<script>
export default {
  data() {
    return {
      pagination: {
        rowsPerPage: 0
      },
      columns: [
        {
          name: "key",
          align: "left",
          label: "Environment Variable",
          field: "key"
        },
        {
          name: "value",
          align: "left",
          label: "Value",
          field: "value"
        }
      ],
      env: Object.keys(process.env).map(x => {
        return {
          key: x,
          value: process.env[x]
        };
      })
    };
  }
};
</script>

<style lang="scss" scoped></style>
