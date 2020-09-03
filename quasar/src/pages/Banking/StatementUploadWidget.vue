<template>
  <div>
    <base-btn @click.native="show = !show">Upload a statement file</base-btn>
    <q-dialog v-model="show">
      <base-card>
        <statement-upload-form />
      </base-card>
    </q-dialog>
  </div>
</template>

<script>
import StatementUploadForm from "./StatementUploadForm.vue";
export default {
  components: {
    StatementUploadForm,
  },
  data() {
    return {
      show: false,
    };
  },
};
</script>

<style scoped></style>
