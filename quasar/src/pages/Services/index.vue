<template>
  <base-page>
    <page-sub-header>Services</page-sub-header>
    <div class="q-pa-md q-gutter-sm">
      <q-btn
        v-for="(s, i) in services"
        :key="i"
        :type="s.type"
        :target="s.target"
        :href="s.href"
        color="primary"
        :icon="s.icon"
        :label="s.name"
      />
    </div>
  </base-page>
</template>

<script>
import services from "./services.js";
export default {
  data() {
    return {
      services,
    };
  },
};
</script>

<style lang="scss" scoped></style>
