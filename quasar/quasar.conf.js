// Configuration for your app
// https://quasar.dev/quasar-cli/quasar-conf-js

module.exports = function(ctx) {
  return {
    // app boot file (/src/boot)
    // --> boot files are part of "main.js"
    boot: ["i18n", "axios", "components", "websockets"],
    css: ["app.styl"],
    extras: [
      // "ionicons-v4",
      // "mdi-v3",
      "fontawesome-v5",
      // "eva-icons",
      // "themify",
      // "roboto-font-latin-ext", // this or either "roboto-font", NEVER both!

      "roboto-font", // optional, you are not bound to it
      "material-icons" // optional, you are not bound to it
    ],

    framework: {
      // iconSet: "ionicons-v4",
      // lang: "de", // Quasar language

      // all: true, // --- includes everything; for dev only!

      components: [
        "QLayout",
        "QHeader",
        "QDrawer",
        "QPageContainer",
        "QPage",
        "QToolbar",
        "QToolbarTitle",
        "QBtn",
        "QIcon",
        "QList",
        "QItem",
        "QItemSection",
        "QItemLabel",
        "QDialog",
        "QCard",
        "QCardActions",
        "QTab",
        "QTabs",
        "QTabPanel",
        "QTabPanels",
        "QInput",
        "QToggle",
        "QExpansionItem",
        "QAjaxBar",
        "QChip",
        "QCheckbox",
        "QCarousel",
        "QCarouselSlide",
        "QSelect",
        "QForm",
        "QSpinnerGears",
        "QInnerLoading",
        "QTable",
        "QPagination",
        "QTh",
        "QTr",
        "QTd",
        "QDate",
        "QPopupProxy",
        "QFile"
      ],

      directives: ["Ripple", "ClosePopup"],

      // Quasar plugins
      plugins: ["Notify", "Cookies"]
    },

    // env: {
    // },
    supportIE: false,

    // TODO: add additional context for ci, production
    build: {
      env: ctx.dev
        ? {
            API_URL: JSON.stringify(
              `${process.env.HTTP_PROTOCOL}://${process.env.DOMAIN_NAME}`
            ),
            WS_PING_PONG: JSON.stringify(
              `${process.env.WS_PROTOCOL}://${process.env.DOMAIN_NAME}/ws/ping-pong/`
            ),
            GITHUB_KEY: JSON.stringify(process.env.GITHUB_KEY),
            GOOGLE_OAUTH2_KEY: JSON.stringify(process.env.GOOGLE_OAUTH2_KEY),
            FACEBOOK_KEY: JSON.stringify(process.env.FACEBOOK_KEY)
          }
        : {
            API_URL: JSON.stringify(
              `${process.env.HTTP_PROTOCOL}://${process.env.DOMAIN_NAME}`
            ),
            WS_PING_PONG: JSON.stringify(
              `${process.env.WS_PROTOCOL}://${process.env.DOMAIN_NAME}/ws/ping-pong/`
            ),
            GITHUB_KEY: JSON.stringify(process.env.GITHUB_KEY),
            GOOGLE_OAUTH2_KEY: JSON.stringify(process.env.GOOGLE_OAUTH2_KEY),
            FACEBOOK_KEY: JSON.stringify(process.env.FACEBOOK_KEY)
          },
      scopeHoisting: true,
      useNotifier: false,
      vueRouterMode: "history",
      // comments
      // vueCompiler: true,
      // gzip: true,
      // analyze: true,
      // extractCSS: false,
      extendWebpack(cfg) {
        cfg.module.rules.push({
          enforce: "pre",
          test: /\.(js|vue)$/,
          loader: "eslint-loader",
          exclude: /node_modules/,
          options: {
            formatter: require("eslint").CLIEngine.getFormatter("stylish")
          }
        });
      }
    },

    devServer: {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers":
          "Origin, X-Requested-With, Content-Type, Accept"
      },
      // https: true,
      port: 8080,
      open: true // opens browser window automatically
    },

    // animations: "all", // --- includes all animations
    animations: "all", //[],

    ssr: {
      pwa: false
    },

    pwa: {
      // workboxPluginMode: "InjectManifest",
      // workboxOptions: {}, // only for NON InjectManifest
      manifest: {
        // name: "Verbose Equals True",
        // short_name: "Verbose Equals True",
        // description: "Quasar frontend for Verbose Equals True",
        display: "standalone",
        orientation: "portrait",
        background_color: "#ffffff",
        theme_color: "#027be3",
        icons: [
          {
            src: "statics/icons/icon-128x128.png",
            sizes: "128x128",
            type: "image/png"
          },
          {
            src: "statics/icons/icon-192x192.png",
            sizes: "192x192",
            type: "image/png"
          },
          {
            src: "statics/icons/icon-256x256.png",
            sizes: "256x256",
            type: "image/png"
          },
          {
            src: "statics/icons/icon-384x384.png",
            sizes: "384x384",
            type: "image/png"
          },
          {
            src: "statics/icons/icon-512x512.png",
            sizes: "512x512",
            type: "image/png"
          }
        ]
      }
    },

    cordova: {
      // id: "org.cordova.quasar.app",
      // noIosLegacyBuildFlag: true, // uncomment only if you know what you are doing
    },

    electron: {
      // bundler: "builder", // or "packager"

      extendWebpack(cfg) {
        // do something with Electron main process Webpack cfg
        // chainWebpack also available besides this extendWebpack
      },

      packager: {
        // https://github.com/electron-userland/electron-packager/blob/master/docs/api.md#options
        // OS X / Mac App Store
        // appBundleId: "",
        // appCategoryType: "",
        // osxSign: "",
        // protocol: "myapp://path",
        // Windows only
        // win32metadata: { ... }
      },

      builder: {
        // https://www.electron.build/configuration/configuration
        // appId: "quasarfrontend"
      }
    }
  };
};
