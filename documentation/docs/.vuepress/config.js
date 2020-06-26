const path = require("path");

module.exports = {
  title: "Verbose Equals True",
  base: "/django-postgres-vue-gitlab-ecs/",
  port: 8080,
  configureWebpack: {
    resolve: {
      alias: {
        "@assets": path.resolve(__dirname, "../assets"),
      },
    },
  },
  dest: "../public",
  plugins: {
    "@vuepress/google-analytics": {
      ga: process.env.GOOGLE_ANALYTICS_CODE,
    },
  },
  serviceWorker: false,
  themeConfig: {
    lastUpdated: "Last Updated: ",
    sidebar: "auto",
    repo: process.env.CI_PROJECT_URL,
    docsBranch: "develop",
    repoLabel: "View on GitLab",
    docsDir: "documentation/docs",
    editLinks: true,
    editLinkText: "Edit this page on GitLab",
    nav: [
      { text: "Home", link: "/" },
      {
        text: "Start Here",
        items: [
          { text: "Overview", link: "/start/overview/" },
          { text: "Tools Used", link: "/start/tools/" },
        ],
      },
      {
        text: "Guide",
        items: [{ text: "Testing", link: "/guide/testing/" }],
      },
      {
        text: "DevOps",
        items: [{ text: "AWS CDK", link: "/devops/aws-cdk/" }],
      },
      {
        text: "Topics",
        items: [
          { text: "GraphQL", link: "/topics/graphql/" },
          { text: "Minikube", link: "/topics/minikube/" },
        ],
      },
    ],
  },
};
