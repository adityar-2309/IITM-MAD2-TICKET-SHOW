<template>
<div id="#app">
<h1>Admin Create Movie</h1>
<form @submit.prevent="createmovie">
<input class="form-control" type="text" placeholder="name" v-model="name">
<input class="form-control" type="text" placeholder="genre" v-model="genre">
<input class="form-control" type="text" placeholder="rating" v-model="rating">
<button class="btn btn primary " >Create Movie</button>
</form>
</div>
</template>
<script>
import axios from 'axios'
export default {
    name: "CreateMovie",
    data() {
        return {
            name: "",
            genre: "",
            rating: ""
        }
    },
    methods: {
        async createmovie(){
            let token =  localStorage.getItem("token")
            const response = await axios.post("createmovie", {
                name: this.name,
                genre: this.genre,
                rating: this.rating
        }, {    headers: {
                    Authorization: "Bearer " + token
                }});
        if (response.data.message == "movie created successfully") {
            console.log("createmovie successful")
            console.log(response)
            this.$router.push('/viewmovies');
        } else {
            console.log(response)
            console.log("createmovie failed")
        }
    }
    }
}


    
</script>
<style></style>
