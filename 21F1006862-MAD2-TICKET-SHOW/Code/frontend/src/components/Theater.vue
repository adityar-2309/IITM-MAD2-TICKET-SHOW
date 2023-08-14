<template>
<div id="#app">
    <h4>Shows in {{ theater_name }}</h4>
    <table class="table table-borderless">
        <tr>
            <th>Show Name</th>
            <th>Genre</th>
            <th>Rating</th>
            <th>Ticket Price</th>
            <th>Available Tickets</th>
            <th>Date</th>
            <th>Time</th>
        </tr>
        <tr v-for="show in shows" :key="show.id">
            <td>{{ show.name }}</td>
            <td>{{ show.genre }}</td>
            <td>{{ show.rating }}</td>
            <td>{{ show.ticket_price }}</td>
            <td>{{ show.available_tickets }}</td>
            <td>{{ show.date }}</td>
            <td>{{ show.time }}</td>
            <td><router-link :to="{name: 'bookshow', params: {id: show.id}}">Book Show</router-link></td>
            </tr>
    </table>
</div>
</template>
<script>
import axios from 'axios';
export default{
    name: "Theater",
    props: ['id'],
    data(){
        return{
            shows: [],
            id: this.$route.params.id,
            theater_name: ""
        }
    },
    methods: {
        async getshows(){
            const response = await axios.get("gettheatershows/"+this.id)
            if (response.data.message == "success") {
                console.log(response)
                console.log("getshows successful")
                this.shows = response.data.shows
                this.theater_name = response.data.theater_name
            } else {
                console.log(response)
                console.log("getshows failed")
            }
        }
    },
    created() {
        this.getshows()
    }
}
</script>
<style>
</style>