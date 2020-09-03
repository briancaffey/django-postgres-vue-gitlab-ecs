<template>
  <div class="form-wrapper">
    <q-file
      :dark="$store.getters.isDark"
      v-model="statementFile"
      label="Select Statement"
      accept=".csv"
    />
    <base-input
      label="Select Month"
      v-model="month"
      @focus="showCalendar = true"
    >
    </base-input>
    <base-date
      emit-immediately
      v-show="showCalendar"
      v-model="month"
      @input="setCal"
      :options="options"
      mask="YYYY-MM-DD"
      default-view="Years"
    >
    </base-date>
    <base-btn
      :disabled="
        !$store.getters['banking/upload/getFile'] ||
        !$store.getters['banking/upload/getDate']
      "
      @click.native="uploadFile"
      >Upload File</base-btn
    >
  </div>
</template>

<script>
export default {
  data() {
    return {
      showCalendar: false,
    };
  },
  methods: {
    uploadFile() {
      this.$store.dispatch("banking/upload/uploadFile", { vm: this });
    },
    setCal(value, reason) {
      this.$store.commit("banking/upload/setDate", value);
      if (reason === "month" || reason === "day") {
        this.showCalendar = false;
      }
    },
    options(date) {
      const parts = date.split("/");
      return parts[2] === "01";
    },
  },
  computed: {
    statementFile: {
      get() {
        return this.$store.getters["banking/upload/getFile"];
      },
      set(f) {
        return this.$store.commit("banking/upload/setFile", f);
      },
    },
    month: {
      get() {
        return this.$store.getters["banking/upload/getDate"];
      },
      set(v) {
        return this.$store.commit("banking/upload/setDate", v);
      },
    },
  },
};
</script>

<style scoped>
.form-wrapper {
  padding: 10px;
  display: grid;
  gap: 10px;
}
</style>
