<template>
  <base-page>
    <page-header>Hacker News Clone</page-header>
    <div v-for="(link, i) in links" :key="i">
      {{ link.id }} {{ link.url }}

      <div v-for="(vote, j) in link.votes" :key="j">
        {{ vote.id }} {{ vote.user.email }}
      </div>
    </div>
  </base-page>
</template>

<script>
import gql from "graphql-tag";
export default {
  apollo: {
    links: gql`
      query {
        links {
          url
          id
          votes {
            id
            user {
              email
            }
          }
        }
      }
    `
  }
};
</script>

<style scoped></style>
