<template>
  <base-page>
    <h4>To-Do's</h4>
    <q-list bordered padding>
      <q-item>
        <q-item-section>
          <q-checkbox v-for="(t, i) in todos" v-model="t.complete" :key="i">
            {{ t.title }}
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
