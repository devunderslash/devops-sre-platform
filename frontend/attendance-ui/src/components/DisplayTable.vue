<template>
  <v-table height="300px" fixed-header>
    <thead>
      <tr>
        <th class="text-left">ID</th>
        <th class="text-left">Name</th>
        <th class="text-left">D.O.B.</th>
        <th class="text-left">Date Joined</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in players" :key="item.name">
        <td>{{ item.id }}</td>
        <td>{{ item.name }}</td>
        <td>{{ item.dob }}</td>
        <td>{{ item.dateJoined }}</td>
      </tr>
    </tbody>
  </v-table>
</template>

<script>
export default {
  props: {
    players: {
      type: Array,
      required: true,
    },
  },
};
</script>
