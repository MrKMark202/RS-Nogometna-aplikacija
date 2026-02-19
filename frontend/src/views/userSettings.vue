<template>
  <div class="obrub">

    <h3 class="tekst naslov">Korisničke postavke</h3>

    <v-img :src="userData.profilnaSlika" class="profilna"></v-img>

    <h3 class="tekst">Ime</h3>
    <h3 class="podaci">{{ userData.ime }}</h3>

    <h3 class="tekst">Prezime</h3>
    <h3 class="podaci">{{ userData.prezime }}</h3>

    <h3 class="tekst">Datum rođenja</h3>
    <h3 class="podaci">{{ userData.datumRodenja }}</h3>

    <h3 class="tekst">Email korisnika</h3>
    <h3 class="podaci">{{ userData.email }}</h3>

    <!-- UPDATE PROFIL -->
    <div class="center" v-if="zastavica">

      <h3 class="tekst podnaslov">Ažuriraj profil</h3>

      <v-text-field
        v-model="profilna"
        label="Nova profilna slika"
        class="full-width"
      ></v-text-field>

      <v-btn class="btn_style" @click="updateUser()">
        Ažuriraj profil
      </v-btn>

      <v-btn class="btn_style" @click="zastavica = false">
        Odustani
      </v-btn>

    </div>

    <!-- PROMJENA LOZINKE -->
    <div class="center" v-if="zastavica2">

      <h3 class="tekst podnaslov">Promijeni lozinku</h3>

      <v-text-field
        v-model="password"
        :rules="[rules.password, rules.length(6), rules.required]"
        filled
        type="password"
        label="Nova lozinka"
      ></v-text-field>

      <v-btn class="btn_style" @click="updateUserLozinka()">
        Promijeni lozinku
      </v-btn>

      <v-btn class="btn_style" @click="zastavica2 = false">
        Odustani
      </v-btn>

    </div>

    <!-- DEFAULT BUTTONI -->
    <div class="center" v-if="!zastavica && !zastavica2">

      <v-btn class="btn_style" @click="zastavica = true">
        Ažuriraj profil
      </v-btn>

      <v-btn class="btn_style" @click="zastavica2 = true">
        Promijeni lozinku
      </v-btn>

      <v-btn
        class="btn_style delete_btn"
        @click="deleteUser"
      >
        Izbriši račun
      </v-btn>

    </div>

  </div>
</template>
<script>
import { Auth } from '@/components/registracija'

export default {

  data: () => ({
    userData: [],
    zastavica: false,
    zastavica2: false,
    profilna: null,
    password: null,
    rules: {
      length: len => v => (v || '').length >= len || `Invalid character length, required ${len}`,
      password: v => !!(v || '').match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$/) ||
      'Password must contain an upper case letter, a numeric character, and a special character',
      required: v => !!v || 'This field is required',
    },
  }),

  mounted() {
    this.dohvatiKorisnika();
  },

  methods: {

    async dohvatiKorisnika() {
      try {
        this.userData = await Auth.fetchUserData(Auth.state.userEmail);
      } catch (error) {
        console.error("Greška dohvat usera:", error);
      }
    },

    async updateUser() {
      await Auth.updateProfile(
        this.profilna,
        Auth.state.userEmail
      );

      window.location.reload();
    },

    async updateUserLozinka() {
        const success = await Auth.passwordChange(
            this.password,
            Auth.state.userEmail
        );

        if (success) {
            alert("Lozinka uspješno promijenjena ✅");
            this.signOut();
        } else {
            alert("Promjena lozinke nije uspjela ❌");
        }
    },


    async deleteUser() {
      if (!confirm("Jeste li sigurni?")) return;

      await Auth.deleteUser(Auth.state.userEmail);

      alert("Korisnički profil je izbrisan!");
      this.signOut();
    },

    signOut() {
      Auth.logout();
      this.$router.push({ path: "/Login" });
    },

    funkcijaTrue() {
      this.zastavica = true;
    },

    funkcijaTrue2() {
      this.zastavica2 = true;
    },

    funkcijaFalse() {
      this.zastavica = false;
    },

    funkcijaFalse2() {
      this.zastavica2 = false;
    }
  }
}
</script>
<style scoped>
    .obrub
    {
        border: 2px solid white;
        background-color: white;
        padding: 50px;
        margin-left: 20%;
        margin-right: 20%;
        margin-top: 100px; 
    }

    .profilna
    {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background-color: Green; 
        margin-left: auto;
        margin-right: auto;
        
    }

    .tekst
    {
        color: black;
        font-size: 50px;
        margin-top: 10px;
    }

    .podaci
    {
        color: black;
        font-size: 30px;
        margin-top: 10px;
        border: 2px green double;
    }

    .btn_style 
    {
        background-color: green !important;
        color: white !important;
        font-weight: bold;
        margin-top: 30px;
        font-size: 30px;
    }

    .center
    {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
</style>