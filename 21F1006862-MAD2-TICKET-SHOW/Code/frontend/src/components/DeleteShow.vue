<template>
<div id="#app">
    <h1> Delete Show</h1>
    <form @submit.prevent="deleteshow">
        <input class="form-control"  type="text" placeholder="name" v-model="name" disabled>
        <input class="form-control" type="text" placeholder="genre" v-model="genre" disabled>
        <input class="form-control" type="number" placeholder="rating" v-model="rating" disabled>
        <input class="form-control" type="text" placeholder="ticket price" v-model="ticket_price" disabled>
        <input class="form-control" type="date" placeholder="date" v-model="date" disabled>
        <input class="form-control" type="time" placeholder="time" v-model="time" disabled>
        <button class="btn btn primary " >Delete Show</button>

    </form>
</div>

</template>

<script>
import axios from 'axios'
export default { 
    name: "DeleteShow",
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
        
        async deleteshow(){
            let token = localStorage.getItem("token")
            const response = await axios.post('deleteshow/'+this.showid,{   
            },
{ headers: {Authorization: "Bearer " + token
                    }});
            if (response.data.message=="success"){
                console.log(response)
                this.$router.push('/admin');
            }
            else{
                console.log(response)
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