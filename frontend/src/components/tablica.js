import axios from "axios";
import { Auth } from "@/components/registracija";

const TableService = axios.create({
  baseURL: process.env.VUE_APP_TABLE_API,
  timeout: 5000,
});

TableService.interceptors.request.use((request) => {
  const token = Auth.getToken();
  if (token) {
    request.headers.Authorization = `Bearer ${token}`;
  }
  return request;
});

const TableApi = {
  async getTable(ligaId) {
    try {
      const res = await TableService.get("/api/table/dohvat", {
        params: { ligaId }
      });

      return res.data;

    } catch (err) {
      console.error("getTable error:", err.response?.data || err.message);
      alert("Ne mogu dohvatiti tablicu.");
      return [];
    }
  },

  async getKlubTablica(ligaId, klubId) {
    const res = await TableService.get("/api/table/dohvat/klub", {
      params: { ligaId, klubId }
    });
    return res.data;
  },

  async updateTablica(data) {
    const res = await TableService.patch("/api/table/update", data);
    return res.data;
  }
};

export default TableApi;
