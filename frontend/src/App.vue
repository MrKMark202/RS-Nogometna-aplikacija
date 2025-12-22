<template>
  <nav>
    <div class="grid-container">
      <div class="grid-item1">
        <v-app-bar-nav-icon
          @click.stop="drawer = !drawer"
          style="color: white;"
          v-if="auth.authenticated"
        ></v-app-bar-nav-icon>

        <v-navigation-drawer
          v-model="drawer"
          absolute
          temporary
          style="background-color: green; width: 30%;"
        >
          <v-list style="padding: 10px">
            <v-list-item-group
              v-model="group"
              active-class="deep-purple--text text--accent-4"
            >
              <v-list-item to="/" class="btn_style">
                🏚  Home
              </v-list-item>
              <hr>
              <v-list-item to="/AboutUs" class="btn_style">
                👁‍🗨  About us
              </v-list-item>
              <hr>
              <v-list-item  to="/KreirajLigu" class="btn_style">
                🏆  Kreiraj ligu
              </v-list-item>
              <hr>
              <v-list-item  to="/KreirajKlub" class="btn_style">
                ⚽  Kreiraj klub
              </v-list-item>
              <hr>
              <v-list-item  to="/KreirajUtakmicu" class="btn_style">
                🆚  Kreiraj utakmicu
              </v-list-item>
              <hr>
              <v-list-item  to="/Tablica" class="btn_style">
                📊  Tablica
              </v-list-item>
              <hr>
              <v-list-item  to="/TekmaPodaci" class="btn_style">
                📃  Pregled utakmica
              </v-list-item>
              <hr>
              <v-list-item  to="/userSettings" class="btn_style">
                🛂  Korisničke postavke
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-navigation-drawer>
      </div>
      <div style="text-align: right; font-size: 30px !important;">
        <v-btn
          v-if="!auth.authenticated"
          class="btn_style"
          elevation="2"
          to="/Login"
        >
          LogIn
        </v-btn>
        <a v-if="!auth.authenticated" > | </a>
        <v-btn
          v-if="!auth.authenticated"
          class="btn_style"
          elevation="2"
          to="/Signup"
        >
          SignUp
        </v-btn>
        <p v-if="auth.authenticated" class="p">
          <img v-if="auth.authenticated" class="profilna" :src="auth.userProfilePicture">
          {{ auth.userEmail }} |
          <v-btn v-if="auth.authenticated" href="#" @click.prevent="signOut()" class="btn_style">LogOut</v-btn>
        </p>
      </div>
    </div>
    <router-view></router-view>
  </nav>
</template>

<script>
  import { Auth } from '@/components/registracija'

  export default {
    data: () => ({
      drawer: false,
      group: null,
      auth: Auth.state,
    }),

    watch: {
      group () {
        this.drawer = false;
      },
    },

    methods: {
      async signOut() {
        Auth.logout();
        this.$router.push({path: "/Login"});
      }
    }
  };
</script>

<style scoped lang="scss">
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    color: #2c3e50;
  }

  .grid-container {
    display: grid;
    grid-template-columns: auto auto;
    padding: 20px;
    background-color: rgb(7, 45, 7);
  }

  .grid-item1 {
    font-size: 30px;
  }

  .btn_style {
    background-color: green !important;
    color: white !important;
    font-weight: bold;
    margin-left: 10px;
    margin-bottom: 10px;
  }

  .profilna
  {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #007bff; 
    margin-right: 10px;
  }

  .p
  {
    display:inline-flex;
    color: white;
    align-items: center;
  };
</style>