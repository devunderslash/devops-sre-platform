<template>
  <v-navigation-drawer expand-on-hover rail style="background-color: #f5f5f5">
    <v-list>
      <v-list-item
        prepend-icon="mdi-home"
        subtitle="attendance"
        title="ui"
        to="/"
        link
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item
        v-for="item in items"
        :key="item.value"
        :prepend-icon="item.icon"
        :title="item.title"
        :value="item.value"
        :to="item.to"
        link
      ></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "NavDrawer",
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
/* There was an issue with the prepend icons disapperaing when the navdrawer was collapsed */
/* Override box-sizing for the navigation drawer and its children */
.v-navigation-drawer,
.v-navigation-drawer *,
.v-navigation-drawer *::before,
.v-navigation-drawer *::after {
  box-sizing: revert !important; /* Revert to the default box-sizing */
}
</style>
