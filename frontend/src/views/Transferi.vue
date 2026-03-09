<template>
  <div>
    <div class="naslov">
      <h1>Transfer igrača</h1>
    </div>
    
    <div class="obrub" data-app>
      <v-form ref="form" v-model="form" style="margin-top: 20px;">
        <v-select
          :rules="[rules.required]"
          :items="players"
          label="Izaberite igrača za transfer"
          v-model="selectedPlayer"
          class="vselect"
          item-text="ime"
          return-object
        ></v-select>

        <v-row class="row2" v-if="selectedPlayer">
            <v-col>
                <p style="color: black">Trenutni klub: <strong>{{ currentClubName }}</strong></p>
            </v-col>
        </v-row>

        <v-select
          :rules="[rules.required]"
          :items="clubs"
          label="Izaberite NOVI klub"
          v-model="selectedClub"
          class="vselect"
          item-text="naziv"
          item-value="_id"
        ></v-select>

        <v-text-field
          v-model.number="transferValue"
          label="Vrijednost transfera (€)"
          type="number"
          min="0"
          :rules="[rules.required]"
        ></v-text-field>

      </v-form>

      <v-btn 
        @click="obaviTransfer()" 
        elevation="2" 
        :disabled="!form || (selectedPlayer && selectedPlayer.klub === selectedClub)"
        :loading="isLoading"
        style="background-color: green; color: white; margin-top:40px; margin-left: 80% !important;">Obavi Transfer!
      </v-btn>
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
    name: "Transfers",
    data: () => ({
      players: [],
      clubs: [],
      selectedPlayer: null,
      selectedClub: "",
      transferValue: 0,
      form: false,
      isLoading: false,
      rules: {
        required: v => !!v || "This field is required",
      },
    }),

    computed: {
        currentClubName() {
            if (!this.selectedPlayer) return "";
            const club = this.clubs.find(c => c._id === this.selectedPlayer.klub);
            return club ? club.naziv : "Nepoznat klub";
        }
    },

    async mounted() {
      await this.dohvatiPodatke();
    },

    methods: {
      async dohvatiPodatke() {
        try {
          // 1. Fetch Clubs
          const leagues = await LigaApi.getLeagues();
          let allClubs = [];
          for (const league of leagues) {
            const clubs = await ClubApi.getClubs(league._id);
            allClubs = [...allClubs, ...clubs];
          }
          this.clubs = allClubs;

          // 2. Fetch Players
          const footballerApi = process.env.VUE_APP_FOOTBALLER_API || "http://localhost:8006";
          const res = await axios.get(`${footballerApi}/api/footballer/dohvat`, {
              headers: { Authorization: `Bearer ${Auth.getToken()}` }
          });
          this.players = res.data;


        } catch (error) {
          console.error("Greška prilikom dohvaćanja podataka:", error);
        }
      },

      async obaviTransfer() {
        if (!this.$refs.form.validate()) return;
        
        this.isLoading = true;
        try {
          await BlockchainService.transferPlayer(
            this.selectedPlayer._id,
            this.selectedPlayer.klub,
            this.selectedClub,
            this.selectedPlayer.blockchainPlayerId,
            this.transferValue
          );

          
          await this.dohvatiPodatke(); // Refresh list
          this.selectedPlayer = null;
          this.selectedClub = "";
          this.$refs.form.reset();
        } catch (error) {
          console.error("Greška pri transferu:", error);
        } finally {
          this.isLoading = false;
        }
      }
    }
  };
</script>

<style>
  .obrub {
    border: 2px solid white;
    background-color: white;
    padding: 50px;
    margin-left: 20%;
    margin-right: 20%;
    margin-top: 100px; 
  }

  .v-text-field {
    font-size: 20px !important;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    font-weight: bold;
  }

  .row2 {
    color: black;
    text-align: center;
  }

  .vselect {
    font-size: 20px !important;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif !important;
  }
</style>
