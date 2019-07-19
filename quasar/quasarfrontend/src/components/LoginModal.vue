<template>
  <div>
    <q-dialog @hide="hideLoginMenu" v-model="visible">
      <q-card style=" max-width: 95%; min-width: 320px;">
        <q-card-section>
          <div class="text-h6">Login</div>
        </q-card-section>
        <q-form @submit="login">
          <q-card-section>
            <q-input v-model="username" type="text" label="Email" autofocus />
            <q-input type="password" v-model="password" label="Password" />
          </q-card-section>

          <q-card-actions align="right" class="text-primary">
            <q-btn tabindex="-1" flat label="Cancel" v-close-popup />
            <q-btn flat label="Login" type="submit" v-close-popup />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: ""
    };
  },
  computed: {
    visible: {
      get() {
        return this.$store.getters.loginModalVisible;
      },
      set() {}
    }
  },
  methods: {
    hideLoginMenu() {
      this.$store.commit("toggleLoginMenu");
    },
    login() {
      this.username = "";
      this.password = "";
    }
  }
};
</script>

<style lang="scss" scoped>
</style>