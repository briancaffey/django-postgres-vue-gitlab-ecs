<template>
  <base-page>
    <page-header>Celery Examples</page-header>
    <div class="celery">
      <q-input
        :dark="$store.getters.isDark"
        id="input"
        v-model.number="sleepSeconds"
        type="number"
        filled
        :disabled="true"
      />
      <base-btn id="set" @click.native="submitTask">Submit Sleep Task</base-btn>
    </div>
  </base-page>
</template>

<script>
export default {
  data() {
    return {
      sleepSeconds: 60,
    };
  },
  methods: {
    submitTask() {
      this.$axios
        .post("/api/celery/sleep-task/", {
          seconds: this.sleepSeconds,
        })
        .then((resp) => {
          this.$q.notify({
            title: "Task received.",
            message: resp.data["message"],
          });
        });
    },
  },
};
</script>

<style scoped>
.celery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 10px;
}
</style>
