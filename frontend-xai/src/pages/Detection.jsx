import { useState } from "react";
import { motion } from "framer-motion";

import ImageUploader from "../components/upload/ImageUploader";
import PredictionCard from "../components/results/PredictionCard";
import GradCamViewer from "../components/visualization/GradCamViewer";
import Toast from "../components/Toast";
import LlamaResponse from "../components/ai/LlamaResponse";
import LimeButton from "../components/buttons/LimeButton";
import LimeOverlay from "../components/visualization/LimeOverlay";
import BoundingBoxOverlay from "../components/visualization/BoundingBoxOverlay";
import DownloadReportButton from "../components/buttons/DownloadReportButton";

import {
  analyzeImage,
  requestLime
} from "../services/predictionService";

import useAnalysisPolling from "../hooks/useAnalysisPolling";


export default function Detection(){

/* =========================
STATE
========================= */

const [image,setImage]=useState(null);
const [jobId,setJobId]=useState(null);

const [prediction,setPrediction]=useState(null);
const [scanType,setScanType]=useState(null);

const [gradcam,setGradcam]=useState(null);
const [llama,setLlama]=useState(null);
const [lime,setLime]=useState(null);

const [dentalBoxes,setDentalBoxes]=useState([]);
const [showDentalBoxes,setShowDentalBoxes]=useState(false);

const [toast,setToast]=useState(null);
const [error,setError]=useState(null);

const [uploading,setUploading]=useState(false);

const [loading,setLoading]=useState({
 prediction:false,
 gradcam:false,
 llama:false,
 lime:false
});



/* =========================
Toast helper
========================= */
const showToast=(msg)=>{
 setToast(msg);

 setTimeout(()=>{
   setToast(null);
 },3000);
};



/* =========================
Polling Update Callback
========================= */

const handlePollUpdate=(res)=>{

/* prediction updates */
if(res.prediction){

 setPrediction(
   res.prediction
 );

 if(
  res.prediction.domain==="dental" &&
  res.prediction.detections
 ){
   setDentalBoxes(
     res.prediction.detections
   );
 }

}



/* ---------------------
GRADCAM
--------------------- */

if(
 res.status.gradcam==="done" &&
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
 res.status.gradcam==="failed"
){
 setLoading(prev=>({
   ...prev,
   gradcam:false
 }));

 setError(
  "Grad-CAM generation failed."
 );
}



/* ---------------------
REPORT
--------------------- */

if(
 res.status.report==="done" &&
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

showToast(
 "AI report ready"
);

}


if(
 res.status.report==="failed"
){

 setLoading(prev=>({
  ...prev,
  llama:false
 }));

 setLlama(
  "AI report unavailable."
 );

 setError(
  "Report generation failed."
 );

}



/* ---------------------
LIME
--------------------- */

if(
 res.status.lime==="done" &&
 res.lime?.image_base64
){

setLime(
`data:image/png;base64,${res.lime.image_base64}`
);

setLoading(prev=>({
 ...prev,
 lime:false
}));

showToast(
 "LIME explanation ready"
);

}


if(
 res.status.lime==="failed"
){

 setLoading(prev=>({
   ...prev,
   lime:false
 }));

 setError(
  "LIME generation failed."
 );

}

};



/* =========================
Polling Hook
========================= */

const {
 restartPolling,
 stopPolling
}=useAnalysisPolling({
 jobId,
 enabled:!!jobId,
 onUpdate:handlePollUpdate
});



/* =========================
UPLOAD
========================= */

const handleUpload=async(file)=>{

if(uploading) return;

try{

setUploading(true);

setError(null);

stopPolling();

setJobId(null);

setImage(
 URL.createObjectURL(file)
);


/* reset old results */
setPrediction(null);
setGradcam(null);
setLlama(null);
setLime(null);

setDentalBoxes([]);
setShowDentalBoxes(false);


setLoading({
 prediction:true,
 gradcam:true,
 llama:true,
 lime:false
});


/* fast path */
const res=
 await analyzeImage(file);


setJobId(
 res.job_id
);

setScanType(
 res.scan_type
);

setPrediction(
 res.prediction
);


if(
 res.prediction.domain==="dental" &&
 res.prediction.detections
){
 setDentalBoxes(
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
 "Analyze error:",
 err
);

setError(
 "Analysis failed. Please try again."
);

}
finally{
 setUploading(false);
}

};



/* =========================
LIME
========================= */

const handleLime=async()=>{

if(!jobId) return;


/* dental explanation mode */
if(
 prediction?.domain==="dental"
){
 setShowDentalBoxes(true);

 showToast(
  "Cavity regions highlighted"
 );

 return;
}


try{

setError(null);

setLoading(prev=>({
 ...prev,
 lime:true
}));

await requestLime(
 jobId
);

restartPolling();

}
catch(err){

console.error(
 "LIME request failed",
 err
);

setLoading(prev=>({
 ...prev,
 lime:false
}));

setError(
 "LIME generation failed."
);

}

};



return(
<div className="min-h-screen flex flex-col items-center justify-start bg-gradient-to-br from-black via-gray-900 to-gray-950 text-white px-6 py-10">


{/* Toast */}
<Toast message={toast}/>


<motion.h1
initial={{opacity:0,y:-30}}
animate={{opacity:1,y:0}}
className="text-3xl md:text-4xl font-bold mb-8 text-center bg-gradient-to-r from-blue-400 via-purple-400 to-pink-500 bg-clip-text text-transparent"
>
Medical Image Detection
</motion.h1>


{/* Error Banner */}
{
error && (
<motion.div
initial={{opacity:0}}
animate={{opacity:1}}
className="
bg-red-500/20
border border-red-500/50
text-red-300
px-6 py-3
rounded-xl
mb-6
"
>
{error}
</motion.div>
)
}


<ImageUploader
 onUpload={handleUpload}
/>


{image && (

<motion.div
initial={{opacity:0}}
animate={{opacity:1}}
className="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-8"
>

{/* LEFT */}
<div className="space-y-6">


{/* Progress Status */}
<motion.div
className="
bg-white/5
border border-white/10
rounded-2xl
p-4
"
>
<div className="space-y-3 text-sm">

<div>
{
loading.prediction
? "🔄 Analyzing image..."
: "✅ Prediction ready"
}
</div>

<div>
{
loading.gradcam
? "🧠 Generating Grad-CAM..."
: "✅ Grad-CAM ready"
}
</div>

<div>
{
loading.llama
? "📄 Generating report..."
: "✅ Report ready"
}
</div>

<div>
{
prediction?.domain==="dental"
? (
showDentalBoxes
? "✅ Cavity regions displayed"
: "🦷 Regions available on button click"
)
:
loading.lime
? "🧪 Generating LIME..."
: lime
? "✅ LIME ready"
: "⏳ LIME on demand"
}
</div>

</div>
</motion.div>


<PredictionCard
 data={prediction}
 loading={loading.prediction}
/>


<LlamaResponse
 data={llama}
 loading={loading.llama}
/>


<DownloadReportButton
 prediction={prediction}
 scanType={scanType}
 reportText={llama}
 gradcamImage={gradcam}
 limeImage={
 prediction?.domain==="dental"
 ? image   // use original pano and recreate boxes in report? bad
 : lime
}
 isDental={
  prediction?.domain==="dental"
 }
/>


<LimeButton
 onClick={handleLime}
 loading={loading.lime}
 disabled={!prediction}
 isDental={
   prediction?.domain==="dental"
 }
/>

</div>



{/* RIGHT */}
<div className="space-y-6">

<GradCamViewer
 data={gradcam}
 loading={loading.gradcam}
/>

{
prediction?.domain==="dental" &&
showDentalBoxes && (
<motion.div
className="
bg-white/5
border border-white/20
rounded-2xl
p-4
"
>
<p className="text-gray-300 font-semibold mb-3">
Image Explanation
</p>

<BoundingBoxOverlay
 image={image}
 boxes={dentalBoxes}
 show={true}
/>

</motion.div>
)
}

{
lime &&
prediction?.domain!=="dental" && (
<LimeOverlay
 image={lime}
/>
)
}

</div>

</motion.div>

)}

</div>
)

}