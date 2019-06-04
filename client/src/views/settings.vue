<template>
  <v-container fluid>
    <v-layout row wrap>
      <v-flex xs12>
        <v-subheader>Devices</v-subheader>
        <v-card>
          <v-card-text>
            <v-select
              :items="devices"
              v-model="select"
              item-text="name"
              item-value="id"
              label="Select device"
            ></v-select>
            <v-btn color="success" @click="saveDevice">Save</v-btn>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <v-layout row wrap>
      <v-flex xs12>
        <v-subheader>Cloud/server URL</v-subheader>
        <v-card>
          <v-card-text>
            <v-form ref="form">
              <v-text-field v-model="settings.cloudUrl" label="Cloud service URL" required></v-text-field>
              <v-btn color="success" @click="save">Save</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <v-snackbar v-model="snackbar">
      {{ snackbarText }}
      <v-btn color="pink" flat @click="snackbar = false">Close</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
/**
 * Settings currently use LocalStorage to persist information.
 * It's lean, but for a production, robust solution for state management,
 * we might want to implement vuex store with LocalStorage persitance.
 */
import cloud from "../services/cloud";

export default {
  data: () => ({
    settings: JSON.parse(localStorage.getItem("settings")) || {
      arduinoUrl: "http://192.168.5.18/arduino/digital",
      cloudUrl: "http://192.168.0.228:31535",
      arduinoID: 1
    },
    snackbar: false,
    snackbarText: "Settings saved",
    devices: [],
    select: null
  }),
  async mounted() {
    if (localStorage.getItem("settings"))
      this.settings = JSON.parse(localStorage.getItem("settings"));
    await this.loadData();
  },
  methods: {
    save() {
      localStorage.setItem("settings", JSON.stringify(this.settings));
      this.snackbar = true;
    },
    async loadData() {
      this.devices = await cloud.devices();
      this.select = this.devices[0]
    },
    saveDevice() {
      let selected = this.devices.filter(obj => obj.id === this.select)[0]
      this.settings.arduinoUrl = selected.ip_address
      this.settings.arduinoID = selected.id
      // eslint-disable-next-line
      console.log(this.settings)
      localStorage.setItem("settings", JSON.stringify(this.settings));
      this.snackbar = true;
    }
  }
};
</script>
