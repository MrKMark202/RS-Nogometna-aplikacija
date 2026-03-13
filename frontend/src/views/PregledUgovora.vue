<template>
  <div>
    <div class="naslov">
      <h1>Pregled ugovora igrača</h1>
    </div>
    
    <div class="obrub" data-app>
      <v-form style="margin-bottom: 30px;">
        <v-autocomplete
          :items="players"
          label="Izaberite igrača za pregled ugovora"
          v-model="selectedPlayer"
          class="vselect"
          item-text="ime"
          return-object
          @change="fetchContracts"
          clearable
        ></v-autocomplete>
      </v-form>

      <div v-if="selectedPlayer">
          <v-row align="center">
            <v-col cols="auto">
              <v-img
                v-if="selectedPlayer.slikaIgraca"
                :src="selectedPlayer.slikaIgraca"
                width="150"
                height="150"
                class="player-img"
              ></v-img>
            </v-col>
            <v-col>
              <h2 style="color: black;">Povijest transfera za: {{ selectedPlayer.ime }}</h2>
            </v-col>
            <v-col cols="auto">
              <v-btn @click="confirmDeletePlayer" :loading="isDeleting" style="color: white; text-decoration: solid; background-color: red; margin-bottom: 50px;">
                Izbriši igrača
              </v-btn>
            </v-col>
          </v-row>
          
          <v-simple-table v-if="contracts.length > 0" class="mt-8">
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">Iz kluba</th>
                  <th class="text-left">U klub</th>
                  <th class="text-left">Datum transfera</th>
                  <th class="text-left">Vrijednost (€)</th>
                  <th class="text-left">Ugovor traje do</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in contracts" :key="index">
                  <td>{{ item.fromClub === 'INITIAL_SIGNING' ? 'Prvo potpisivanje' : getClubName(item.fromClub) }}</td>
                  <td>{{ getClubName(item.toClub) }}</td>
                  <td>{{ item.timestamp }}</td>
                  <td>{{ (item.value || 0).toLocaleString() }} €</td>
                  <td :style="{ color: item.ugovorTrajeDo === 'Raskid ugovora' ? 'red' : 'black' }">
                    {{ item.ugovorTrajeDo && item.ugovorTrajeDo !== '' ? item.ugovorTrajeDo : '---' }}
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
          
          <div v-else-if="!loading" style="text-align: center; padding: 20px;">
              <p style="color: grey;">Nema zabilježenih transfera na blockchainu za ovog igrača.</p>
          </div>
          
          <v-progress-linear v-if="loading" indeterminate color="green"></v-progress-linear>
      </div>
    </div>
   </div>
</template>

<script>
  import { Auth } from "@/components/registracija";
  import ClubApi from "@/components/klub";
  import LigaApi from "@/components/liga";
  import BlockchainService from "@/components/igrac_transfer";
  import axios from "axios";

  export default {
    name: "PregledUgovora",
    data: () => ({
      players: [],
      clubs: [],
      contracts: [],
      selectedPlayer: null,
      loading: false,
      isDeleting: false,
    }),

    async mounted() {
      await this.dohvatiPodatke();
    },

    methods: {
      async dohvatiPodatke() {
        try {
          const leagues = await LigaApi.getLeagues();
          let allClubs = [];
          for (const league of leagues) {
            const clubs = await ClubApi.getClubs(league._id);
            allClubs = [...allClubs, ...clubs];
          }
          this.clubs = allClubs;

          const footballerApi = process.env.VUE_APP_FOOTBALLER_API || "http://localhost:8006";
          const res = await axios.get(`${footballerApi}/api/footballer/dohvat`, {
              headers: { Authorization: `Bearer ${Auth.getToken()}` }
          });

          this.players = res.data;
        } catch (error) {
          console.error("Greška prilikom dohvaćanja podataka:", error);
        }
      },

      async fetchContracts() {
          if (!this.selectedPlayer) return;
          
          const pId = this.selectedPlayer._id;
          console.log("PregledUgovora: Odabran igrač:", this.selectedPlayer.ime, "DB ID:", pId);

          if (!pId) {
              alert("Ovaj igrač nema ispravan ID.");
              this.contracts = [];
              return;
          }
          
          this.loading = true;
          try {
              // Fetch contract history from Database (PRIMARY SOURCE)
              const dbContracts = await BlockchainService.getDatabaseContracts(pId);
              
              console.log("PregledUgovora: Database podaci:", dbContracts);

              if (dbContracts.length > 0) {
                  this.contracts = dbContracts.map(dbc => ({
                      fromClub: dbc.fromClub,
                      toClub: dbc.toClub,
                      timestamp: dbc.timestamp,
                      value: dbc.value,
                      ugovorTrajeDo: dbc.ugovorTrajeDo || ""
                  }));
                  console.log("PregledUgovora: Koristim podatke iz baze.");
              } else {
                  this.contracts = [];
              }
              
              console.log("PregledUgovora: Podaci za prikaz:", this.contracts);
          } catch (error) {
              console.error("PregledUgovora error:", error);
              this.contracts = [];
          } finally {
              this.loading = false;
          }
      },

      async confirmDeletePlayer() {
          if (!this.selectedPlayer) return;
          if (confirm(`Jeste li sigurni da želite izbrisati igrača ${this.selectedPlayer.ime} i sve njegove podatke? Ovaj postupak je nepovratan.`)) {
              await this.deletePlayer();
          }
      },

      async deletePlayer() {
          this.isDeleting = true;
          try {
              await BlockchainService.deletePlayer(this.selectedPlayer._id);
              this.selectedPlayer = null;
              this.contracts = [];
              await this.dohvatiPodatke(); // Refresh list
          } catch (error) {
              console.error("Greška pri brisanju:", error);
          } finally {
              this.isDeleting = false;
          }
      },




      getClubName(id) {
          const club = this.clubs.find(c => c._id === id);
          return club ? club.naziv : id;
      }
    }
  };
</script>

<style scoped>
  .obrub {
    border: 2px solid white;
    background-color: white;
    padding: 50px;
    margin-left: 10%;
    margin-right: 10%;
    margin-top: 50px; 
    color: black;
  }

  .player-img {
    border-radius: 50%;
    margin-left: 0;
    margin-bottom: 20px;
    border: 2px solid #ccc;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  .vselect {
    font-size: 20px !important;
  }
</style>
