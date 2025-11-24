<template>
    <div>
        <div class="naslov2">
            <h1>Resetirajte svoju lozinku!</h1>
        </div>

        <v-card
            class="mx-auto"
            style="max-width: 500px; margin-top: 80px; margin-left: auto; margin-right:auto; padding: 30px;"
        >

            <v-form
                ref="form"
                v-model="form"
                style="margin-top: 20px;"
            >
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
                    v-model="newPassword"
                    :rules="[rules.password, rules.length(6), rules.required]"
                    filled
                    color="black"
                    counter="6"
                    label="Lozinka"
                    style="min-height: 100px"
                    type="password"
                ></v-text-field>


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

                <v-card-actions class="card-actions">
					<v-btn
                        class="butot"
                        style="color:white;"
						outlined
						text
						@click="passwordChange()"
                    >
					    Pošalji zahtjev!
					</v-btn>
				</v-card-actions>
            </v-form>
        </v-card>
    </div>
</template>
    
<script>

    import { Auth } from '@/components/registracija';

    export default {
        name: "passReset",
        data: () => ({   
            form: false,
            email: null,
            pin: null,
            newPassword: null,
            rules: {
                email: v => !!(v || '').match(/@/) || 'Please enter a valid email',
                length: len => v => (v || '').length >= len || `Invalid character length, required ${len}`,
                password: v => !!(v || '').match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$/) ||
                'Password must contain an upper case letter, a numeric character, and a special character',
                required: v => !!v || 'This field is required',
            },  
        }),

        methods: {
            async passwordChange() {
                let success = await Auth.passwordChange(this.email, this.newPassword, this.pin);
                console.log("Rezultat promjene lozinke:", success);

                if(success == true) {
                    this.$router.push({path: "/Login"})
                }
            }
        }
    };
</script>
    
<style>
    .naslov2
    {
        font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
        text-align: center;
        color: white;
        margin-top:120px;
    }
</style>