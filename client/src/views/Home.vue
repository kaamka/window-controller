<template>
  <v-container>
    <v-subheader>Online mode</v-subheader>
    <control-screen :api="cloud" :online="true"></control-screen>
  </v-container>
</template>

<script>
// eslint-disable-next-line
import cloud from "../services/cloud";
import ControlScreen from '../components/control-screen.vue'


export default {
  data() {
    return {
      cloud: cloud
    };
  },
  components: {
    ControlScreen
  },
};
</script>