<template>
<div id="#app">
<h1>Admin View Movies</h1>
<table class="table">
<tr>
<th>Movie Name</th>
<th>Movie Genre</th>
<th>Movie Rating</th>
</tr>
<tr v-for="movie in movies" :key="movie.id">
<td>{{ movie.name }}</td>
<td>{{ movie.genre }}</td>
<td>{{ movie.rating }}</td>
<td><router-link :to="{name: 'editmovie', params: {id: movie.id}}">Edit Movie</router-link></td>
<td><router-link :to="{name: 'deletemovie', params: {id: movie.id}}">Delete Movie</router-link></td>
</tr>
</table>
<router-link to="/createmovie">Create Movie</router-link>
</div>
</template>
<script>
import axios from 'axios'
export default{
    name: "ViewMovies",
    data() {
        return {
            movies: []
        }
    },
    methods: {
        async getmovies(){
            let token =  localStorage.getItem("token")
            const response = await axios.get('getmovies')
            if ( response.data.message == "success"){
                this.movies = response.data.movies
                console.log(response)
            } else {
                console.log(response)
            }
        }
    },
    mounted(){
        this.getmovies()
    }
}

</script>
<style></style>