import axios from "axios";
import { Auth } from "@/components/registracija";

const API_LEAGUE_BASE = process.env.VUE_APP_LEAGUE_API;

const LigaApi = {
  async createLeague(naziv, godinaOsnivanja, drzava, grbLige) {
    try {
      const korisnikEmail = Auth.state.userEmail;

      await axios.post(`${API_LEAGUE_BASE}/api/league/create`, {
        naziv,
        godinaOsnivanja,
        drzava,
        grbLige,
        korisnikEmail,
      });

      return true;
    } catch (err) {
      const status = err.response?.status;

      if (status === 409) return alert("Liga s tim nazivom već postoji"), false;
      if (status === 422) return alert("Provjeri unesene podatke"), false;
      if (status === 404) return alert("Korisnik nije pronađen"), false;

      alert("Došlo je do greške pri kreiranju lige");
      return false;
    }
  },

  async getLeagues() {
    try {
      const korisnikEmail = Auth.state.userEmail;

      const res = await axios.get(`${API_LEAGUE_BASE}/api/league/dohvat`, {
        params: { korisnikEmail },
      });

      return res.data; // lista liga
    } catch (err) {
      alert("Ne mogu dohvatiti lige");
      return [];
    }
  },

  async deleteLeague(leagueId) {
    try {
      const korisnikEmail = Auth.state.userEmail;

      await axios.delete(`${API_LEAGUE_BASE}/api/league/delete`, {
        data: { leagueId, korisnikEmail }, // DELETE body
      });

      return true;
    } catch (err) {
      const status = err.response?.status;

      if (status === 403) return alert("Nemaš pravo obrisati ovu ligu"), false;
      if (status === 404) return alert("Liga nije pronađena"), false;

      alert("Došlo je do greške pri brisanju lige");
      return false;
    }
  },
};

export default LigaApi;