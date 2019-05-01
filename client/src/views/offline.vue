<template>
  <v-container>
    <v-layout wrap>
      <v-flex xs12>
        <v-subheader>O aplikacji</v-subheader>
        <v-card>
          <v-card-title primary-title>Local</v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { arduino } from "../services/api";

export default {
  data: {
  },
  components: {},
  async mounted() {
    let status = await arduino().get("status");
    // eslint-disable-next-line
    console.log(status);
  },
  methods: {}
};
</script>
