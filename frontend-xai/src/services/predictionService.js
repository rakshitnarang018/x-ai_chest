import api from "./api";

/*
Backend Contract

GET  /health
POST /analyze
GET  /analysis/{job_id}
POST /analysis/{job_id}/lime
*/


/* -----------------------------
Health Check
----------------------------- */
export const checkHealth = async () => {
  const res = await api.get("/health");
  return res.data;
};


/* -----------------------------
Upload + Fast Prediction
multipart/form-data
----------------------------- */
export const analyzeImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await api.post(
    "/analyze",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return res.data;
};


/* -----------------------------
Polling endpoint
----------------------------- */
export const getAnalysis = async (jobId) => {
  const res = await api.get(
    `/analysis/${jobId}`
  );

  return res.data;
};


/* -----------------------------
On-demand LIME trigger
----------------------------- */
export const requestLime = async (jobId) => {
  const res = await api.post(
    `/analysis/${jobId}/lime`
  );

  return res.data;
};