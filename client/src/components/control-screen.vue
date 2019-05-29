<template>
  <v-container>
    <v-layout wrap>
      <v-flex xs12>
        <v-subheader>Controls</v-subheader>
        <v-card>
          <v-card-text>
            <v-container fluid class="pa-0">
              <v-layout row wrap align-center>
                <v-flex xs6>
                  <div class="text-xs-center">
                    <div>
                      <v-btn @click="open" color="primary" fab large dark>
                        <v-icon>lock_open</v-icon>
                      </v-btn>
                    </div>
                  </div>
                </v-flex>
                <v-flex xs6>
                  <div class="text-xs-center">
                    <div>
                      <v-btn @click="close" color="error" fab large dark>
                        <v-icon>lock</v-icon>
                      </v-btn>
                    </div>
                  </div>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs12>
        <v-subheader>Window status</v-subheader>
        <v-card>
          <v-card-text>
            <p>Status: {{ status }}</p>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs12>
        <v-subheader>Current data</v-subheader>
        <v-card>
          <v-card-text>
            <p>Gas level: {{ data.gas }}</p>
            <p>Sound level: {{ data.sound }}</p>
            <p>Humidity: {{ data.humidity }}</p>
            <p>Temperature: {{ data.temp }}</p>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-dialog v-model="dialog" hide-overlay persistent width="300">
      <v-card color="primary" dark>
        <v-card-text>
          Please stand by
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbar" :multi-line="true" :bottom="true" :timeout="5000">
      {{ sbText }}
      <v-btn color="pink" flat @click="snackbar = false">Close</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
import timeout from "../plugins/timeout"

export default {
  data() {
    return {
      status: "unknown",
      data: {
        gas: null,
        sound: null,
        humidity: null,
        temp: null
      },
      dialog: false,
      snackbar: false,
      sbText: ""
    };
  },
  props: {
    online: {
      type: Boolean,
      default: false
    },
    api: Object
  },
  components: {},
  async mounted() {
    this.refresh();
  },
  methods: {
    async refresh() {
      try {
        let status = await timeout(20000, this.api.status())
        this.status = status.data;
      } catch (e) {

        this.snackbar = true
        this.sbText = 'Connection problem (status), retrying. ' + e.message // e.config + Object.keys(e)
        setTimeout(this.refresh, 5000);
        return

      }
      try {
        let data = await timeout(15000, this.api.data())
        this.data = data;
      } catch (e) {
        this.snackbar = true
        this.sbText = 'Connection problem (data), retrying. ' + e.message
        setTimeout(this.refresh, 5000);
        return
      }
    },
    async open() {
      this.moveWindow(this.api.open, 'open', this.open)
    },
    async close() {
      this.moveWindow(this.api.close, 'closed', this.close)
    },
    async moveWindow(handler, type, caller) {
      this.dialog = true;
      let openPromise = timeout(7000, handler())
      
      openPromise.then(res => {
        let status = res.data;
        if (status == `was_${type}`) {
          this.snackbar = true
          this.sbText = `Window was ${type}`
        } else {
          this.status = type
        }
        this.dialog = false
      });

      // eslint-disable-next-line
      openPromise.catch(_error => {
        // eslint-disable-next-line
        console.log('Retrying opening')
        caller()
      })
    }
  }
};
</script>

<style scoped>
.material-icons {
  display: inline-flex;
}
</style>
