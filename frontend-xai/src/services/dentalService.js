import api from "./api";

export const predictDental = async (base64) => {
  const res = await api.post("/predict-dental", { image: base64 });
  return res.data;
};