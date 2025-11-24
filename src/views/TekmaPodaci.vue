<template>
    <div data-app class="obrub1">
        <v-row >
          <v-col cols="2" v-if="ligaGrb">
            <v-img :src="ligaGrb[0]" class="image-box"></v-img>
          </v-col>
          
          <v-col cols="4" >
            <div class="naslov" style="color: black !important; margin-top: 0px !important;">
              <h2>Pregled utakmica</h2>
            </div>
          </v-col>
        </v-row>

            <v-select
              label="Izaberite ligu za prikazati!"
              v-model="selectedLiga"
              @change="dohvatiUtakmice(), dohvatiKlubove(), dohvatiGrbLige()"
              style="width: 40%; margin-left: 30%;"
              :items="ligas"
            ></v-select>

            <v-text-field 
              v-model="kolo" 
              label="Broj utakmice (kolo)" 
              variant="underlined"
              style="width: 40%; margin-left: 30%;"
              ></v-text-field>

            <v-select
              label="Izaberite domaćina!"
              v-model="domacin"
              style="width: 40%; margin-left: 30%;"
              :items="gostiTim"
              @change="domaciDohvat()"
            ></v-select>

            <v-select
              label="Izaberite goste!"
              v-model="gosti"
              style="width: 40%; margin-left: 30%;"
              :items="domaciTim"
              @change="gostiDohvat()"
            ></v-select>
                
            <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
                class="search"
            ></v-text-field>

            <div class="center">

              <h3 style="color: black; text-align: center;">! Potrebno učitati podatke prije brisanja utakmice !</h3>

              <v-btn @click="dohvatiJednuUtakmicu(), dohvatTablicaDomacin(), dohvatTablicaGosti()" class="deleteBtn">Učitaj podatke!</v-btn>
              
              <v-btn @click="updateTablicaDomacin(), updateTablicaGosti(), deleteUtakmica()" class="deleteBtn">Izbriši utakmicu</v-btn>
            </div>

            <v-data-table
              :search="search"
              :headers="headers"
              :items="podaci"
              style="font-weight: bold; text-align: center;"
              class="elevation-1"
              :items-per-page="-1"
              hide-default-footer
            ></v-data-table>
    </div>
</template>

<script>
  import axios from 'axios';
  import { Auth } from '@/components/registracija';

  export default {
    data () {
      return {
        auth: Auth.state,
        search: '',
        selectedLiga: '',
        ligaGrb: '',
        domacin: '',
        gosti: '',
        kolo: "",
        ligas: [],
        headers: [
          { text: 'Kolo', value: 'kl'},
          { text: 'Domacin', value: 'dm'},
          { text: 'Golovi domačina', value: 'gd'},
          { text: ":", value: 'i'},
          { text: 'Golovi gostiju', value: 'gg'},
          { text: 'Gosti', value: 'gs'},
          { text: 'Liga', value: 'lg' },
          { text: 'Mjesto', value: 'ms' },
          { text: 'Stadion', value: 'std' },
          { text: 'Gledatelji', value: 'gl' },
          { text: 'Datum', value: 'dt' },
        ],
        podaci: [],
        polje1: [],
        klubs: [],
        domaciTim: [],
        gostiTim: [],
        domacinData: [],
        gostiData: [],
        utakmica: [],
        domBod: 0,
        gosBod: 0,
      }
    },

    mounted() {
      this.dohvatiLige();
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

      async dohvatiUtakmice() {
        try {
          const userEmail = this.auth.userEmail;
          const userLiga = this.selectedLiga;
          const response = await axios.get(`https://nogometna-aplikacija.onrender.com/api/utakmica/dohvat?email=${userEmail}&liga=${userLiga}`);
          if (response.status !== 200) {
             throw new Error('Network response was not ok');
        } 
        this.polje1 = response.data;
        } catch (error) {
          console.error('Greška prilikom dohvaćanja zapisa svih utakmica:', error);
        }
        this.dohvatPodatakaUtakmice();
      },

      async dohvatiJednuUtakmicu() {
        try {
          this.utakmica = [];
          const userEmail = this.auth.userEmail;
          const userLiga = this.selectedLiga;
          const userKolo = this.kolo;
          const userDomacin = this.domacin;
          const userGost = this.gosti;
          const response = await axios.get(`https://nogometna-aplikacija.onrender.com/api/utakmica/dohvat/jedna?email=${userEmail}&liga=${userLiga}&kolo=${userKolo}&domacin=${userDomacin}&gost=${userGost}`);
          if (response.status !== 200) {
             throw new Error('Network response was not ok');
        } 
        this.utakmica = response.data;
        } catch (error) {
          console.error('Greška prilikom dohvaćanja zapisa svih utakmica:', error);
        }
        this.domaciBodovi();
        this.gostiBodovi();
      },

      async dohvatiKlubove() {
        this.klubs=[];
        this.domaciTim=[];
        try {
          const userEmail = this.auth.userEmail;
          const userLiga = this.selectedLiga;
          const response = await axios.get(`https://nogometna-aplikacija.onrender.com/api/klub/dohvat?email=${userEmail}&liga=${userLiga}`);
          if (response.status !== 200) {
            throw new Error('Network response was not ok');
          } 
            this.klubs = response.data;
            this.gostiTim = this.klubs;
        } catch (error) {
          console.error('Greška prilikom dohvaćanja klubova:', error);
        }
      },

      domaciDohvat() {
        this.domaciTim = this.klubs.filter((klub) => klub !== this.domacin);
      },

      gostiDohvat() {
        this.gostiTim = this.klubs.filter((klub) => klub !== this.gosti);
      },


      dohvatPodatakaUtakmice() {
        this.podaci = [];

        const copiedData = [...this.polje1];

        // Sortirajte kopirane podatke po broju kola
        copiedData.sort((a, b) => a.kolo - b.kolo);

        copiedData.forEach((item) => {
          this.podaci.push({
            kl: item.kolo,
            dm: item.Domacin,
            gd: item.domacinGol,
            i: ":",
            gg: item.gostiGol,
            gs: item.Gosti,
            lg: item.Liga,
            ms: item.mjestoIgranja,
            std: item.stadionNaziv,
            gl: item.gledateljiBroj,
            dt: item.datum
          });
        });
      },

      async deleteUtakmica() {

        if(!this.selectedLiga) {
            alert("Prvo izaberite ligu");
          }
        else if(this.selectedLiga && !this.domacin && !this.gosti && !this.kolo) {
          alert("Morate izabrati 2 kluba koja su odigrali utakmicu i kolo u kojem se utakmica odigrala kako biste ju mogli izbrisati!");
        }
        else {
          try {
            if(confirm("Jeste li sigurni da želite izbridati utakmicu?")) {
              let response = await axios.patch("https://nogometna-aplikacija.onrender.com/api/utakmica/delete", {
                ligaName: this.selectedLiga,
                domacin: this.domacin,
                gost: this.gosti,
                korisnik: this.auth.userEmail,
                kolo: this.kolo
              })
              console.log('Document deleted successfully');
              window.location.reload();
            }
          } catch (error) {
            console.error('Error deleting document:', error);
          }
        }
      },

      async dohvatTablicaDomacin() {
        try {
          this.domacinData = [];
          const userEmail = this.auth.userEmail;
          const userLiga = this.selectedLiga;
          const domacinKlub = this.domacin;
          const response = await axios.get(`https://nogometna-aplikacija.onrender.com/api/tablica/dohvat/domacin?email=${userEmail}&liga=${userLiga}&domacin=${domacinKlub}`);
          if (response.status !== 200) {
            throw new Error('Network response was not ok');
          } 
            this.domacinData = response.data;
        } catch (error) {
          console.error('Greška prilikom ozvježivanja podataka za domaćina:', error);
        }
      },

      async domaciBodovi() {
        this.domBod = 0;
        if(this.utakmica[0].domacinGol > this.utakmica[0].gostiGol) {
          parseInt(this.domBod-=3);
        }
        else if(this.utakmica[0].domacinGol == this.utakmica[0].gostiGol) {
          parseInt(this.domBod-=1);
        }
      },

      async updateTablicaDomacin() {
        let response = await axios.patch("https://nogometna-aplikacija.onrender.com/api/tablica/update/domacin", {
          bodovi: parseInt(this.domacinData[0].bodovi) + parseInt(this.domBod),
          postignutiPogodci: parseInt(this.domacinData[0].postignutiPogodci) - parseInt(this.utakmica[0].domacinGol),
          primljeniPogodci: parseInt(this.domacinData[0].primljeniPogodci) - parseInt(this.utakmica[0].gostiGol),
          odigranihDvoboja: parseInt(this.domacinData[0].odigranihDvoboja) - parseInt(1),
          liga: this.selectedLiga,
          klub: this.domacin,
          korisnik: this.auth.userEmail
        })
      },

      async dohvatTablicaGosti() {
        try {
          this.gostiData = [];
          const userEmail = this.auth.userEmail;
          const userLiga = this.selectedLiga;
          const gostKlub = this.gosti;
          const response = await axios.get(`https://nogometna-aplikacija.onrender.com/api/tablica/dohvat/gost?email=${userEmail}&liga=${userLiga}&gost=${gostKlub}`);
          if (response.status !== 200) {
            throw new Error('Network response was not ok');
          } 
            this.gostiData = response.data;
        } catch (error) {
          console.error('Greška prilikom ozvježivanja podataka za goste:', error);
        }
      },

      async gostiBodovi() {
        this.gosBod = 0;
        if(this.utakmica[0].gostiGol > this.utakmica[0].domacinGol) {
          parseInt(this.gosBod-=3);
        }
        else if(this.utakmica[0].domacinGol == this.utakmica[0].gostiGol) {
          parseInt(this.gosBod-=1);
        }
      },

      async updateTablicaGosti() {
        let response = await axios.patch("https://nogometna-aplikacija.onrender.com/api/tablica/update/gost", {
          bodovi: parseInt(this.gostiData[0].bodovi) + parseInt(this.gosBod),
          postignutiPogodci: parseInt(this.gostiData[0].postignutiPogodci) - parseInt(this.utakmica[0].gostiGol),
          primljeniPogodci: parseInt(this.gostiData[0].primljeniPogodci) - parseInt(this.utakmica[0].domacinGol),
          odigranihDvoboja: parseInt(this.gostiData[0].odigranihDvoboja) - parseInt(1),
          liga: this.selectedLiga,
          klub: this.gosti,
          korisnik: this.auth.userEmail
        })
      },
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

  .search {
    margin-left: 30%;
    margin-right: 30%;
    margin-bottom: 30px;
  }
  .image-box {
  width: 200px;
  height: 200px; 
  } 

  .deleteBtn {
    background-color: red !important;
    color: white; 
    margin-top: 10px;
    margin-bottom: 30px;
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