<template>
  <base-page>
    <h4>Services</h4>
    <div class="q-gutter-md">
      <service-link
        v-for="(s, i) in services"
        :key="i"
        :icon="s.icon"
        :name="s.name"
        :link="s.link"
        :type="s.type"
        :href="s.href"
      />
    </div>
  </base-page>
</template>

<script>
import services from "./services.js";
export default {
  data() {
    return {
      services
    };
  }
};
</script>

<style lang="scss" scoped>
</style>