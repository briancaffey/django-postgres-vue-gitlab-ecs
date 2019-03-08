<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>This is a static site that is served with a CloudFront distribution in front of an S3 bucket.</p>
    <p>The site is updated through a <a href="https://gitlab.com/briancaffey/briancaffey.com">GitLab CI/CD pipeline</a>.</p>
    <p>Commit ref: {{ commit }}</p>
    <p>Using cache invalidation</p>
    <a :href="ciJobUrl">View CI Job</a>
    <p>Now the site now has a Django backend that deploys to ECS via CloudFormation templates.</p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data(){
    return {
      commit: process.env.VUE_APP_CI_COMMIT_SHORT_SHA,
      ciJobUrl: process.env.VUE_APP_CI_JOB_URL
    }
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
