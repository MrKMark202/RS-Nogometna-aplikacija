import axios from "axios";
import $router from "@/router";

const API_AUTH_BASE = process.env.VUE_APP_AUTH_API;

// ---------------- PUBLIC (bez tokena) ----------------

const Public = axios.create({
  baseURL: API_AUTH_BASE,
  timeout: 5000,
});

// ---------------- AUTH (sa tokenom) ----------------

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

// ---------------- AUTH OBJECT ----------------

let Auth = {

  // ---------------- LOGIN ----------------

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

      alert("Greška prilikom prijave");
      return false;
    }
  },

  // ---------------- SIGNUP ----------------

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

      if (status === 409) return alert("Račun već postoji"), false;
      if (status === 422) return alert("Provjeri podatke"), false;

      alert("Greška prilikom registracije");
      return false;
    }
  },

  // ---------------- RESET LOZINKE (PIN) ----------------

  async passwordReset(email, newPassword, pin) {
    try {
      await Public.patch("/api/auth/update/lozinka/reset", {
        email,
        lozinka: newPassword,
        pin: Number(pin),
      });

      return true;

    } catch (err) {
      const status = err.response?.status;

      if (status === 401) return alert("Neispravan PIN"), false;
      if (status === 404) return alert("Korisnik ne postoji"), false;

      alert("Greška pri resetiranju lozinke");
      return false;
    }
  },

  // ---------------- PROMJENA LOZINKE (PRIJAVLJEN) ----------------

  async passwordChange(newPassword, email) {
    try {
      await AuthService.patch("/api/user/update/lozinka/me", {
        email,
        lozinka: newPassword,
      });

      return true;

    } catch {
      alert("Greška pri promjeni lozinke");
      return false;
    }
  },

  // ---------------- DOHVAT USER PODATAKA ----------------

  async fetchUserData(email) {
    try {
      const res = await AuthService.get("/api/user/dohvat", {
        params: { email }
      });

      return res.data;

    } catch {
      alert("Greška pri dohvaćanju korisnika");
      return null;
    }
  },

  // ---------------- UPDATE PROFILNE ----------------

  async updateProfile(profilna, email) {
    try {
      await AuthService.patch("/api/user/update/podaci", {
        profilna,
        email,
      });

      // update localStorage profilne
      const user = Auth.getUser();
      user.profilna = profilna;
      localStorage.setItem("user", JSON.stringify(user));

      return true;

    } catch {
      alert("Greška pri ažuriranju profilne");
      return false;
    }
  },

  // ---------------- DELETE USER ----------------

  async deleteUser(email) {
    try {
      await AuthService.patch("/api/user/delete", {
        userEmail: email
      });

      return true;

    } catch {
      alert("Greška pri brisanju računa");
      return false;
    }
  },

  // ---------------- LOGOUT ----------------

  logout() {
    localStorage.removeItem("user");
  },

  // ---------------- GETTERS ----------------

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
