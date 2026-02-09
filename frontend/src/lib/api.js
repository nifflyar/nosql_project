import axios from "axios";

export const API_BASE = "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});
