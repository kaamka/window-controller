<template>
  <v-bottom-nav
    :active.sync="bottomNav"
    :value="true"
    fixed
  >
    <v-btn
      color="teal"
      flat
      value="trasa"
      :to="{name: 'home'}"
    >
      <span>Remote access</span>
      <v-icon>cloud</v-icon>
    </v-btn>

    <v-btn
      color="teal"
      flat
      value="wars"
      :to="{name: 'offline'}"
    >
      <span>Local access</span>
      <v-icon>home</v-icon>
    </v-btn>

    <v-btn
      color="teal"
      flat
      value="media"
      :to="{name: 'settings'}"
    >
      <span>Settings</span>
      <v-icon>settings</v-icon>
    </v-btn>
  </v-bottom-nav>
</template>

<script>
  export default {
    props: [],
    data () {
      return {
        bottomNav: null
      }
    },
  }
</script>