<template>
  <div>
    <div class="naslov">
      <h1>Kreiraj igrača</h1>
    </div>
    
    <div class="obrub" data-app>
      <v-form ref="form" v-model="form" style="margin-top: 20px;">
        <v-text-field v-model="playerName" label="Naziv igrača" variant="underlined" :rules="[rules.required]"></v-text-field>
        
        <v-col
            cols="12"
            sm="6"
            md="4"
        >
            <v-dialog
                ref="dialog"
                v-model="modal"
                :return-value.sync="date"
                width="80%"
            >
                <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                        v-model="date"
                        label="Datum rođenja igrača"
                        prepend-icon="mdi-calendar"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                        :rules="[rules.required]"
                    ></v-text-field>
                </template>
                <v-date-picker
                    v-model="date"
                    scrollable
                >
                    <v-spacer></v-spacer>
                    <v-btn
                        text
                        color="primary"
                        @click="$refs.dialog.save(null); modal = false"
                    >
                        Cancel
                    </v-btn>
                    <v-btn
                        text
                        color="primary"
                        @click="$refs.dialog.save(date)"
                    >
                        OK
                    </v-btn>
                </v-date-picker>
            </v-dialog>
        </v-col>

        <v-text-field v-model="playerCountry" label="Državljanstvo" variant="underlined" :rules="[rules.required]"></v-text-field>

        <v-row class="row2">
          <v-col>
            <div>
              <v-select
                :rules="[rules.required]"
                :items="clubs"
                label="Izaberite klub za igrača!"
                v-model="selectedClub"
                class="vselect"
                item-text="naziv"
                item-value="_id"
              ></v-select>
              <br><br>
            </div>
          </v-col>
        </v-row>
          
        <h3 style="color: black">! Potrebno postaviti link slike sa interneta ili diskorda !</h3>

        <v-text-field
          class="butot"  
          v-model="playerImage"
          :rules="[rules.required]"
          label="Slika igrača"
        ></v-text-field>

        <v-text-field
          v-model.number="initialValue"
          label="Početna vrijednost ugovora (€)"
          type="number"
          min="0"
          :rules="[rules.required]"
        ></v-text-field>
      </v-form>

      <v-btn 
         @click="kreirajIgraca()" 
        elevation="2" 
        :disabled="!form"
        :loading="isLoading"
        style="background-color: green; color: white; margin-top:40px; margin-left: 85% !important;">Kreiraj!
      </v-btn>
    </div>
   </div>
</template>

<script>
  import { Auth } from "@/components/registracija";
  import ClubApi from "@/components/klub";
  import LigaApi from "@/components/liga";
  import BlockchainService from "@/components/igrac_transfer";

  export default {
    name: "CreatePlayer",
    data: () => ({
      playerName: null,
      playerCountry: null,
      playerImage: null,
      initialValue: 0,
      clubs: [],
      selectedClub: "",
      modal: false,
      form: false,
      isLoading: false,

      date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      rules: {
        required: v => !!v || "This field is required",
      },
    }),

    async mounted() {
      await this.dohvatiKlubove();
    },

    methods: {
      clearFormData() {
        this.playerName = null;
        this.playerCountry = "Hrvatska";
        this.playerImage = null;
        this.selectedClub = "";
      },

      async dohvatiKlubove() {
        try {
          const leagues = await LigaApi.getLeagues();
          let allClubs = [];
          for (const league of leagues) {
            const clubs = await ClubApi.getClubs(league._id);
            allClubs = [...allClubs, ...clubs];
          }
          this.clubs = allClubs;
        } catch (error) {
          console.error("Greška prilikom dohvaćanja klubova:", error);
        }
      },

      async kreirajIgraca() {
        if (!this.$refs.form.validate()) return;
        
        this.isLoading = true;
        try {
          await BlockchainService.registerPlayer(
            this.playerName,
            this.selectedClub,
            this.date,
            this.playerImage,
            this.initialValue,
            this.playerCountry
          );
          this.clearFormData();
          this.$refs.form.reset();
        } catch (error) {
          console.error("Greška pri kreiranju igrača:", error);
        } finally {
          this.isLoading = false;
        }
      }
    }
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