<template>
<div id="#app">
<h1>View Shows</h1>
<table class="table">
<tr>
<th>Movie</th>
<th>Theater</th>
<th>Ticket Price</th>
<th>Date</th>
<th>Time</th>
</tr>
<tr v-for="show in shows" :key="show.id">
<td>{{ show.name }}</td>
<td>{{ show.theater_name }}</td>
<td>{{ show.ticket_price }}</td>
<td>{{ show.date }}</td>
<td>{{ show.time }}</td>
<router-link :to="{name: 'bookshow', params: {id: show.id}}">Book Show</router-link>
</tr>
</table>
</div>
</template>
<script>
import axios from 'axios'
export default {
name: "ViewShow",
props: ["id"],
data() {
return {
shows: [],
movie_id: this.$route.params.id
}
},
methods: {
async getshow(){
let token =  localStorage.getItem("token")
const response = await axios.get("viewshow/" + this.movie_id, {
headers: {
Authorization: "Bearer " + token
}});
if (response.data.message == "success") {
this.shows = response.data.show
console.log("getshow successful")
console.log(response)
} else {
console.log(response)
console.log("getshow failed")
}
},
},
mounted(){
this.getshow()
}
}


</script>
<style></style>