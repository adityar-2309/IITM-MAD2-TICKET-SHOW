<template>
<div id="#app">
<div v-if="$store.state.checkl  && $store.state.checkadmin">
<h1>Admin Dashboard</h1>
<table class="table table-borderless">
    <tr>
        <th>Show name</th>
        <th>Show genre</th>
        <th>Show rating</th>
        <th>Show Date</th>
        <th>Show Time</th>
        <th>Show Theater</th>
    </tr>
    <tr v-for="show in shows" :key="show.id">
        <td>{{ show.name }}</td>
        <td>{{ show.genre }}</td>
        <td>{{ show.rating }}</td>
        <td>{{ show.date }}</td>
        <td>{{ show.time }}</td>
        <td>{{ show.theater_name }}</td>
        <td><router-link :to="{name: 'editshow', params: {id: show.id}}">Edit Show</router-link></td>
        <td><router-link :to="{name: 'deleteshow', params: {id: show.id}}">Delete Show</router-link></td>

    </tr>

</table>
<router-link to="/createshow">Create Show</router-link>
<router-link to="/viewtheater">View Theaters</router-link>
<router-link to="/createmovie">Create Movie</router-link>



</div>  
<div v-else>
    <h1>Not logged in</h1>
    <router-link to="/login">Login</router-link>
</div>
</div>
</template>

<script>
import axios from 'axios';

export default {
    name: "Admin",
    data(){
        return {
            shows: [],
        }
    },
    methods: {
        async checklogin(){
            let token = localStorage.getItem("token")
            const response = await axios.get("/checklogin", {
                headers: {
                    Authorization: "Bearer " + token
                }}
            )
        console.log(response.data)
            if (response.data.message == "success") {
                this.$store.commit("setcheckl", true)
                console.log(response, this.checkl)
        }
            else if(response.data.message == "failed") {
            this.$store.commit("setcheckl", false)
            console.log(response)
        }
        },
        async checkadmin(){
            let token = localStorage.getItem("token")
            const response = await axios.get("/checkadmin",{
                headers: {
                    Authorization: "Bearer " + token
                }}
            )
        console.log(response.data)
            if (response.data.message == "success") {
                this.$store.commit("setcheckadmin", true)
                console.log(response, this.checka)
        }
            else if(response.data.message == "failed") {
            this.$store.commit("setchecka", false)
            console.log(response)
            alert("You are not an admin redirecting to home page")
            this.$router.push('/')
        }
        },

        async getshows() {
        const response = await axios.get("/")
        this.shows = response.data.shows
        console.log(response)
    }
    },
    mounted(){
        this.getshows()
    },
    created(){
        this.checklogin()
        this.checkadmin()
    }
}

</script>

<style>

</style>