import axios from "axios";
import { Auth } from "@/components/registracija";

const ClubService = axios.create({
  baseURL: process.env.VUE_APP_CLUB_API,
  timeout: 5000,
});

ClubService.interceptors.request.use((request) => {
  const token = Auth.getToken();
  if (token) {
    request.headers.Authorization = `Bearer ${token}`;
  }
  return request;
});

const ClubApi = {
  async getClubs(ligaId) {
    try {
      const res = await ClubService.get("/api/club/dohvat", {
        params: { ligaId }
      });
      
      return res.data;
    } catch (err) {
      alert("Ne mogu dohvatiti klubove");
      return [];
    }
  },

  async createClub({ naziv, godinaOsnivanja, drzava, grbKluba, ligaId }) {
    try {
      const res = await ClubService.post("/api/club/create", {
        naziv,
        godinaOsnivanja,
        drzava,
        grbKluba,
        ligaId,
      });

      alert("Klub je uspješno kreiran ✅");
      return res.data;

    } catch (err) {
      const status = err.response?.status;
      const data = err.response?.data;

      if (status === 409) return alert("Klub s tim nazivom već postoji."), false;
      if (status === 404) return alert(data?.detail || "Liga nije pronađena."), false;
      if (status === 401) return alert("Nisi prijavljen."), false;
      if (status === 422) return alert("Provjeri unos podataka."), false;

      alert("Greška pri kreiranju kluba.");
      console.error("createClub error:", data || err.message);
      return false;
    }
  },

  async deleteClub(clubId) {
    try {
      await ClubService.delete("/api/club/delete", {
        data: { clubId }
      });

      return true;
    } catch (err) {
      const status = err.response?.status;

      if (status === 403) alert("Nemaš pravo brisati ovaj klub.");
      else if (status === 404) alert("Klub nije pronađen.");
      else alert("Greška pri brisanju kluba.");

      return false;
    }
  }
};

export default ClubApi;
