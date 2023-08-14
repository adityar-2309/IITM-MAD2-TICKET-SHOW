<template>
<div id="#app">
    <h1>Theaters</h1>
    <table class="table table-borderless">
        <tr>
            <th>Name</th>
            <th>Place</th>
            <th>Capacity</th>
        </tr>
        <tr v-for="theater in theaters" :key="theater.id">
            <td>{{ theater.name }}</td>
            <td>{{ theater.place }}</td>
            <td>{{ theater.capacity }}</td>
            <td><router-link :to="{name: 'theater', params: {id: theater.id}}">View Shows</router-link>
            </td>
            </tr>   
    </table>

</div>
</template>
<script>
import axios from 'axios';
export default {
    name: 'Theaters',
    data() {
        return {
            theaters: []
        }
    },
    methods: {
    async gettheaters(){
        let token = localStorage.getItem("token")
        const response = await axios.get("gettheaters", {
        headers: {
        Authorization: "Bearer " + token
        }});
    if (response.data.message == "success") {
        console.log(response)
        console.log("gettheaters successful")
        this.theaters = response.data.theaters
        } else {
    console.log(response)
    console.log("gettheaters failed")
}
},
    },
    created() {
        this.gettheaters()
    }
}
</script>
<style>
</style>