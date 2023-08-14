<template>
    <div id="#app">
    <h1>Admin Edit Show</h1>
    <form @submit.prevent="editshow">
    <input class="form-control" type="text" placeholder="name" v-model="name">
    <input class="form-control" type="text" placeholder="genre" v-model="genre">
    <input  class="form-control" type="number" placeholder="rating" v-model="rating">
    <input class="form-control" type="number" placeholder="ticket price" v-model="ticket_price">
    <input class="form-control" type="date" placeholder="date" v-model="date">
    <input class="form-control" type="time" placeholder="time" v-model="time">
    <button class="btn btn primary " >Edit Show</button>
    </form>
    </div>
    </template>
    <script>
    import axios from 'axios'
    export default{
        name: "EditShow",
        props : ['id'],
        data() {
            return {
                showid: this.$route.params.id,
                name: "",
                genre: "",
                rating: null,
                ticket_price: null,
                date: "",
                time: ""
            }
        },
        methods: {
            async editshow() {
                let token =  localStorage.getItem("token")
                const response = await axios.post("editshow/"+this.showid, {
                    name: this.name,
                    genre: this.genre,
                    rating: this.rating,
                    ticket_price: this.ticket_price,
                    date: this.date,
                    time: this.time
            }, {
                    headers: {
                        Authorization: "Bearer " + token
                    }});
            if (response.data.message == "success") {
                console.log("editshow successful")
                console.log(response)
                this.$router.push('/admin');
            } else {
                console.log(response)
                console.log("editshow failed")
            }
        },
        async getshow(){
            let token = localStorage.getItem("token")
            const response = await axios.post('getshow/'+this.showid,{
            id: this.showid },
            { headers: {
                        Authorization: "Bearer " + token
                    }});
            if (response.data.message=="success"){
                console.log("response")
                this.name = response.data.show.name
                this.genre = response.data.show.genre
                this.rating = response.data.show.rating
                this.ticket_price = response.data.show.ticket_price
                this.date = response.data.show.date
                this.time = response.data.show.time
            }
            else{
                console.log("response")
            }

        }
    },
    created(){
        this.getshow()
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