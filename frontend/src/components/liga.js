import axios from "axios";
import { Auth } from "@/components/registracija";

const LeagueService = axios.create({
  baseURL: process.env.VUE_APP_LEAGUE_API,
  timeout: 5000,
});

LeagueService.interceptors.request.use((request) => {
  const token = Auth.getToken();
  if (token) {
    request.headers.Authorization = `Bearer ${token}`;
  }
  return request;
});

const LeagueApi = {
  async createLeague(naziv, godinaOsnivanja, drzava, grbLige) {
  try {
    await LeagueService.post("/api/league/create", {
      naziv,
      godinaOsnivanja,
      drzava,
      grbLige,
    });

    alert("Liga je uspješno kreirana ✅");
    return true;

  } catch (err) {
    const status = err.response?.status;

    if (status === 409) return alert("Liga s tim nazivom već postoji"), false;
    if (status === 401) return alert("Nisi prijavljen"), false;

    alert("Došlo je do greške pri kreiranju lige");
    return false;
  }
},

  async getLeagues() {
    try {
      const res = await LeagueService.get("/api/league/dohvat");
      return res.data;
    } catch (err) {
      alert("Ne mogu dohvatiti lige");
      return [];
    }
  },

  async deleteLeague(leagueId) {
    try {
      await LeagueService.delete("/api/league/delete", {
        data: { leagueId },
      });

      return true;
    } catch (err) {
      const status = err.response?.status;

      if (status === 403) return alert("Nemaš pravo obrisati ovu ligu"), false;
      if (status === 404) return alert("Liga nije pronađena"), false;
      if (status === 401) return alert("Nisi prijavljen"), false;

      alert("Došlo je do greške pri brisanju lige");
      return false;
    }
  },
};

export default LeagueApi;
