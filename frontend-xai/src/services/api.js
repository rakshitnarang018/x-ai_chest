import axios from "axios";

const api = axios.create({
  baseURL:"http://127.0.0.1:8000",
  timeout:30000
});


api.interceptors.response.use(
 res=>res,

 async(error)=>{

  const config=error.config;

  if(
   !config ||
   config.__retry
  ){
   return Promise.reject(error);
  }

  if(
   error.code==="ECONNABORTED" ||
   !error.response
  ){

   config.__retry=true;

   console.warn(
    "Retrying request..."
   );

   return api(config);
  }

  return Promise.reject(error);
 }
);

export default api;