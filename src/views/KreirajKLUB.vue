<template>
  <div>
    <div class="naslov">
      <h1>Kreiraj klub</h1>
    </div>
    
    <div class="obrub" data-app>
      <v-form ref="form" v-model="form" style="margin-top: 20px;">
        <v-text-field v-model="clubName" label="Naziv kluba" variant="underlined" :rules="[rules.required]"></v-text-field>
        <v-text-field v-model="clubYear" label="Godina osnivanja" variant="underlined" :rules="[rules.required]"></v-text-field>
        <v-text-field v-model="clubCountry" label="Država" variant="underlined" :rules="[rules.required]"></v-text-field>

        <v-row class="row2">
          <v-col>
            <div>
              <v-select
                :rules="[rules.required]"
                :items="ligas"
                label="Izaberite ligu za koju kreirate klub!"
                v-model="selectedLiga"
                class="vselect"
              ></v-select>
              <br><br>
            </div>
          </v-col>
        </v-row>
          
        <h3 style="color: black">! Potrebno postaviti link slike sa interneta ili diskorda !</h3>

        <v-text-field
          class="butot"  
          v-model="clubGrb"
          :rules="[rules.required]"
          label="Grb kluba"
        ></v-text-field>
      </v-form>

      <v-btn 
         @click="kreirajKlub()" 
        elevation="2" 
        :disabled="!form"
        :loading="isLoading"
        style="background-color: green; color: white; margin-top:40px; margin-left: 85% !important;">Kreiraj!
      </v-btn>
    </div>
   </div>
</template>

<script>
  import axios from 'axios';
  import { Auth } from '@/components/registracija'

  export default {
    name: "CreateClub",
    data: () => ({
      auth: Auth.state,
      clubName: null,
      clubCountry: null,
      clubYear: null,
      clubGrb: null,
      ligas: [],
      selectedLiga: '',
      form: false,
      isLoading: false,
      rules: {
        required: v => !!v || 'This field is required'
      },
    }),

    mounted() {
      this.dohvatiLige();
    },

    methods: {
      clearFormData() {
			  this.clubName = null;
			  this.clubYear = null;
			  this.clubCountry = null;
        this.clubGrb = null;
        this.selectedLiga = '';
		  },

      async dohvatiLige() {
        try {
          const userEmail = this.auth.userEmail;
          const response = await axios.get(`https://nogometna-aplikacija.onrender.com/api/liga/dohvat?email=${userEmail}`);
          if (response.status !== 200) {
            throw new Error('Network response was not ok');
          } 
          this.ligas = response.data
        } catch (error) {
            console.error('Greška prilikom dohvaćanja liga:', error);
        }
      },

      async kreirajKlub() {
        let response = await axios.post("https://nogometna-aplikacija.onrender.com/api/klub/create", {
          clubName: this.clubName,
          clubYear: this.clubYear,
          clubCountry: this.clubCountry,
          clubGrb: this.clubGrb,
          liga: this.selectedLiga,
          userEmail: this.auth.userEmail
        })
        await this.kreirajTablicu();
        this.clearFormData();
      },

      async kreirajTablicu() {
        let response = await axios.post("https://nogometna-aplikacija.onrender.com/api/tablica/create", {
          bodovi: 0,
          postignutiPogodci: 0,
          primljeniPogodci: 0,
          odigranihDvoboja: 0,
          liga: this.selectedLiga,
          klub: this.clubName,
          grbKlub: this.clubGrb,
          userEmail: this.auth.userEmail
        })
      }
    },
  };
</script>


<style>
  .obrub
  {
    border: 2px solid white;
    background-color: white;
    padding: 50px;
    margin-left: 20%;
    margin-right: 20%;
    margin-top: 100px; 
  }

  .v-text-field
  {
    font-size: 20px !important;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    font-weight: bold;
  }

  .row2
  {
    color: black;
    text-align: center;
  }

  .vselect
  {
    font-size: 20px !important;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif !important;
  }
</style>