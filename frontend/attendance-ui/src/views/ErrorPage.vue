<!-- 404 error page -->
<template>
  <div class="error-page text-center">
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="display-1">404</h1>
          <h2>Page not found</h2>
          <br />
          <p class="error-page__paragraph center">
            The page you are looking for might have been removed, had its name
            changed, or is temporarily unavailable.
          </p>
          <br />
          <br />
          <v-btn color="green" to="/">Go back to home</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "NotFound",
};
</script>

<style scoped>
center {
  margin: 15vw;
}

h1 {
  color: var(--border);
  font-size: 16em;
}

h2 {
  color: var(--border);
  font-size: 4em;
}

.error-page__paragraph {
  font-size: 1.5em;
  color: var(--border);
}
</style>
