<template>
  <div>
    <q-dialog v-model="show">
      <base-card class="card">
        <q-card-section> Upload new link </q-card-section>
        <q-card-section>
          <base-input v-model="url" label="URL"></base-input>
        </q-card-section>
        <q-card-section>
          <base-input
            v-model="description"
            label="Description"
            type="textarea"
          ></base-input>
        </q-card-section>
        <base-btn @click.native="submit">Submit Link</base-btn>
      </base-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  methods: {
    submit() {
      this.$store.dispatch("hn/upload/submitLink", { vm: this });
    },
  },
  computed: {
    url: {
      get() {
        return this.$store.getters["hn/upload/getUrl"];
      },
      set(v) {
        this.$store.commit("hn/upload/setUrl", v);
      },
    },
    description: {
      get() {
        return this.$store.getters["hn/upload/getDescription"];
      },
      set(v) {
        this.$store.commit("hn/upload/setDescription", v);
      },
    },
    show: {
      get() {
        return this.$store.getters["hn/upload/getShowUploadForm"];
      },
      set() {
        this.$store.commit("hn/upload/toggleUploadForm");
      },
    },
  },
};
</script>

<style scoped>
.card {
  /* padding: 10px; */
}
</style>
