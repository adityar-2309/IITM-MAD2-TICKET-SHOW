<template>
<div id="#app">
<h1>Admin View Theater</h1>
<table>
<tr>
<th>Name</th>
<th>Place</th>
<th>Capacity</th>

</tr>
<tr v-for="theater in theaters" :key="theater.id">
<td>{{theater.name}}</td>
<td>{{theater.place}}</td>
<td>{{theater.capacity}}</td>
<td><router-link :to="{name: 'edittheater', params: {id: theater.id}}">Edit Theater</router-link></td>
<td><a href="javascript:void(0)" @click="deletetheater(theater.id)">Delete Theater</a></td>
</tr>

</table>
<router-link to="/createtheater">Create Theater</router-link>

</div>
</template>
<script>
import axios from 'axios'
export default {
name: "ViewTheater",
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
async deletetheater(id){
    let token = localStorage.getItem("token")
    const response = await axios.post("deletetheater/"+id,{}, {
    headers: {
    Authorization: "Bearer " + token
    }});
if (response.data.message == "success") {
    console.log(response)
    console.log("deletetheater successful")
    this.gettheaters()
    } else {
console.log(response)
console.log("deletetheater failed")
}

}
},
created() {
this.gettheaters()
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