<template>
    <div id="#app">
        <h1>Signup</h1>
        <form @submit.prevent="signup">
            <input class="form-control" type="text" placeholder="name" v-model="name">
            <input  class="form-control" type="text" placeholder="email" v-model="email">
            <input class="form-control" type="password" placeholder="password" v-model="password">
            <button class="btn btn primary " >Signup</button>
        </form>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name:"Signup",
    data() {
        return {
            name: '',
            email: '',
            password: ''
        }
    },
    methods: {
        async signup() { 
            const response = await axios.post('signup', {
                name: this.name,
                email: this.email,
                password: this.password
            });
            this.$router.push('/login');

            
        }
    }
}

    
</script>

<style></style>