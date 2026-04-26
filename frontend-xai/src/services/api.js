import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // 🔥 change to your backend
});

export default api;