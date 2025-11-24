import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/Home.vue'
import aboutUs from '../views/AboutUs.vue'
import login from '../views/Login.vue'
import signup from '../views/Signup.vue'
import k_ligu from '../views/KreirajLIGU.vue'
import k_klub from '../views/KreirajKLUB.vue'
import k_tekmu from '../views/KreirajTEKMU.vue'
import passReset from '../views/passReset.vue'
import Table from '../views/Tablica.vue'
import TekmaPodaci from '../views/TekmaPodaci.vue'
import userSettings from '../views/userSettings.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/AboutUs',
    name: 'About us',
    component: aboutUs
  },
  {
    path: '/Login',
    name: 'LogIn',
    component: login
  },
  {
    path: '/Signup',
    name: 'SignUp',
    component: signup
  },
  {
    path: '/KreirajLigu',
    name: 'KreirajLigu',
    component: k_ligu
  },
  {
    path: '/KreirajKlub',
    name: 'KreirajKlub',
    component: k_klub
  },
  {
    path: '/KreirajUtakmicu',
    name: 'KreirajUtakmicu',
    component: k_tekmu
  },
  {
    path: '/passReset',
    name: 'Reset your password',
    component: passReset
  },
  {
    path: '/Tablica',
    name: 'Tablica',
    component: Table
  },
  {
    path: '/TekmaPodaci',
    name: 'Podaci za utakmice',
    component: TekmaPodaci
  },
  {
    path: '/userSettings',
    name: 'Korisničke postavke',
    component:userSettings
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
