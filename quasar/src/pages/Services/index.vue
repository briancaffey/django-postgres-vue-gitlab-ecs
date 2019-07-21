<template>
  <base-page>
    <h4>Services</h4>
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
    <h4>Documentation Links</h4>
    <div class="q-pa-md q-gutter-sm">
      <q-btn
        v-for="(s, i) in documentationLinks"
        :key="i"
        :type="s.type"
        :target="s.target"
        :href="s.href"
        color="primary"
        :icon="s.icon || null"
        :label="s.name"
      />
    </div>
    <h4>Helpful Links</h4>
    <div class="q-pa-md q-gutter-sm">
      <q-btn
        v-for="(s, i) in helpfulLinks"
        :key="i"
        :type="s.type"
        :target="s.target"
        :href="s.href"
        color="primary"
        :icon="s.icon || null"
        :label="s.name"
      />
    </div>
  </base-page>
</template>

<script>
import services from "./services.js";
import documentationLinks from "./documentation.js";
import helpfulLinks from "./helpfulLinks.js";
export default {
  data() {
    return {
      services,
      documentationLinks,
      helpfulLinks
    };
  }
};
</script>

<style lang="scss" scoped></style>
