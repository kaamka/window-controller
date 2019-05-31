<template>
  <v-container pb-5>
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

      <v-flex xs12 v-if="online">
        <v-subheader>Historic data</v-subheader>
        <v-data-table
          :headers="headers"
          :pagination.sync="pagination"
          :items="allData"
          class="elevation-1"
        >
          <template slot="headerCell" slot-scope="props">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <span v-on="on">{{ props.header.text }}</span>
              </template>
              <span>{{ props.header.text }}</span>
            </v-tooltip>
          </template>
          <template v-slot:items="props">
            <!-- <td class="text-xs-right">{{ props.item.id }}</td>
            <td class="text-xs-center">{{ props.item.device_id }}</td>-->
            <td class="text-xs-center">{{ new Date(props.item.time).toLocaleString() }}</td>
            <td class="text-xs-center">{{ props.item.hum }}</td>
            <td class="text-xs-center">{{ props.item.temp }}</td>
            <td class="text-xs-center">{{ props.item.gas }}</td>
            <td class="text-xs-center">{{ props.item.sound }}</td>
            <td class="text-xs-center">{{ props.item.open_status }}</td>
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
    <template v-if="charts">
      <v-flex xs12 v-for="(chart, i) in charts" :key="i">
        <v-subheader>{{ chart.name }}</v-subheader>
        <v-card>
          <v-card-text>
            <graph-line-timerange
              :height="200"
              :axis-min="0"
              :axis-max="chart.maxc"
              :axis-reverse="false"
              :axis-format="'HH:mm'"
              :axis-interval="1000 * 60 * 60 * 8"
              :labels="chart.labels"
              :values="chart.values"
            >
              <note :text="chart.name"></note>
              <guideline :tooltip-x="true" :tooltip-y="true"></guideline>
            </graph-line-timerange>
          </v-card-text>
        </v-card>
      </v-flex>
    </template>
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
import timeout from "../plugins/timeout";

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
      sbText: "",
      allData: [],
      headers: [
        // { text: "id", value: "id" },
        // { text: "device_id", value: "device_id" },
        { text: "Time", value: "time", align: "center" },
        { text: "Humidity", value: "hum", align: "center" },
        { text: "Temperature", value: "temp", align: "center" },
        { text: "Gas level", value: "gas", align: "center" },
        { text: "Sound Level", value: "sound", align: "center" },
        { text: "Status", value: "open_status", align: "center" }
      ],
      pagination: {
        descending: true,
        sortBy: "time"
      },
      charts: false
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
        let status = await timeout(20000, this.api.status());
        this.status = status.data;
      } catch (e) {
        // eslint-disable-next-line
        console.log(e);
        this.snackbar = true;
        this.sbText = "Connection problem (status), retrying. " + e.message; // e.config + Object.keys(e)
        setTimeout(this.refresh, 5000);
        return;
      }
      try {
        let data = await timeout(15000, this.api.data());
        this.data = data;
      } catch (e) {
        this.snackbar = true;
        this.sbText = "Connection problem (data), retrying. " + e.message;
        setTimeout(this.refresh, 5000);
        return;
      }

      this.allData = (await this.api.allData()).data;
      this.prepareCharts();
    },
    async open() {
      this.moveWindow(this.api.open, "open", this.open);
    },
    async close() {
      this.moveWindow(this.api.close, "closed", this.close);
    },
    async moveWindow(handler, type, caller) {
      this.dialog = true;
      let openPromise = timeout(7000, handler());

      openPromise.then(res => {
        let status = res.data;
        if (status == `was_${type}`) {
          this.snackbar = true;
          this.sbText = `Window was ${type}`;
        } else {
          this.status = type;
        }
        this.dialog = false;
      });

      // eslint-disable-next-line
      openPromise.catch(_error => {
        // eslint-disable-next-line
        console.log("Retrying opening");
        caller();
      });
    },
    prepareCharts() {
      let charts = [];
      let min = new Date(
        this.allData.reduce(function(prev, curr) {
          return prev.time < curr.time ? prev : curr;
        }).time
      );
      let max = new Date(
        this.allData.reduce(function(prev, curr) {
          return prev.time > curr.time ? prev : curr;
        }).time
      );
      for (let col of this.headers) {
        if (col.value == "open_status" || col.value == "time") continue;
        let vals = this.allData.map(el => [new Date(el.time), el[col.value]]);
        let maxc = this.allData.reduce(function(prev, curr) {
            return prev[col.value] > curr[col.value] ? prev : curr;
          })[col.value]

        charts.push({
          name: col.text,
          values: vals,
          labels: [min, max],
          maxc
        });
      }
      this.charts = charts;
    }
  }
};
</script>

<style scoped>
.material-icons {
  display: inline-flex;
}
</style>
