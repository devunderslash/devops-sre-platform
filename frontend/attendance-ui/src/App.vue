<template>
  <v-app>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </nav>
    <v-main>
      <NavDrawer :items="navItems" />
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import NavDrawer from "@/components/NavDrawer.vue";

export default {
  components: {
    NavDrawer,
  },
  data() {
    return {
      navItems: [
        {
          icon: "mdi-account",
          title: "Player Details",
          value: "playerdetails",
          to: "/players",
        },
        {
          icon: "mdi-format-list-bulleted",
          title: "Attendance",
          value: "attendance",
          to: "/attendance",
        },
        {
          icon: "mdi-help-circle",
          title: "Help",
          value: "help",
          action: () => {
            alert("Help clicked");
          },
        },
      ],
    };
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
