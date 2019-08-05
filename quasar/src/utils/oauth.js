const url = process.env.API_URL;

const oauth = {
  github: {
    url: "https://github.com/login/oauth/authorize",
    params: {
      client_id: process.env.GITHUB_KEY,
      redirect_uri: `${url}/auth/github/callback`,
      login: "",
      scope: "user",
      state: "eworifjeovivoiej"
    }
  },
  google: {
    url: "https://accounts.google.com/o/oauth2/v2/auth",
    params: {
      client_id: process.env.GOOGLE_OAUTH2_KEY,
      response_type: "code",
      scope: "openid email",
      redirect_uri: `${url}/auth/google/callback`,
      state: "eworifjeovivoiej",
      nonce: "forewijf43oirjoifj",
      login_hint: ""
    }
  }
};

export default oauth;
