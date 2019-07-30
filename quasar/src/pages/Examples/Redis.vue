<template>
  <base-page>
    <h4>Redis Test</h4>
    <p class="redis-debug">
      Value:
      <span id="val">{{ valueFromCache }}</span>
    </p>
    <q-input
      id="input"
      v-model.number="valueToSet"
      type="number"
      filled
      style="max-width: 200px"
      :disabled="true"
    />
    <q-btn id="set" @click="setCacheValue">Set Value to Cache</q-btn>
    <q-btn id="clear" @click="clearCacheValue">Delete Value from Cache</q-btn>
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
      apiCall.delete("/api/debug/redis").then(resp => {
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

<style lang="scss" scoped></style>
