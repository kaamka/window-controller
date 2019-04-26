<template>
  <v-bottom-nav
    :active.sync="bottomNav"
    :value="true"
    fixed
    @update:active="changed"
  >
    <v-btn
      color="teal"
      flat
      value="trasa"
    >
      <span>Remote access</span>
      <v-icon>cloud</v-icon>
    </v-btn>

    <v-btn
      color="teal"
      flat
      value="wars"
    >
      <span>Local access</span>
      <v-icon>home</v-icon>
    </v-btn>

    <v-btn
      color="teal"
      flat
      value="media"
    >
      <span>Settings</span>
      <v-icon>settings</v-icon>
    </v-btn>
  </v-bottom-nav>
</template>

<script>
  export default {
    props: ['bottomNav'],
    data () {
      return {
      }
    },
    methods: {
      changed (val) {
        this.$emit('bottom-menu-change', val)
      }
    }
  }
</script>