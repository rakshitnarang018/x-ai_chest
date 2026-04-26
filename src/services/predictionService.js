import api from "./api";

export const predictImage = async (base64) => {
  const res = await api.post("/predict", { image: base64 });
  return res.data;
};

export const getGradCam = async (base64) => {
  const res = await api.post("/gradcam", { image: base64 });
  return res.data;
};

export const getLlama = async (base64) => {
  const res = await api.post("/llama", { image: base64 });
  return res.data;
};

export const getLime = async (base64) => {
  const res = await api.post("/lime", { image: base64 });
  return res.data;
};