import axios from "axios";
import $router from "@/router";

const API_AUTH_BASE = process.env.VUE_APP_AUTH_API;

// 1) Public instance (BEZ tokena, bez interceptora)
const Public = axios.create({
  baseURL: API_AUTH_BASE,
  timeout: 5000,
});

// 2) Private instance (S tokenom)
const Service = axios.create({
  baseURL: API_AUTH_BASE,
  timeout: 5000,
});

Service.interceptors.request.use((request) => {
  const token = Auth.getToken();
  if (token) {
    request.headers["Authorization"] = "Bearer " + token;
  }
  return request;
});

Service.interceptors.response.use(
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
      const response = await axios.post(`${API_AUTH_BASE}/api/auth/login`,
        { email, password }
      );

      const user = response.data;
      localStorage.setItem("user", JSON.stringify(user));
      return true;

    } catch (err) {
      const status = err.response?.status;

      if (status === 401) {
        window.alert("Neispravan email ili lozinka");
        return false;
      }

      if (status === 422) {
        window.alert("Neispravan unos podataka");
        return false;
      }

      window.alert("Došlo je do greške prilikom prijave");
      return false;
    }
  },

  async signin(name, surname, date, email, password, profilna, pin) {
    try {
      const response = await axios.post(`${API_AUTH_BASE}/api/auth/signup`, {
          ime: name,
          prezime: surname,
          datumRodenja: date,
          email,
          password,
          profilnaSlika: profilna,
          pin: Number(pin),
        }
      );

      const user = response.data;
      localStorage.setItem("user", JSON.stringify(user));
      return true;

    } catch (err) {
      const status = err.response?.status;

      if (status === 409) {
        window.alert("Račun s ovim emailom već postoji");
        return false;
      }

      if (status === 422) {
        window.alert("Provjeri unesene podatke");
        return false;
      }

      window.alert("Došlo je do greške prilikom registracije");
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
      const detail = err.response?.data?.detail;

      // PIN ili validacija
      if (status === 422) {
        window.alert("Neispravan pin");
        return false;
      }

      // korisnik ne postoji
      if (status === 404) {
        window.alert("Korisnik ne postoji");
        return false;
      }

      // fallback
      window.alert("Došlo je do greške. Pokušajte ponovno.");
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
    const user = Auth.getUser();
    return user?.token || false;
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

export { Service, Public, Auth };
