<template>
    <div>
      <div data-app class="obrub1">
        <v-row >
          <v-col cols="2" v-if="selectedLigaObj">
            <v-img :src="selectedLigaObj.grbLige" class="image-box"></v-img>
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
            @change="dohvatiKlubove(), dohvatiTablicu()"
            item-text="naziv"
            item-value="_id"
          ></v-select>

          <v-select
            class="grid-item4"
            label="Izaberite klub!"
            v-model="selectedKlub"
            style="width: 350px;"
            :items="klubs"
            item-text="naziv"
            item-value="_id"
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
  import { Auth } from '@/components/registracija'
  import LeagueApi from '@/components/liga';
  import ClubApi from '@/components/klub';
  import TableApi from "@/components/tablica";

  export default {
    data () {
      return {
        search: '',
        selectedLiga: '',
        selectedKlub: '',
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
        klubs: [],
      }
    },

    async mounted() {
      this.ligas = await LeagueApi.getLeagues();
    },

    computed: {
      selectedLigaObj() {
        return this.ligas.find(l => l._id === this.selectedLiga)
      }
    },

    methods: {

      async dohvatiKlubove() {
        this.klubs=[];
        try {
          if (!this.selectedLiga) return;

          const clubs = await ClubApi.getClubs(this.selectedLiga);

          this.klubs = clubs;
        } catch (error) {
          console.error('Greška prilikom dohvaćanja klubova:', error);
        }
      },

      async dohvatiTablicu() {
        if (!this.selectedLiga) return;

        const datas = await TableApi.getTable(this.selectedLiga);

        const sorted = [...datas].sort((a, b) => b.bodovi - a.bodovi);

        this.podaci = sorted.map((item, index) => ({
          pz: index + 1,
          grb: item.grbKlub,
          nt: item.klub,
          od: item.odigranihDvoboja,
          pp: item.postignutiPogodci,
          pg: item.primljeniPogodci,
          gr: item.postignutiPogodci - item.primljeniPogodci,
          bd: item.bodovi,
        }));
      },

      async deleteLiga() {
        if (!this.selectedLiga) {
          alert("Prvo izaberi ligu.");
          return;
        }

        if (!confirm("Jesi siguran da želiš obrisati ligu?")) return;

        const result = await LeagueApi.deleteLeague(this.selectedLiga);

        if (result) {
          alert("Liga je uspješno obrisana ✅");
          this.selectedLiga = "";
          location.reload();
        }
      },

      async deleteKlub() {
        if (!this.selectedKlub) {
          alert("Izaberi klub.");
          return;
        }

        if (!confirm("Jesi siguran da želiš obrisati klub?")) return;

        const result = await ClubApi.deleteClub(this.selectedKlub);

        if (result) {
          alert("Klub je uspješno obrisan ✅");
          this.selectedKlub = "";
          await this.dohvatiKlubove();
        }
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