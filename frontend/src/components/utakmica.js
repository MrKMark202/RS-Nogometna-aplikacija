import axios from "axios";
import { Auth } from "@/components/registracija";

const MatchService = axios.create({
  baseURL: process.env.VUE_APP_MATCH_API,
  timeout: 5000,
});

MatchService.interceptors.request.use((request) => {
  const token = Auth.getToken();
  if (token) {
    request.headers.Authorization = `Bearer ${token}`;
  }
  return request;
});

const MatchApi = {

  async createMatch({
    kolo,
    mjestoIgranja,
    stadionNaziv,
    gledateljiBroj,
    datum,
    satUpisa,
    liga,
    domacin,
    gost,
    domacinGol,
    gostiGol
  }) {
    try {
      const res = await MatchService.post("/api/match/create", {
        kolo,
        mjestoIgranja,
        stadionNaziv,
        gledateljiBroj,
        datum,
        satUpisa,
        liga,
        domacin,
        gost,
        domacinGol,
        gostiGol
      });

      alert("Utakmica je uspješno kreirana ✅");
      return res.data;

    } catch (err) {
      console.log(err.response?.data);
      return false;
    }
  },

  async getMatch(ligaId) {
    try {
      const res = await MatchService.get("/api/match/dohvat", {
        params: { ligaId }
      });

      return res.data;

    } catch (err) {
      console.log("Greška kod dohvaćanja utakmica:", err.response?.data);
      return [];
    }
  },

  async deleteMatch({ liga, domacin, gost, kolo }) {
    try {
      const res = await MatchService.patch("/api/match/delete", {
        liga,
        domacin,
        gost,
        kolo,
      });

      return res.data;
    } catch (err) {
      console.log(err.response?.data);
      return false;
    }
  },

  async getSingleMatch({ liga, domacin, gost, kolo }) {
  try {
    const res = await MatchService.get("/api/match/one", {
      params: {
        liga,
        domacin,
        gost,
        kolo
      }
    });

    return res.data;

  } catch (err) {
    console.log(err.response?.data);
    return null;
  }
},

};

export default MatchApi;
