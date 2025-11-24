import axios from 'axios';
import $router from '@/router'

let Service = axios.create({
    baseURL: 'https://nogometna-aplikacija.onrender.com/',
    timeout: 1000,
});

Service.interceptors.request.use((request) => {
    let token = Auth.getToken()

    if (!token) {
        $router.go();
        return;
    }
    else {
        request.headers["Authorization"] = 'Bearer' + token;
    }

    return request;
})

Service.interceptors.response.use((response) => response, (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
        Auth.logout();
        $router.go();
    }
})

let Auth = {
    async login(email, password) {
        let response = await axios.post("https://nogometna-aplikacija.onrender.com/api/auth/login", {
            email: email,
            password: password,
        })

        let user = response.data;

        localStorage.setItem('user', JSON.stringify(user));

        return true;
    },

    logout() {
        localStorage.removeItem('user');
    },

    async signin(name, surname, date, email, password, profilna, pin) {
        let response = await axios.post("https://nogometna-aplikacija.onrender.com/api/auth/signUp", {
            ime: name,
            prezime: surname,
            datumRodenja: date,
            email: email,
            password: password,
            profilna: profilna,
            pin: pin
        })

        let user = response.data;

        localStorage.setItem('user', JSON.stringify(user));

        return true;
    },

    async passwordChange(email, newPassword, pin) {
        let response = await axios.patch("https://nogometna-aplikacija.onrender.com/api/auth/passwordChange", {
            email: email,
            password: newPassword,
            pin: pin
        })

        return true;
    },

    getUser() {
        return JSON.parse(localStorage.getItem('user'));
    },

    getToken() {
        let user = Auth.getUser();
        if (user && user.token) {
            return user.token;
        }
        else {
            return false;
        }
    },

    authenticated() {
        let user = Auth.getUser();
        if (user && user.token) {
            return true
        }
        return false;
    },

    state: {
        get authenticated() {
            return Auth.authenticated();
        },

        get userEmail() {
            let user = Auth.getUser();

            if (user) {
                return user.email;
            }
        },

        get userProfilePicture() {
            let user = Auth.getUser();

            if (user) {
                return user.profilna;
            }
        }
    }
};

export {Service, Auth};