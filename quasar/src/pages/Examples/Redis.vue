<template>
  <base-page>
    <page-header>Redis Test</page-header>
    <page-text class="redis-debug">
      Value:
      <span id="val">{{ valueFromCache }}</span>
    </page-text>
    <div class="redis">
      <q-input
        :dark="$store.getters.isDark"
        id="input"
        v-model.number="valueToSet"
        type="number"
        filled
        :disabled="true"
      />
      <base-btn id="set" @click.native="setCacheValue"
        >Set Value to Cache</base-btn
      >
      <base-btn id="clear" @click.native="clearCacheValue"
        >Delete Value from Cache</base-btn
      >
    </div>
  </base-page>
</template>

<script>
import apiCall from "../../utils/api.js";
export default {
  data() {
    return {
      valueToSet: null,
      valueFromCache: null
    };
  },
  created() {
    this.getCachedValue();
    if (this.valueFromCache) {
      console.log("here.");
      this.valueToSet = this.valueFromCache;
    }
  },
  methods: {
    clearCacheValue() {
      apiCall.delete("/api/debug/redis/").then(resp => {
        console.log(resp);
        console.log("getting here..");
        this.valueFromCache = null;
      });
    },
    getCachedValue() {
      apiCall.get("/api/debug/redis/").then(resp => {
        this.valueFromCache = resp.data["count"];
      });
    },
    setCacheValue() {
      if (this.valueToSet) {
        apiCall
          .post("/api/debug/redis/", { count: this.valueToSet })
          .then(resp => {
            this.valueFromCache = resp.data.count;
          });
      }
    }
  }
};
</script>

<style scoped>
.redis {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 10px;
}
</style>
