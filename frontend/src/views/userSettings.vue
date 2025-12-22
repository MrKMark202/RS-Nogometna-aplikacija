<template>
    <div class="obrub">
        
        <h3 class="tekst" style="text-align: center; font-size: 70px !important; margin-bottom: 50px;">Korisničke postavke</h3>
        
        <v-img :src="auth.userProfilePicture" class="profilna"></v-img>

        <h3 class="tekst">Ime</h3>
        <h3 class="podaci">{{ userData.ime }}</h3>

        <h3 class="tekst">Prezime</h3>
        <h3 class="podaci">{{ userData.prezime }}</h3>

        <h3 class="tekst">Datum rođenja</h3>
        <h3 class="podaci">{{ userData.datumRodenja}}</h3>

        <h3 class="tekst">Email korisnika</h3>
        <h3 class="podaci">{{ userData.email }}</h3>

        <div class="center" v-if="this.zastavica == true">

            <h3 class="tekst" style="text-align: center; margin-top: 30px;">Ažuriraj profil</h3>

            <v-text-field
                style="background-color: green; margin-top: 30px; margin-bottom: 20px; width: 100%;"  
                v-model="profilna"
                label="Nova profilna slika"
            ></v-text-field>

            <v-btn class="btn_style" @click="updateUser(), funkcijaFalse()">Ažuriraj profil</v-btn>
            <v-btn class="btn_style" @click="funkcijaFalse()">Odustani</v-btn>
        </div>

        <div class="center" v-if="this.zastavica2 == true">

            <h3 class="tekst" style="text-align: center; margin-top: 30px;">Promijeni lozinku</h3>

            <v-text-field
                v-model="password"
                :rules="[rules.password, rules.length(6), rules.required]"
                filled
                color="black"
                counter="6"
                label="Nova lozinka"
                style="min-height: 100px; width: 50%;"
                type="password"
            ></v-text-field>

            <v-btn class="btn_style" @click="funkcijaFalse2(), updateUserLozinka()">Promijeni lozinku</v-btn>
            <v-btn class="btn_style" @click="funkcijaFalse2()">Odustani</v-btn>
        </div>

        <div class="center" v-if="this.zastavica == false && this.zastavica2 == false">
            <v-btn class="btn_style" @click="funkcijaTrue()">Ažuriraj profil</v-btn>
            <v-btn class="btn_style" @click="funkcijaTrue2()">Promijeni lozinku</v-btn>
            <v-btn class="btn_style" @click="deleteUser()" style="background-color: red !important; color: white; font-size: 30px;">Izbriši račun</v-btn>
        </div>
    </div>
</template>
<script>
    import { Auth } from '@/components/registracija'
    import axios from 'axios';

    export default {
        data: () => ({
            auth: Auth.state,
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
                const userEmail = this.auth.userEmail;
                const response = await axios.get(`https://nogometna-aplikacija.onrender.com/api/user/dohvat?email=${userEmail}`);
                if (response.status !== 200) {
                    throw new Error('Network response was not ok');
                } 
                this.userData = response.data
                } catch (error) {
                    console.error('Greška prilikom dohvaćanja podataka korisnika:', error);
                }
            },

            async updateUser() {
                let response = await axios.patch("https://nogometna-aplikacija.onrender.com/api/user/update/podaci", {
                    profilna: this.profilna,
                    email: this.auth.userEmail
                })
                window.location.reload();
            },

            async updateUserLozinka() {
                let response = await axios.patch("https://nogometna-aplikacija.onrender.com/api/user/update/lozinka", {
                    lozinka: this.password,
                    email: this.auth.userEmail
                })
                this.signOut();
            },

            async deleteUser() {
                if(confirm("Jeste li sigurni da želite izbrisati račun?")) {
                    let response = await axios.patch("https://nogometna-aplikacija.onrender.com/api/user/delete", {
                        userEmail: this.auth.userEmail
                    })
                    alert("Korisnikči profil je izbrisan!")
                    this.signOut();
                }
            },

            async signOut() {
                Auth.logout();
                this.$router.push({path: "/Login"});
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