<template>
    <div>
      <div data-app class="obrub1">
        <v-row >
          <v-col cols="2" v-if="ligaGrb">
            <v-img :src="ligaGrb[0]" class="image-box"></v-img>
          </v-col>
          
          <v-col cols="4" >
            <div class="naslov" style="color: black !important; margin-top: 0px !important">
              <h1>Tablica</h1>
            </div>
          </v-col>
        </v-row>
       
        <div class="grid-container2">
          <v-btn class="grid-item4" @click="deleteLiga()" elevation="2" style="background-color: red; color: white; margin-top:40px; font-size: 30px;">Izbriši ligu!</v-btn>
          <v-btn class="grid-item4" @click="deleteKlub()" elevation="2" style="background-color: red; color: white; margin-top:40px; font-size: 30px;">Izbriši klub!</v-btn>
          <v-select
            class="grid-item4"
            label="Izaberite ligu za prikazati!"
            v-model="selectedLiga"
            style="width: 350px;"
            :items="ligas"
            @change="dohvatiKlubove(), dohvatiGrbLige()"
          ></v-select>

          <v-select
            class="grid-item4"
            label="Izaberite klub!"
            v-model="selectedKlub"
            style="width: 350px;"
            :items="klubs"
          ></v-select>
        </div>
                
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
          class="search"
        ></v-text-field> 

        <v-data-table
          :headers="headers"
          :items="podaci"
          :search="search"
          style="font-weight: bold; text-align: center;"
          item-key="nt"
          class="elevation-1"
          loading
          loading-text="Izaberite ligu!"
          :items-per-page="-1"
          hide-default-footer
        >
          <template v-slot:item.grb="{ item }">
            <v-img :src="item.grb" class="klub-grb"></v-img>
          </template>
        </v-data-table>
      </div>
  </div>
</template>

<script>

  import axios from 'axios';
  import { Auth } from '@/components/registracija'

  export default {
    data () {
      return {
        auth: Auth.state,
        search: '',
        selectedLiga: '',
        selectedKlub: '',
        ligaGrb: '',
        headers: [
            { text: 'Pozicija', value: 'pz'},
            { text: 'Grb', value: 'grb'},
            {
                text: 'Naziv tima',
                align: 'start',
                value: 'nt',
            },
            { text: 'Odigranih dvoboja', value: 'od' },
            { text: 'Postignuti pogodci', value: 'pp' },
            { text: 'Primljeni golovi', value: 'pg' },
            { text: 'Gol razlika', value: 'gr'},
            { text: 'Bodovi', value: 'bd', sortable: true},
        ],
        podaci: [],
        ligas: [],
        klubs:[],
      }
    },

    mounted() {
      this.dohvatiLige()
    },

    methods: {
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

      async dohvatiGrbLige() {
        try {
          const userEmail = this.auth.userEmail;
          const liga = this.selectedLiga;
          const response = await axios.get(`https://nogometna-aplikacija.onrender.com/api/liga/dohvat/grb?email=${userEmail}&liga=${liga}`);
          if (response.status !== 200) {
            throw new Error('Network response was not ok');
          } 
          this.ligaGrb = response.data;
        } catch (error) {
            console.error('Greška prilikom dohvaćanja liga:', error);
        }
      },


      async dohvatiKlubove() {
        this.klubs=[];
        try {
          const userEmail = this.auth.userEmail;
          const userLiga = this.selectedLiga;
          const response = await axios.get(`https://nogometna-aplikacija.onrender.com/api/klub/dohvat?email=${userEmail}&liga=${userLiga}`);
          if (response.status !== 200) {
            throw new Error('Network response was not ok');
        } 
          this.klubs = response.data
          this.dohvatiTablicu();
        } catch (error) {
          console.error('Greška prilikom dohvaćanja klubova:', error);
        }
      },

      async dohvatiTablicu() {
        this.datas = [];
        try {
          const userEmail = this.auth.userEmail;
          const userLiga = this.selectedLiga;
          const response = await axios.get(`https://nogometna-aplikacija.onrender.com/api/tablica/dohvat?email=${userEmail}&liga=${userLiga}`);
          if (response.status !== 200) {
            throw new Error('Network response was not ok');
          } 
          this.datas = response.data;
          this.dohvatiPodatkeTablice();
        } catch (error) {
          console.error('Greška prilikom dohvaćanja podataka tablice', error);
        }
      },

      async dohvatiPodatkeTablice() {
        this.podaci = [];
        const sortedDatas = [...this.datas];
        sortedDatas.sort((a, b) => {
          return b.bodovi - a.bodovi;
        });
        
        sortedDatas.forEach((item, index) => {
          this.podaci.push({
            pz: index + 1,
            grb: item.grbKlub,
            nt: item.klub,
            od: item.odigranihDvoboja,
            pp: item.postignutiPogodci,
            pg: item.primljeniPogodci,
            gr: item.postignutiPogodci - item.primljeniPogodci,
            bd: item.bodovi,
          });
        });
      },

      async deleteLiga() {

        if(!this.selectedLiga) {
          alert("Prvo izaberite ligu");
        }
        else {
          try {
            if(confirm("Jeste li sigurni da želite izbridati ligu")) {
              const response = await axios.patch(`https://nogometna-aplikacija.onrender.com/api/liga/delete`, {
                ligaName: this.selectedLiga,
                userEmail: this.auth.userEmail
              });
              await this.deleteKlub();
              console.log('Document deleted successfully');
              window.location.reload();
            }
          } catch (error) {
            console.error('Error deleting document:', error);
          }
        }
      },

      async deleteKlub() {

        if(!this.selectedLiga) {
          alert("Prvo izaberite ligu da bi ste mogli klub!");
        }
        
        else if(this.selectedLiga && !this.selectedKlub) {
          alert("Izaberite klub!");
        }
        else {
          try {
            if(confirm("Jeste li sigurni da želite izbrisati klub")) {
              const response = await axios.patch(`https://nogometna-aplikacija.onrender.com/api/klub/delete`, {
                ligaName: this.selectedLiga,
                userEmail: this.auth.userEmail,
                clubName: this.selectedKlub
              });
              await this.deleteTablica();
              console.log('Document deleted successfully');
              window.location.reload();
            }
          } catch (error) {
            console.error('Error deleting document:', error);
          }
        }
      },

      async deleteTablica() {
        const response = await axios.patch(`https://nogometna-aplikacija.onrender.com/api/tablica/delete`, {
          ligaName: this.selectedLiga,
          userEmail: this.auth.userEmail,
          clubName: this.selectedKlub
        });
      }
    }
  }
</script>

<style scoped>
  .obrub1
  {
    border: 2px solid white;
    background-color: white;
    padding: 50px;
    margin-left: 200px;
    margin-right: 200px;
    margin-bottom: 100px;
  }

  .grid-container2 {
    display: grid;
    grid-template-columns: auto auto;
    background-color: white;
    justify-content: space-between;
    align-items: center;
    margin-left: 10%;
    margin-right: 10%;
  }

  .grid-item4 {
    background-color: white;
    padding: 20px;
  }

  .klub-grb {
    max-width: 50px;
    max-height: 50px;
  }

  .search {
    margin-left: 30%;
    margin-right: 30%;
    margin-bottom: 30px;
  }

  .image-box {
    width: 200px;
    height: 200px; 
  } 

</style>