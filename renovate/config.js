module.exports = {
  endpoint: 'https://gitlab.com/api/v4/',
  token: process.env.GITLAB_TOKEN,
  platform: 'gitlab',
  logFileLevel: 'warn',
  logLevel: 'debug',
  logFile: 'renovate.log',
  onboarding: true,
  onboardingConfig: {
    extends: ['config:base'],
    ignorePresets: [":prHourlyLimit2"],
    pip_requirements: {
      "fileMatch": ["requirements\/.+\.txt$"]
    },
  },
  hostRules: [
    {
      "domainName": "github.com",
      "encrypted": {
        "token": process.env.GITHUB_TOKEN
      }
    }
  ],
  repositories: ['verbose-equals-true/django-postgres-vue-gitlab-ecs'],
  gitAuthor: "Brian Caffey <briancaffey2010@gmail.com>",
  ignorePresets: [":prHourlyLimit2"],
  prHourlyLimit: 10
};
