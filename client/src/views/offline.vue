<template>
  <v-container>
    <v-subheader>Offline mode</v-subheader>
    <control-screen :api="arduino" :online="false"></control-screen>
  </v-container>
</template>

<script>
// eslint-disable-next-line
import arduino from "../services/arduino";
import ControlScreen from '../components/control-screen.vue'


export default {
  data() {
    return {
      arduino: arduino
    };
  },
  components: {
    ControlScreen
  },
};
</script>