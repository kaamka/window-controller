<template>
  <v-container fluid>
    <v-layout row wrap>
      <v-flex xs12>
        <v-subheader>Server and device URLs</v-subheader>
        <v-card>
          <v-card-text>
            <v-form
              ref="form"
            >
              <v-text-field
                v-model="settings.arduinoUrl"
                label="Arduino URL"
                required
              ></v-text-field>
              <v-text-field
                v-model="settings.cloudUrl"
                label="Cloud service URL"
                required
              ></v-text-field>
              <v-btn
                color="success"
                @click="save"
              >
                Save
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <v-snackbar
      v-model="snackbar"
    >
      {{ snackbarText }}
      <v-btn
        color="pink"
        flat
        @click="snackbar = false"
      >
        Close
      </v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
/**
 * Settings currently use LocalStorage to persist information.
 * It's lean, but for a production, robust solution for state management,
 * we might want to implement vuex store with LocalStorage persitance.
 */

export default {
  data: () => ({
    settings: JSON.parse(localStorage.getItem('settings')) || {
      arduinoUrl: 'http://192.168.5.18',
      cloudUrl: 'http://192.168.0.228:31535'
    },
    snackbar: false,
    snackbarText: 'Settings saved'
  }),
  methods: {
    mounted () {
      if (localStorage.getItem('settings')) this.settings = JSON.parse(localStorage.getItem('settings'));
    },
    save () {
      localStorage.setItem('settings', JSON.stringify(this.settings));
      this.snackbar = true
    }
  }
}
</script>
