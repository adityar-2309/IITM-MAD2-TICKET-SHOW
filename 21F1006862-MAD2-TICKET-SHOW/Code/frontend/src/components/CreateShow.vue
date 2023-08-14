<template>
<div id="#app">
<h1>Admin Create Show</h1>
<form @submit.prevent="createshow">
<select class="form-control" v-model="movie_id">
<option v-for="movie in movies" :value="movie.id">{{movie.name}}</option>
</select>
<input class="form-control" type="number" placeholder="ticket price" v-model="ticket_price">
<input class="form-control" type="date" placeholder="date" v-model="date">
<input class="form-control" type="time" placeholder="time" v-model="time">
<label>Theater</label>
<select class="form-control" v-model="theaterid" >
<option v-for="theater in theaters" :value="theater.id">{{theater.name}}</option>
</select>
<button class="btn btn primary " >Create Show</button>
</form>
</div>
</template>
<script>
import axios from 'axios'
export default{
    name: "CreateShow",
    data() {
        return {
            theaterid: null,
            theaters: [],
            ticket_price: null,
            date: "",
            time: "",
            movies: [],
            movie_id: null
        }
    },
    methods: {
        async createshow() {
            let token =  localStorage.getItem("token")
            const response = await axios.post("createshow", {
                movie_id: this.movie_id,
                theaterid: this.theaterid,
                ticket_price: this.ticket_price,
                date: this.date,
                time: this.time
        }, {
                headers: {
                    Authorization: "Bearer " + token
                }});
        if (response.data.message == "show created successfully") {
            console.log("createshow successful")
            console.log(response)
            this.$router.push('/admin');
        } else {
            console.log(response)
            console.log("createshow failed")
        }
    },
    async getmovies(){
        let token =  localStorage.getItem("token")
        const response = await axios.get("getmovies", {
            headers: {
                Authorization: "Bearer " + token
            }});
    if (response.data.message == "success") {
        console.log("getmovies successful")
        console.log(response)
        this.movies = response.data.movies
    } else {
        console.log(response)
        console.log("getmovies failed")
    }
},
    async gettheaters(){
        let token =  localStorage.getItem("token")
        const response = await axios.get("gettheaters", {
            headers: {
                Authorization: "Bearer " + token
            }});
    if (response.data.message == "success") {
        console.log("gettheaters successful")
        console.log(response)
        this.theaters = response.data.theaters
    } else {
        console.log(response)
        console.log("gettheaters failed")

  
    }
},
},
mounted(){
    this.gettheaters(),
    this.getmovies()
},

beforeCreate () {
    if (this.$store.state.checkl == false) {
        this.$router.push('/login')
    }
    if (this.$store.state.checka == false) {
        this.$router.push('/')
    }
}
}
</script>
<style>

</style>