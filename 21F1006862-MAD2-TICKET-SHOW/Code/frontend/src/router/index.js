import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Signup from '../components/Signup.vue'
import BookShow from '../components/BookShow.vue'
import Admin from '../components/Admin.vue'
import CreateShow from '../components/CreateShow.vue'
import EditShow from '../components/EditShow.vue'
import DeleteShow from '../components/DeleteShow.vue'
import Tickets from '../components/Tickets.vue'
import ViewTheater from '../components/ViewTheater.vue'
import CreateTheater from '../components/CreateTheater.vue'
import EditTheater from '../components/EditTheater.vue'
import Theaters from '../components/Theaters.vue'
import Theater from '../components/Theater.vue'
import CreateMovie from '../components/CreateMovie.vue'
import ViewMovies from '../components/ViewMovies.vue'
import EditMovie from '../components/EditMovie.vue'
import DeleteMovie from '../components/DeleteMovie.vue'
import ViewShow from '../components/ViewShow.vue'
import Search from '../components/Search.vue'



const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/login',
    name: 'login',
    component : Login,
    },
  {
    path: '/signup',
    name: 'signup',
    component : Signup,
  },
  {
    path: '/bookshow/:id',
    name: 'bookshow',
    component: BookShow
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
  },
  {
    path: '/createshow',
    name: 'createshow',
    component: CreateShow,
  },
  {
    path: '/editshow/:id',
    name: 'editshow',
    component: EditShow,
  },
  {
    path: '/deleteshow/:id',
    name: 'deleteshow',
    component: DeleteShow,
  },
  {
    path: '/tickets',
    name: 'tickets',
    component: Tickets,
  },
  {
    path: '/viewtheater',
    name: 'viewtheater',
    component: ViewTheater,
  },
  {
    path: '/createtheater',
    name: 'createtheater',
    component: CreateTheater,
  },
  {
    path: '/edittheater/:id',
    name: 'edittheater',
    component: EditTheater,
  },
  {
    path: '/theaters',
    name: 'theaters',
    component: Theaters,
  },
  {
    path: '/theater/:id',
    name: 'theater',
    component: Theater,
  },
  {
    path: '/createmovie',
    name: 'createmovie',
    component: CreateMovie,
  },
  {
    path: '/viewmovies',
    name: 'viewmovies',
    component: ViewMovies,
  },
  {
    path: '/editmovie/:id',
    name: 'editmovie',
    component: EditMovie,
  },
  {
    path: '/deletemovie/:id',
    name: 'deletemovie',
    component: DeleteMovie,
  },
  {
    path: '/viewshow/:id',
    name: 'viewshow',
    component: ViewShow,
  },
  {
    path: '/search',
    name: 'search',
    component: Search,
  },
]


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
