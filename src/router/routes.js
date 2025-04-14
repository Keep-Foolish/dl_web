import HomePage from "../components/HomePage.vue";
import DetectLodging from "../components/DetectLodging.vue";
import ImageStitching from "../components/ImageStitching.vue";
import DetectHistory from "../components/DetectHistory.vue";

export const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
  }, {
    path: "/DetectLodging",
    name: "Detect",
    component: DetectLodging
  }, {
    path: "/ImageStitching",
    name: "Stitching",
    component: ImageStitching
  }, {
    path: "/DetectHistory",
    name: "History",
    component: DetectHistory
  }
]



