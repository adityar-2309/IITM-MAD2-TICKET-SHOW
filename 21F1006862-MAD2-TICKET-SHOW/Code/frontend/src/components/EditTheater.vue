<template>
    <div id="#app">
    <h1>Admin Edit Theater</h1>
    <form @submit.prevent="edittheater">
    <input class="form-control" type="text" placeholder="name" v-model="name">
    <input class="form-control" type="text" placeholder="place" v-model="place">
    <input class="form-control" type="number" placeholder="capacity" v-model="capacity">
    <button class="btn btn primary " >Edit Theater</button>
    
    </form>
    </div>
    </template>
    <script>
    import axios from 'axios'
    export default {
    name: "CreateTheater",
    props : ['id'],
    data() {
    return {
        theaterid: this.$route.params.id,
    name: "",
    place: "",
    capacity: null
    }
    },
    methods: {
        async edittheater() {
                let token =  localStorage.getItem("token")
                const response = await axios.post("edittheater/"+this.theaterid, {
                    name: this.name,
                    place: this.place,
                    capacity: this.capacity
            }, {
                    headers: {
                        Authorization: "Bearer " + token
                    }});
            if (response.data.message == "success") {
                console.log("edittheater successful")
                console.log(response)
                this.$router.push('/viewtheater');
            } else {
                console.log(response)
                console.log("editshow failed")
                alert("Edit Theater failed")
                this.$router.push('/viewtheater');
            }
        },
        async gettheater(){
            let token = localStorage.getItem("token")
            const response = await axios.get('gettheater/'+this.theaterid,{headers: {Authorization: "Bearer " + token}});
            if (response.data.message=="success"){
                console.log("response")
                this.name = response.data.theater.name
                this.place = response.data.theater.place
                this.capacity = response.data.theater.capacity
            }
            else{
                console.log("response")
            }
    }
    },
    created() {
        this.gettheater()
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