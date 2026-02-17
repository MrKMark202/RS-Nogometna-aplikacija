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
  }
};

export default MatchApi;