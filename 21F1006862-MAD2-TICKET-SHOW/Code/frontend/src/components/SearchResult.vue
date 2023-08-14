<template>
    <h4>Search Results</h4>
    <table>
        <tr>
            <th>Movie Name</th>
            <th>Movie Genre</th>
            <th>Movie Rating</th>
            <th> Ticket Price</th>
            <th>Available Seats</th>
            <th>Theater Name</th>
            <th>Date</th>
            <th>Time</th>
        
        </tr>
        <tr v-for="show in searchresult">
            <td>{{show.movie_name}}</td>
            <td>{{show.movie_genre}}</td>
            <td>{{show.movie_rating}}</td>
            <td>{{show.ticket_price}}</td>
            <td>{{show.available_seats}}</td>
            <td>{{show.theater_name}}</td>
            <td>{{show.date}}</td>
            <td>{{show.time}}</td>
        </tr>
    </table>
<table>

</table>
</template>
<script>
import axios from 'axios';
export default{
    name:"SearchResult",
    props:['search'],
    data(){
        return{
            search: $route.params.search,
            searchresult:[]
        }
    },
    methods:{
        async search(){
            let token = localStorage.getItem("token");
            const response = await axios.get('search/'+this.search);
            if (response.data.status == "success") {
                this.searchresult = response.data.showlist
            }
        }
    },
    created(){
        this.search();
    }
}

</script>
<style>
</style>