import axios from "axios";
import $router from "@/router";
import jwt_decode from "jwt-decode";

const API_AUTH_BASE = process.env.VUE_APP_AUTH_API;

const Public = axios.create({
  baseURL: API_AUTH_BASE,
  timeout: 5000,
});

const AuthService = axios.create({
  baseURL: API_AUTH_BASE,
  timeout: 5000,
});

AuthService.interceptors.request.use((request) => {
  const token = Auth.getToken();
  if (token) {
    request.headers.Authorization = `Bearer ${token}`;
  }
  return request;
});

AuthService.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      Auth.logout();
      $router.push({ path: "/Login" });
    }
    return Promise.reject(error);
  }
);

let Auth = {
  async login(email, password) {
    try {
      const response = await Public.post("/api/auth/login", {
        email,
        password,
      });

      localStorage.setItem("user", JSON.stringify(response.data));
      return true;
    } catch (err) {
      const status = err.response?.status;

      if (status === 401) return alert("Neispravan email ili lozinka"), false;
      if (status === 422) return alert("Neispravan unos podataka"), false;

      alert("Došlo je do greške prilikom prijave");
      return false;
    }
  },

  async signin(name, surname, date, email, password, profilna, pin) {
    try {
      const response = await Public.post("/api/auth/signup", {
        ime: name,
        prezime: surname,
        datumRodenja: date,
        email,
        password,
        profilnaSlika: profilna,
        pin: Number(pin),
      });

      localStorage.setItem("user", JSON.stringify(response.data));
      return true;
    } catch (err) {
      const status = err.response?.status;

      if (status === 409) return alert("Račun s ovim emailom već postoji"), false;
      if (status === 422) return alert("Provjeri unesene podatke"), false;

      alert("Došlo je do greške prilikom registracije");
      return false;
    }
  },

  async passwordChange(email, newPassword, pin) {
    try {
      await Public.patch("/api/user/update/lozinka", {
        email,
        lozinka: newPassword,
        pin: Number(pin),
      });

      return true;
    } catch (err) {
      const status = err.response?.status;

      if (status === 422) return alert("Neispravan pin"), false;
      if (status === 404) return alert("Korisnik ne postoji"), false;

      alert("Došlo je do greške. Pokušajte ponovno.");
      return false;
    }
  },

  logout() {
    localStorage.removeItem("user");
  },

  getUser() {
    return JSON.parse(localStorage.getItem("user"));
  },

  getToken() {
    return Auth.getUser()?.token || null;
  },

  state: {
    get authenticated() {
      return !!Auth.getToken();
    },
    get userEmail() {
      return Auth.getUser()?.email;
    },
    get userProfilePicture() {
      return Auth.getUser()?.profilna;
    },
  },
};

export { AuthService, Public, Auth };
