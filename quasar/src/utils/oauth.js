const protocol = process.env.NODE_ENV === "production" ? "https://" : "http://";
const url = process.env.SITE_URL;
const baseUrl = protocol + url;

const oauth = {
  github: {
    url: "https://github.com/oauth",
    params: {
      client_id: process.env.GITHUB_KEY,
      redirect_uri: `${baseUrl}/auth/github/callback`,
      login: "",
      scope: "user",
      state: "eworifjeovivoiej"
    }
  }
};

export default oauth;
