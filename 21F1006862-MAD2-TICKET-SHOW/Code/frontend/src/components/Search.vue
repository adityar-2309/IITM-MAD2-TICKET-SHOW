<template>
<div id="#app">
    <div class="container">
        <div class="row">
        <div class="col-md-12">
            <h1>Search</h1>
            <hr>
            <div class="form-group">
            <label for="search">Search</label>
            <form @submit.prevent="searchit">
            <input type="text" class="form-control" id="search" v-model="search">
            <button class="btn btn-primary">Search</button>
            </form>
            </div>
            <table class="table table-hover">
            <thead>
                <tr>
                <th>Movie Name</th>
                <th>Movie Rating</th>
                <th>Movie Genre</th>
                <th>Ticket Price</th>
                <th>Date</th>
                <th>Time</th>
                <th>Available Tickets</th>

                </tr>
            </thead>
            <tbody>
                <tr v-for="movie in movies">
                <td>{{movie.name}}</td>
                <td>{{movie.rating}}</td>
                <td>{{movie.genre}}</td>
                <td>{{movie.ticket_price}}</td>
                <td>{{movie.date}}</td>
                <td>{{movie.time}}</td>
                <td>{{movie.available_tickets}}</td>
                <td><router-link :to="{name: 'viewshow', params: {id: movie.show_id}}">View Shows</router-link></td>
</tr>
            </tbody>
            </table>
            </div>  
            </div>
            </div>

</div>
</template>
<script>
import axios from 'axios';
export default {
    name: 'Search',
    data() {
        return {
            search: '',
            movies: []
        };
    },
    methods: {
        async searchit() {
            let token = localStorage.getItem('token');
            const response = await axios.get('search/' + this.search
            );
            if (response.data.message == 'success') {
                this.movies = response.data.movies;
                console.log(response);
            } else {    
                console.log(response);
            }
        
        }
    },
}

</script>
<style>
</style>