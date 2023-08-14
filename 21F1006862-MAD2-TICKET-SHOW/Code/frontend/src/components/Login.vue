<template>
    <div id="#app">
        <h1>Login</h1>
        <form @submit.prevent="login">
            <input class="form-control" type="text" placeholder="email" v-model="email">
            <input class="form-control" type="password" placeholder="password" v-model="password">
            <button class="btn btn primary">Login</button>
        </form>
        
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name: "Login",
    data() {
        return {
            email: "",
            password: ""
        }
    },
    methods: {
      async  login() {
        const response = await axios.post('login', {
            email: this.email,
            password: this.password
        });
        if (response.data.message == "login successful") {
            console.log("login successful", response.data)
            console.log(response.data.token)
            localStorage.setItem("token", response.data.access_token)
            this.$store.commit("setcheckl", true)
            this.$router.push('/');
        }
        else if (response.data.message == "admin login successful") {
            console.log("admin login successful", response.data)
            console.log(response.data.token)
            localStorage.setItem("token", response.data.access_token)
            this.$router.push('/admin');
        }
        else {
            console.log(response)
            console.log("login failed")
            alert("Invalid Credentials")
            this.$router.push('/login');
        }
    }
}
}    
</script>
<style></style>