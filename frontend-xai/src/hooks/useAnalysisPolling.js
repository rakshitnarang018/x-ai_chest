import { useEffect, useRef, useState } from "react";
import { getAnalysis } from "../services/predictionService";

export default function useAnalysisPolling({
  jobId,
  enabled,
  onUpdate,
  interval = 2000,
  maxPolls = 60
}) {

  const timerRef = useRef(null);
  const pollsRef = useRef(0);

  const [polling,setPolling] = useState(false);
  const [error,setError] = useState(null);

  const stopPolling=()=>{
    if(timerRef.current){
      clearInterval(timerRef.current);
      timerRef.current=null;
    }
    setPolling(false);
  };

  const pollOnce = async ()=>{

    if(!jobId) return;

    try{

      pollsRef.current++;

      if(
        pollsRef.current > maxPolls
      ){
        console.warn(
          "Polling timeout reached"
        );
        stopPolling();
        return;
      }

      const res =
        await getAnalysis(jobId);

      if(onUpdate){
        onUpdate(res);
      }

      const done=
        res.status.gradcam==="done" &&
        res.status.report==="done" &&
        (
          res.status.lime==="done" ||
          res.status.lime==="not_requested" ||
          res.status.lime==="failed"
        );

      if(done){
        stopPolling();
      }

    }
    catch(err){
      console.error(
        "Polling error",
        err
      );
      setError(err);
    }
  };


  const startPolling=()=>{
    if(!jobId) return;

    stopPolling();

    pollsRef.current=0;
    setPolling(true);

    timerRef.current=
      setInterval(
        pollOnce,
        interval
      );
  };


  useEffect(()=>{

    if(
      enabled &&
      jobId
    ){
      startPolling();
    }

    return ()=>stopPolling();

  },[
    enabled,
    jobId
  ]);


  return {
    polling,
    error,
    restartPolling:startPolling,
    stopPolling
  };
}