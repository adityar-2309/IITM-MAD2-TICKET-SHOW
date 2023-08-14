<template>
<div id="#app">
<h1>Admin Edit Movies</h1>
<form @submit.prevent="editmovie">
<input class="form-control" type="text" placeholder="name" v-model="name">
<input class="form-control" type="text" placeholder="genre" v-model="genre">
<input class="form-control" type="text" placeholder="rating" v-model="rating">
<button class="btn btn primary " >Edit Movie</button>
</form>
</div>
</template>
<script>
import axios from 'axios'
export default {
name: "EditMovie",
props: ["id"],
data() {
return {
    movies_id: this.$route.params.id,
name: "",
genre: "",
rating: ""
}
},
methods: {
async editmovie(){
let token =  localStorage.getItem("token")
const response = await axios.post("editmovie/" + this.movies_id, {
name: this.name,
genre: this.genre,
rating: this.rating
}, {
headers: {
Authorization: "Bearer " + token
}});
if (response.data.message == "success") {
console.log("editmovie successful")
console.log(response)
this.$router.push('/admin');
} else {
console.log(response)
console.log("editmovie failed")
}
},
async getmovie(){
let token =  localStorage.getItem("token")
const response = await axios.get("getmovie/" + this.movies_id, {
headers: {
Authorization: "Bearer " + token
}});
if (response.data.message == "success") {
this.name = response.data.movie.name
this.genre = response.data.movie.genre
this.rating = response.data.movie.rating
console.log("getmovie successful")
console.log(response)
} else {
console.log(response)
console.log("getmovie failed")
}
}
},
mounted(){
this.getmovie()
}
}


</script>
<style></style>
