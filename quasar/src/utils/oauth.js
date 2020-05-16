const url = process.env.API_URL;

const oauth = {
  github: {
    url: "https://github.com/login/oauth/authorize",
    params: {
      client_id: process.env.GITHUB_KEY,
      redirect_uri: `${url}/auth/github/callback`,
      login: "",
      scope: "user",
      state: "eworifjeovivoiej",
    },
  },
  "google-oauth2": {
    url: "https://accounts.google.com/o/oauth2/v2/auth",
    params: {
      client_id: process.env.GOOGLE_OAUTH2_KEY,
      response_type: "code",
      scope: "openid email",
      redirect_uri: `${url}/auth/google-oauth2/callback`,
      state: "eworifjeovivoiej", // TODO: change these
      nonce: "forewijf43oirjoifj",
      login_hint: "",
    },
  },
  facebook: {
    url: "https://www.facebook.com/v5.0/dialog/oauth",
    params: {
      client_id: process.env.FACEBOOK_KEY,
      redirect_uri: `${url}/auth/facebook/callback`,
      state: "eworifjeovivoiej", // TODO: change these
      scope: "email",
    },
  },
};

export default oauth;
