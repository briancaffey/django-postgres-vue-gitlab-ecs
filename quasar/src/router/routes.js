// import store from "../store";
// import router from "../router";

// for pages that should not be available to logged in users,
// such as "Recover password" or a dedicated "Login" page

// const ifNotAuthenticated = (to, from, next) => {
//   if (!store.getters.isAuthenticated) {
//     next();
//     return;
//   }
//   next("/");
// };

// const ifAuthenticated = (to, from, next) => {
//   if (store.getters.isAuthenticated) {
//     next();
//     return;
//   }

//   store.commit("setNextLink", { nextLink: to.fullPath });
//   store.commit("toggleLoginMenu");
//   router.push("/");
//   return;
// };

const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "auth/:provider/callback",
        component: () => import("pages/Auth/Callback.vue"),
      },
      {
        path: "",
        component: () => import("pages/Index.vue"),
      },
      { path: "login", component: () => import("pages/Auth/Login.vue") },
      { path: "login-gql", component: () => import("pages/Auth/LoginGQL.vue") },
      { path: "signup", component: () => import("pages/Auth/SignUp.vue") },
      {
        path: "about",
        component: () => import("pages/About.vue"),
      },
      {
        path: "banking",
        component: () => import("pages/Banking/index.vue"),
      },
      {
        path: "hn-clone",
        component: () => import("pages/HackerNewsClone/index.vue"),
      },
      {
        path: "transactions",
        component: () => import("pages/Transactions/index.vue"),
      },
      {
        path: "services",
        component: () => import("pages/Services/index.vue"),
      },
      {
        path: "debug/environment-variables",
        component: () => import("pages/Environment.vue"),
      },
      {
        path: "examples/",
        // beforeEnter: ifAuthenticated,
        component: () => import("pages/Examples/index.vue"),
        children: [
          {
            path: "websockets",
            // beforeEnter: ifAuthenticated,
            component: () => import("pages/Examples/Websockets.vue"),
          },
          {
            path: "celery",
            // beforeEnter: ifAuthenticated,
            component: () => import("pages/Celery/index.vue"),
          },
          {
            path: "redis",
            // beforeEnter: ifAuthenticated,
            component: () => import("pages/Examples/Redis.vue"),
          },
        ],
      },
    ],
  },
];

// Always leave this as last one
if (process.env.MODE !== "ssr") {
  routes.push({
    path: "*",
    component: () => import("pages/Error404.vue"),
  });
}

export default routes;
