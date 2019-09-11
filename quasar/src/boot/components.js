import BasePage from "components/ui/BasePage.vue";
import DarkMode from "components/ui/DarkMode.vue";
import LeftMenuLink from "components/LeftMenuLink.vue";
import MainHeader from "layouts/primary/MainHeader.vue";
import PageHeader from "components/ui/PageHeader.vue";
import PageSubHeader from "components/ui/PageSubHeader.vue";
import PageText from "components/ui/PageText.vue";
import BaseBtn from "components/ui/BaseBtn.vue";
import MainLeftDrawer from "layouts/primary/MainLeftDrawer.vue";
import MainCarousel from "components/MainCarousel.vue";
import { Emoji } from "emoji-mart-vue";

// leave the export, even if you don't use it
export default async ({ Vue }) => {
  Vue.component("Emoji", Emoji);
  Vue.component("BasePage", BasePage);
  Vue.component("DarkMode", DarkMode);
  Vue.component("LeftMenuLink", LeftMenuLink);
  Vue.component("MainHeader", MainHeader);
  Vue.component("PageHeader", PageHeader);
  Vue.component("PageSubHeader", PageSubHeader);
  Vue.component("PageText", PageText);
  Vue.component("BaseBtn", BaseBtn);
  Vue.component("MainLeftDrawer", MainLeftDrawer);
  Vue.component("MainCarousel", MainCarousel);
};
