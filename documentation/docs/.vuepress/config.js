module.exports = {
  title: 'Verbose Equals True',
  base: '/docs/',
  port: 8080,
  dest: "public",
  plugins: {
    '@vuepress/google-analytics': {
      'ga': 'UA-131443776-1',
    },
  },
  serviceWorker: false,
  themeConfig: {
    lastUpdated: 'Last Updated: ',
    sidebar: 'auto',
    nav: [
      { text: 'Home', link: '/' },
      {
        text: 'Start Here',
        items: [
          { text: 'Overview', link: '/start/overview/' },
          { text: 'Tools Used', link: '/start/tools/' },
        ]
      },
      {
        text: 'Guide',
        items: [
          { text: 'Project Setup', link: '/guide/project-setup/' },
          { text: 'Backend API', link: '/guide/django-rest-framework/' },
          { text: 'Vue App', link: '/guide/vue-app/' },
          { text: 'Connecting Backend & Frontend', link: '/guide/connecting-backend-frontend/' },
          { text: 'NGINX', link: '/guide/nginx/' },
          { text: 'Celery & Redis', link: '/guide/celery-and-redis/' },
          { text: 'Production Environment', link: '/guide/production-environment/' },
          { text: 'Vue Authentication', link: '/guide/vue-authentication/' },
        ]
      },
      { text: 'Website', link: 'https://verbose-equals-true.tk' },
      { text: 'Source Code', link: 'https://gitlab.com/briancaffey/verbose-equals-true/tree/master/vuepress' },

    ]
  }
}