<template>
    <div>
        <div class="naslov">
            <h1>Kreiraj ligu</h1>
        </div>
    
        <div class="obrub">
            <v-form ref="form" v-model="form" style="margin-top: 20px;">
                <v-text-field v-model="ligaName" label="Naziv Lige" variant="underlined" :rules="[rules.required]"></v-text-field>
                <v-text-field v-model="ligaYear" label="Godina osnivanja" variant="underlined" :rules="[rules.required]"></v-text-field>
                <v-text-field v-model="ligaCountry" label="Država" variant="underlined" :rules="[rules.required]"></v-text-field>
            

                <h3 style="color: black">! Potrebno postaviti link slike sa interneta ili diskorda !</h3>

                <v-text-field
                    class="butot"  
                    v-model="grbLige"
                    :rules="[rules.required]"
                    label="Grb lige"
                ></v-text-field>
            </v-form>
            <v-btn 
                type="button"
                elevation="2" class="btn_style" 
                style="background-color: green; color: white; margin-top:40px; margin-left: 85% !important;"
                :disabled="!form"
                :loading="isLoading"
                @click="kreirajLigu()" 
            >Kreiraj!</v-btn>
        </div>
    </div>
</template>

<script>
    import { Auth } from '@/components/registracija'
    import axios from 'axios'

    export default {
        name: "createLIGA",
        data: () => ({
            auth : Auth.state,
            ligaName: null,
            ligaYear: null,
            ligaCountry: null,
            form: false,
            isLoading: false,
            grbLige: null,
            rules: {
                required: v => !!v || 'This field is required'
            },
        }),

        methods: {
            clearFormData() {
                this.ligaName = null;
                this.ligaYear = null;
                this.ligaCountry = null;
                this.grbLige = null;
            },

           async kreirajLigu() {
            	let response = await axios.post("https://nogometna-aplikacija.onrender.com/api/liga/create", {
                    ligaName: this.ligaName,
                    ligaYear: this.ligaYear,
                    ligaCountry: this.ligaCountry,
                    grbLige: this.grbLige,
                    userEmail: this.auth.userEmail
                })

                this.clearFormData();
            }
        }
    }
</script>


<style>
    .obrub
    {
        border: 2px solid white;
        background-color: white;
        padding: 50px;
        margin-left: 25% !important;
        margin-right: 25% !important;
        margin-top: 100px;

        
    }

    .v-text-field
    {
        font-size: 20px;
        font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
        font-weight: bold;
    }

    .butot
    {
        margin-top: 20px;
        background-color: green;
        color: black;
        font-size: 20px;
        font-weight: bold;
    }

    .grb
    {
        margin-top: 20px;
        color: black;
        font-size: 30px;
    }
</style>