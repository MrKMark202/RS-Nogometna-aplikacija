<template>
  <div data-app>
    <div class="naslov1">
      <h1>SignUp</h1>
    </div>

    <v-card
      class="mx-auto"
      style="max-width: 800px; margin-top: 80px; margin-left: auto; margin-right:auto; padding: 30px;"
    >

      <v-card-title> Imaš li već račun? <v-btn to="/LogIn" style="margin-left:10px; color:black; text-decoration: none;"> Prijavi se! </v-btn> </v-card-title>

      <v-form ref="form" v-model="form" style="margin-top: 20px;">

        <v-text-field
          v-model="name"
          filled
          label="Ime"
          style="min-height: 100px;"
          :rules="[rules.required]"
          type="text"
        ></v-text-field>

        <v-text-field
          v-model="surname"
          filled
          color="black"
          label="Prezime"
          style="min-height: 100px"
          :rules="[rules.required]"
          type="text"
        ></v-text-field>

        <v-dialog
          ref="dialog"
          v-model="modal"
          :return-value.sync="date"
          persistent
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="date"
              label="Odaberite datum rođenja"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
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
              @click="modal = false"
            > Cancel </v-btn>

            <v-btn
              text
              color="primary"
              @click="$refs.dialog.save(date)"
            > OK </v-btn>
          </v-date-picker>
        </v-dialog>

        <v-text-field
          v-model="email"
          :rules="[rules.email, rules.required]"
          filled
          color="black"
          label="Email adresa"
          style="min-height: 100px"
          type="email"
        ></v-text-field>

        <v-text-field
          v-model="password"
          :rules="[rules.password, rules.length(6), rules.required]"
          filled
          color="black"
          counter="6"
          label="Lozinka"
          style="min-height: 100px"
          type="password"
        ></v-text-field>

        <h3>! Pin će služiti za promjenu lozinke ukoliko ste ju zaborvili prije prijave !</h3>
        <h3 style="color: red">! Nemojte ga zaboraviti !</h3>

        <v-text-field
          v-model="pin"
          filled
          color="black"
          label="Pin za promjenu lozinke"
          style="min-height: 100px"
          :rules="[rules.required]"
          counter="5"
          type="text"
          onkeypress='return event.charCode >= 48 && event.charCode <= 57'
        ></v-text-field>

        <h3>! Potrebno postaviti link slike sa interneta ili diskorda !</h3>

        <v-text-field
          class="butot"  
          :rules="[rules.required]"
          v-model="profilna"
          label="Profilna slika"
        ></v-text-field>

        <v-checkbox
          v-model="agreement"
          :rules="[rules.required]"
          color="black"
        >
          <template v-slot:label>
            I agree to the Terms of Service and Privacy Policy
          </template>
        </v-checkbox>
      </v-form>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn
          style="margin-bottom: 10px;"
          text
          @click="$refs.form.reset()"
        >
          Clear
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          type="button"
          :disabled="!form"
          :loading="isLoading"
          class="butot"
          depressed
          @click="signUp()"
        >
          SignUP!
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>


<script>
  import { Auth } from '@/components/registracija';

  export default {
    name: "Signup",
    components: {},
    data: () => ({
      name: null,
      surname: null,
      email: null,
      profilna: null,
      form: false,
      isLoading: false,
      password: null,
      pin: null,
      date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      modal: false,
      rules: {
        email: v => !!(v || '').match(/@/) || 'Please enter a valid email',
        length: len => v => (v || '').length >= len || `Invalid character length, required ${len}`,
        password: v => !!(v || '').match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$/) ||
          'Password must contain an upper case letter, a numeric character, and a special character',
        required: v => !!v || 'This field is required',
      },
    }),

    methods: {

      clearFormData() {
			  this.name = null;
			  this.surname = null;
			  this.email = null;
			  this.password = null;
        this.birthDate = null;
        this.date = null;
        this.profilna = null;
        this.pin = null;
		  },

      async signUp() {
        let success = await Auth.signin(this.name, this.surname, this.date, this.email, this.password, this.profilna, this.pin);
        console.log("Rezultat registracije:", success);

        if(success == true) {
          this.clearFormData();
          this.$router.push({path: "/Login"})
        }
      }
    }
  };
</script>

<style>
  .obrub1
  {
    border: 2px solid white;
    background-color: white;
    padding: 50px;
    margin-left: 200px;
    margin-right: 200px;
    margin-top: 100px;
    margin-bottom: 100px;
  }

  .naslov1
  {
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    text-align: center;
    color: white;
    margin-top:120px;
  }
</style>