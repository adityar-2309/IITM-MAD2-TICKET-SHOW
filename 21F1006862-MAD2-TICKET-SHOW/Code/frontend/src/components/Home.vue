<template>
<div id="#app">
<h3>Home</h3>
<div v-if="$store.state.checkl">

<table class="table table-borderless">
    <tr>
        <th>Show name</th>
        <th>Show genre</th>
        <th>Show rating</th>
      
    </tr>
    <tr v-for="show in shows" :key="show.id">
        <td>{{ show.name }}</td>
        <td>{{ show.genre }}</td>
        <td>{{ show.rating }}</td>
        <td><router-link :to="{name: 'viewshow', params: {id: show.id}}">View Shows</router-link></td>

    </tr>
</table>

</div>
<div v-else>
    <h1>Not logged in</h1>
    <router-link to="/login">Login</router-link>
</div>
</div>  
</template>
<script>
import axios from 'axios';

export default{
    name: 'Home',
    data(){
        return{
            shows: []
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
            this.$router.push('/login')
        }
  },

        async getmovies() {
            let token = localStorage.getItem("token")
        const response = await axios.get("getmovies", {
                headers: {
                    Authorization: "Bearer " + token
                }})
        this.shows = response.data.movies
        console.log(response)
    }
    
    },
    mounted(){
        this.getmovies()
    },
    created(){
        this.checklogin()
    },
    
beforeCreate () {
  if (this.$store.state.checkl == false) {
    this.$router.push('/login')
}}

}


</script>

<style>

</style>