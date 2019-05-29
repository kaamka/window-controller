<template>
  <v-container>
    <v-subheader>Offline mode</v-subheader>
    <control-screen :api="arduino"></control-screen>
  </v-container>
</template>

<script>
// eslint-disable-next-line
import arduino from "../services/arduino";
import ControlScreen from '../components/control-screen.vue'


export default {
  components: {
    ControlScreen
  },
};
</script>