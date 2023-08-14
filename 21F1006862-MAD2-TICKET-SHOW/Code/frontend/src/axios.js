import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:3435';
let token = localStorage.getItem("token")
axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
