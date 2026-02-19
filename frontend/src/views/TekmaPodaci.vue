<template>
    <div data-app class="obrub1">
        <v-row >
          <v-col cols="2" v-if="selectedLigaObj">
            <v-img :src="selectedLigaObj.grbLige" class="image-box"></v-img>
          </v-col>
          
          <v-col cols="4" >
            <div class="naslov" style="color: black !important; margin-top: 0px !important;">
              <h2>Pregled utakmica</h2>
            </div>
          </v-col>
        </v-row>

            <v-select
              label="Izaberite ligu za prikazati!"
              v-model="izabranaLiga"
              @change="dohvatiKlubove(), dohvatiUtakmice()"
              style="width: 40%; margin-left: 30%;"
              :items="ligas"
              item-text="naziv"
              item-value="_id"
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
              item-text="naziv"
              item-value="_id"
            ></v-select>

            <v-select
              label="Izaberite goste!"
              v-model="gosti"
              style="width: 40%; margin-left: 30%;"
              :items="domaciTim"
              @change="gostiDohvat()"
              item-text="naziv"
              item-value="_id"
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
              <v-btn @click="deleteUtakmica()" class="deleteBtn">Izbriši utakmicu</v-btn>
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
  import { Auth } from '@/components/registracija';
  import LeagueApi from '@/components/liga'
  import ClubApi from '@/components/klub';
  import MatchApi from '@/components/utakmica';
  import TableApi from '@/components/tablica';

  export default {
    data () {
      return {
        search: '',
        izabranaLiga: '',
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
        klubs: [],
        domaciTim: [],
        gostiTim: [],
      }
    },

    async mounted() {
      this.ligas = await LeagueApi.getLeagues();
    },

    computed: {
      selectedLigaObj() {
        return this.ligas.find(l => l._id === this.izabranaLiga)
      }
    },

    methods: {

      async dohvatiKlubove() {
        this.klubs=[];
        this.domaciTim=[];
        try {
          if (!this.izabranaLiga) return;
            const clubs = await ClubApi.getClubs(this.izabranaLiga);
            this.klubs = clubs;
            this.gostiTim = this.klubs;
            this.domaciTim = this.klubs;
        } catch (error) {
            console.error('Greška prilikom dohvaćanja klubova:', error);
        }
      },

      domaciDohvat() {
        this.domaciTim = this.klubs.filter(
          (klub) => klub._id !== this.domacin
        );
      },

      gostiDohvat() {
        this.gostiTim = this.klubs.filter(
          (klub) => klub._id !== this.gosti
        );
      },

      async dohvatiUtakmice() {
        if (!this.izabranaLiga) return;

        const datas = await MatchApi.getMatch(this.izabranaLiga);

        this.podaci = datas.map((item) => ({
          kl: item.kolo,
          dm: item.domacin,
          gd: item.domacinGol,
          i: ":",
          gg: item.gostiGol,
          gs: item.gost,
          lg: item.ligaNaziv,
          ms: item.mjesto,
          std: item.stadion,
          gl: item.gledatelji,
          dt: item.datum,
        }));
      },

      async deleteUtakmica() {

        if (!confirm("Jesi siguran?")) return;

        const res = await MatchApi.deleteMatch({
          liga: this.izabranaLiga,
          domacin: this.domacin,
          gost: this.gosti,
          kolo: this.kolo
        });

        if (res.deleted > 0) {
          await this.dohvatiUtakmice();
          alert("Utakmica obrisana ✅");
        } else {
          alert("Utakmica nije pronađena ❌");
        }
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