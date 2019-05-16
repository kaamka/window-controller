<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Smart Window </span>
        <span class="font-weight-light">Controller</span>
      </v-toolbar-title>
    </v-toolbar>

    <v-content>
      <router-view/>
      <bottom-nav></bottom-nav>
    </v-content>
  </v-app>
</template>

<script>
import BottomNav from './components/bottom-nav.vue'

export default {
  name: 'App',
  data () {
    return {
      //
    }
  },
  components: {
    BottomNav,
  }
}
</script>
