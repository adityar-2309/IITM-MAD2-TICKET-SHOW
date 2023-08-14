<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light justify-content-center" >
    <div class="container-fluid">
      <div class="navbar-header" v-if="$store.state.checkadmin ==false">
    <router-link  class="navbar-brand" to="/">Home   </router-link> 
    </div>
    <div class="navbar-header" v-else-if="$store.state.checkadmin">
    <router-link  class="navbar-brand" to="/viewmovies">Admin Home   </router-link>
    </div>
    <div class="navbar-nav" v-if="$store.state.checkl == false" >
    <router-link  class="nav-link" to="/login">Login   </router-link> 
    <router-link  class="nav-link" to="/signup">Signup   </router-link>
    </div>
    <div v-else-if="$store.state.checkl && $store.state.checkadmin == false" class="navbar-nav">
    <router-link  class="nav-link" to="/tickets">Tickets   </router-link> 
    <router-link  class="nav-link" to="/theaters">View Theaters   </router-link>
    <router-link class="nav-link" to="/search">Search   </router-link>
    <a href="javascript:void(0)" class="nav-link" @click="logout">Logout</a>
  </div>
  <div v-else-if="$store.state.checkl && $store.state.checkadmin" class="navbar-nav">
    <router-link  class="nav-link" to="/viewmovies">Admin  View  </router-link>
    <router-link  class="nav-link" to="/admin">Admin  View Shows </router-link>
    <router-link  class="nav-link" to="/viewtheater">Admin View Theaters   </router-link>
    <a href="javascript:void(0)" class="nav-link" @click="logout">Logout</a>
    </div>
  </div>
  </nav>
  <router-view/>
</template>
<script>
import axios from 'axios';

export default{
  name:"App",
  methods:{
    logout(){
      this.$store.state.checkl = false;
      this.$store.state.checkadmin = false;
      localStorage.setItem("token", null);
      this.$router.push('/login');
    }
  }
}

</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
