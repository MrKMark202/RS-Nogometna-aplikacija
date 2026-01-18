import axios from "axios";

// Base URL iz .env (preporuka)
const API_CLUB_BASE = process.env.VUE_APP_CLUB_API;

const Public = axios.create({
  baseURL: API_CLUB_BASE,
  timeout: 5000,
});

const ClubApi = {
  async getLeaguesForSelect(korisnikEmail) {
    try {
      const res = await Public.get("/api/club/leagues", {
        params: { korisnikEmail },
      });
      return res.data; // [{_id, naziv, ...}]
    } catch (err) {
      console.error("getLeaguesForSelect error:", err.response?.data || err.message);
      window.alert("Ne mogu dohvatiti lige.");
      return [];
    }
  },

  async createClub({ naziv, godinaOsnivanja, drzava, grbKluba, ligaId, korisnikEmail }) {
    try {
      const payload = { naziv, godinaOsnivanja, drzava, grbKluba, ligaId, korisnikEmail };

      console.log("Create club payload:", payload);

      const res = await Public.post("/api/club/create", payload);
      return res.data; // vrati kreirani dokument
    } catch (err) {
      const status = err.response?.status;
      const data = err.response?.data;

      // Jednostavne, “user-friendly” poruke
      if (status === 409) {
        window.alert("Klub s tim nazivom već postoji.");
        return false;
      }
      if (status === 404) {
        window.alert(data?.detail || "Liga ili korisnik nije pronađen.");
        return false;
      }
      if (status === 422) {
        window.alert("Provjeri unos (neka polja su prazna ili liga nije odabrana).");
        return false;
      }

      window.alert("Greška pri kreiranju kluba.");
      console.error("createClub error:", data || err.message);
      return false;
    }
  },
};

export default ClubApi;