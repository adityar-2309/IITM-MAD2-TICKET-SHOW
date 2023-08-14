<template>
<div id="#app">
<h1>Admin Create Theater</h1>
<form @submit.prevent="createtheater">
<input class="form-control" type="text" placeholder="name" v-model="name">
<input class="form-control" type="text" placeholder="place" v-model="place">
<input class="form-control" type="number" placeholder="capacity" v-model="capacity">
<button class="btn btn primary " >Create Theater</button>

</form>
</div>
</template>
<script>
import axios from 'axios'
export default {
name: "CreateTheater",
data() {
return {
name: "",
place: "",
capacity: null
}
},
methods: {
    async createtheater() {
            let token =  localStorage.getItem("token")
            const response = await axios.post("createtheater", {
                name: this.name,
                place: this.place,
                capacity: this.capacity
        }, {
                headers: {
                    Authorization: "Bearer " + token
                }});
        if (response.data.message == "success") {
            console.log("createtheater successful")
            console.log(response)
            this.$router.push('/viewtheater');
        } else {
            console.log(response)
            console.log("createtheater failed")
        }
    }
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