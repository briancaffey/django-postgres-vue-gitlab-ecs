<template>
  <base-page>
    <page-header>To-Do's</page-header>
    <q-list bordered padding :dark="$store.getters.isDark">
      <q-item>
        <q-item-section>
          <q-checkbox
            :dark="$store.getters.isDark"
            v-for="(t, i) in todos"
            v-model="t.complete"
            :key="i"
          >
            <span
              :style="`color: ${$store.getters.isDark ? 'white' : 'black'}`"
            >
              {{ t.title }}</span
            >
          </q-checkbox>
        </q-item-section>
      </q-item>
    </q-list>
  </base-page>
</template>

<script>
import todos from "./todos.js";
export default {
  created() {
    this.toDoItems = todos.map(x => {
      x.complete;
    });
  },
  data() {
    return {
      darkMode: false,
      todos
    };
  }
};
</script>

<style lang="scss" scoped></style>
