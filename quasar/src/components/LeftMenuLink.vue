<template>
  <div>
    <q-item clickable tag="a" :to="to" exact>
      <q-item-section avatar>
        <q-icon :name="icon" />
      </q-item-section>
      <q-item-section>
        <q-item-label>{{ label }}</q-item-label>
        <q-item-label caption>{{ caption }}</q-item-label>
      </q-item-section>
    </q-item>
  </div>
</template>

<script>
export default {
  props: ["label", "to", "icon", "caption"]
};
</script>

<style lang="scss" scoped></style>
