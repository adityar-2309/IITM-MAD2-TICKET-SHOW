<template>
<div id="#app">
    <h1>Tickets</h1>
    <table class="table table-borderless">
        <tr>
            <th>Name</th>
            <th>Movie Name</th>
            <th>Theater Name</th>
            <th>Number of Tickets</th>
            <th>Ticket Price</th>
            <th>Date</th>
            <th>Time</th>
        </tr>
        <tr v-for="ticket in tickets">
            <td>{{ticket.username}}</td>
            <td>{{ticket.name}}</td>
            <td>{{ticket.theater_name}}</td>
            <td>{{ticket.nooftickets}}</td>
            <td>{{ticket.ticket_price}}</td>
            <td>{{ticket.date}}</td>
            <td>{{ticket.time}}</td>
        </tr>
    </table>

</div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Tickets',
    data() {
        return {
            tickets: []
        }
    },
    methods: {
        async gettickets() {
            let token = localStorage.getItem('token')
            const response = await axios.get("gettickets", {
                headers: {
                        Authorization: "Bearer " + token
                    }});
            if (response.data.message == "success") {
                console.log("getTickets successful")
                console.log(response)
                this.tickets = response.data.tickets
            } else {
                console.log(response)
                console.log("getTickets failed")
            }
        }
    },
    created() {
        this.gettickets()
    }
}
</script>

<style>

</style>