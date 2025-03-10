<template>
  <div class="players">
    <h1>Players</h1>
    <!-- I want to structure the page so that there are 2 buttons at the top, 
     Underneath I want a table that displays all players. The table will be a reusable component which is passed the data from an api call -->
    <v-row justify="center">
      <v-col cols="auto">
        <!-- i want this button to pull left -->
        <v-btn class="mr-2" color="green" to="/add-player">Add Player</v-btn>
        <!-- i want this button to pull right -->
        <v-btn color="green" to="/delete-player">Delete Player</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <DisplayTable :players="players" />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import DisplayTable from "@/components/DisplayTable.vue";

export default {
  components: {
    DisplayTable,
  },
  data() {
    return {
      players: [
        {
          id: 1,
          name: "Bert mcGurt",
          dob: "22/04/1985",
          dateJoined: "01/01/2021",
        },
        {
          id: 2,
          name: "John Doe",
          dob: "22/04/1985",
          dateJoined: "01/01/2021",
        },
        {
          id: 3,
          name: "Jane Doe",
          dob: "22/04/1985",
          dateJoined: "01/01/2021",
        },
        {
          id: 4,
          name: "John Smith",
          dob: "22/04/1985",
          dateJoined: "01/01/2021",
        },
        {
          id: 5,
          name: "Jane Smith",
          dob: "22/04/1985",
          dateJoined: "01/01/2021",
        },
      ],
    };
  },
};
</script>

<!-- <style scoped>
</style> -->
