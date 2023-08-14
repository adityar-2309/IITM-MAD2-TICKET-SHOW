<template>
    <div id="#app">
    
    
        <h1>Book Show</h1>
            <form @submit.prevent="bookshow">
            <input class="form-control" type="text" placeholder="show" v-bind:value="$route.params.id" disabled>
            <input class="form-control" type="text" placeholder="show name" v-bind:value="showname" disabled>
            <input class="form-control" type="text" placeholder="genre" v-bind:value="genre" disabled>
            <input class="form-control" type="number" placeholder="rating" v-bind:value="rating" disabled>
            <input class="form-control" type="text" placeholder="name" v-model="name">
            <input class="form-control" type="number" placeholder="no of tickets" v-model="nooftickets">
            <input class="form-control" type="number" placeholder="available tickets" v-bind:value="available_tickets" disabled>
            <input class="form-control" type="date" placeholder="date" v-model="date" disabled>
            <input class="form-control" type="time" placeholder="time" v-model="time" disabled>
            <input class="form-control" type="number" placeholder="ticket price" v-bind:value="nooftickets*ticket_price" disabled>
            <button class="btn btn primary ">Book Show</button>
        </form>
</div>
</template>

<script>
import axios from 'axios'
export default {
    name: "BookShow",
    props : ['id'],
    data() {
        return {
            name: "",
            nooftickets: null,
            showid: this.$route.params.id,
            showname: "",
            genre: "",
            rating: null,
            ticket_price: null,
            date: "",
            time: "",
            available_tickets: null
        };
    },
    created() {
        console.log(this.id)
    },
    methods: {
        async bookshow() {
            let token =  localStorage.getItem("token")
            const response = await axios.post("bookshow/"+this.showid, {
                id: this.id,
                name : this.name,
                nooftickets: this.nooftickets
            }, {
                headers: {
                    Authorization: "Bearer " + token
                }}
);
            if ( response.data.message == "success") {
                console.log("bookshow successful")
                console.log(response)
                this.$router.push('/');
            } else if (response.data.message == "houseful") {
                console.log("show houseful")
                alert("show houseful")
                this.$router.push('/');
            } 
            else {
                console.log("bookshow failed")

        }
    },async getshow(){
            let token = localStorage.getItem("token")
            const response = await axios.post('getshow/'+this.showid,{
            id: this.showid },
            { headers: {
                        Authorization: "Bearer " + token
                    }});
            if (response.data.message=="success"){
                console.log(response)
                this.showname = response.data.show.name
                this.genre = response.data.show.genre
                this.rating = response.data.show.rating
                this.ticket_price = response.data.show.ticket_price
                this.available_tickets = response.data.show.available_tickets
                this.date = response.data.show.date
                this.time = response.data.show.time
            }
            else{
                console.log(response)
            }

        }
    },
    created(){
        this.getshow()
    }}

                
</script>

<style>

</style>
