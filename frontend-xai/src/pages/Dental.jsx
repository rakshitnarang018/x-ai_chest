import { useState } from "react";
import { motion } from "framer-motion";

import ImageUploader from "../components/upload/ImageUploader";
import PredictionCard from "../components/results/PredictionCard";
import GradCamViewer from "../components/visualization/GradCamViewer";
import LlamaResponse from "../components/ai/LlamaResponse";
import LimeButton from "../components/buttons/LimeButton";
import BoundingBoxOverlay from "../components/visualization/BoundingBoxOverlay";

import {
 analyzeImage
} from "../services/predictionService";

import useAnalysisPolling from "../hooks/useAnalysisPolling";

export default function Dental(){

const [image,setImage]=useState(null);
const [jobId,setJobId]=useState(null);

const [prediction,setPrediction]=useState(null);

const [boxes,setBoxes]=useState([]);

const [gradcam,setGradcam]=useState(null);
const [llama,setLlama]=useState(null);

const [showBoxes,setShowBoxes]=useState(false);

const [loading,setLoading]=useState({
 prediction:false,
 gradcam:false,
 llama:false
});


const handlePollUpdate=(res)=>{

 if(res.prediction){

   setPrediction(
    res.prediction
   );

   if(
    res.prediction.detections
   ){
    setBoxes(
      res.prediction.detections
    );
   }

 }


 if(
  res.gradcam?.image_base64
 ){
 setGradcam(
`data:image/png;base64,${res.gradcam.image_base64}`
 );

 setLoading(prev=>({
   ...prev,
   gradcam:false
 }));
 }


 if(
  res.report?.report
 ){

setLlama(
`
Findings:
${res.report.report.findings}

Impression:
${res.report.report.impression}

Limitations:
${res.report.report.limitations}
`
);

setLoading(prev=>({
 ...prev,
 llama:false
}));

 }

};



const {
 stopPolling
}=useAnalysisPolling({
 jobId,
 enabled:!!jobId,
 onUpdate:handlePollUpdate
});



const handleUpload=async(file)=>{

try{

stopPolling();

setImage(
 URL.createObjectURL(file)
);

setPrediction(null);
setBoxes([]);
setGradcam(null);
setLlama(null);
setShowBoxes(false);

setLoading({
 prediction:true,
 gradcam:true,
 llama:true
});


const res=
 await analyzeImage(file);


setJobId(
 res.job_id
);

setPrediction(
 res.prediction
);

if(
 res.prediction.detections
){
 setBoxes(
  res.prediction.detections
 );
}

setLoading(prev=>({
 ...prev,
 prediction:false
}));

}
catch(err){

console.error(
"Dental analyze error:",
err
);

}

};



const handleLimeClick=()=>{
 setShowBoxes(true);
};



return(
<div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-gray-950 text-white px-6 py-10">

<motion.h1
initial={{opacity:0,y:-30}}
animate={{opacity:1,y:0}}
className="text-3xl md:text-4xl font-bold mb-8 text-center bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent"
>
Dental Image Analysis
</motion.h1>


<ImageUploader
 onUpload={handleUpload}
/>


{image && (

<motion.div
initial={{opacity:0}}
animate={{opacity:1}}
className="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-8"
>

<div className="space-y-6">

<PredictionCard
 data={prediction}
 loading={loading.prediction}
/>

<LlamaResponse
 data={llama}
 loading={loading.llama}
/>

<LimeButton
 onClick={handleLimeClick}
/>

</div>


<div className="space-y-6">

<motion.div
className="bg-white/5 border border-white/10 rounded-2xl p-4"
>

<p className="text-gray-400 mb-2">
Detected Regions
</p>

<BoundingBoxOverlay
 image={image}
 boxes={boxes}
 show={showBoxes}
/>

</motion.div>


<GradCamViewer
 data={gradcam}
 loading={loading.gradcam}
/>

</div>

</motion.div>

)}

</div>
)

}