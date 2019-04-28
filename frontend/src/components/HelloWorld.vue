<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>This site demonstrates how to use JWT authentication with websockets.</p>
    <p>The backend uses Django and Django Channels.</p>
    <p>The frontend uses <a href="https://github.com/nathantsoi/vue-native-websocket">vue-native-websocket</a>.</p>
    <p>Source code for this site can be found in my <a href="https://gitlab.com/briancaffey/briancaffey.com">GitLab repo</a>.</p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
