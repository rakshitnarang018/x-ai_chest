import { motion } from "framer-motion";

export default function GradCamViewer({ data, loading }) {

return(
<motion.div
 initial={{opacity:0,y:40}}
 animate={{opacity:1,y:0}}
 className="
bg-white/5
backdrop-blur-xl
border border-white/10
rounded-2xl
p-4
shadow-lg
"
>

<h2 className="text-lg font-semibold mb-3 text-white">
Grad-CAM Visualization
</h2>


{loading && (
<div className="
w-full
min-h-[320px]
h-[55vh]
max-h-[650px]
flex items-center justify-center
rounded-xl
bg-white/5
border border-white/10
relative
">

<motion.div
 animate={{
  scale:[1,1.2,1]
 }}
 transition={{
  repeat:Infinity,
  duration:1.2
 }}
 className="
w-16 h-16 rounded-full
bg-gradient-to-r
from-blue-500 to-purple-500
opacity-70 blur-xl
"
/>

<p className="absolute text-sm text-gray-400 mt-28">
Generating heatmap...
</p>

</div>
)}


{!loading && data && (
<motion.div
 initial={{
  scale:.96,
  opacity:0
 }}
 animate={{
  scale:1,
  opacity:1
 }}
 transition={{
  duration:.6
 }}
 className="
relative
min-h-[320px]
h-[55vh]
max-h-[650px]
rounded-xl
overflow-hidden
bg-black/20
flex items-center justify-center
"
>

<div className="
absolute inset-0
bg-gradient-to-r
from-blue-500/20
to-purple-500/20
blur-xl opacity-60
"/>

<img
 src={data}
 alt="GradCAM"
 className="
relative
w-full
h-full
object-contain
"
/>

</motion.div>
)}


{!loading && !data && (
<p className="text-gray-400 text-sm">
Grad-CAM will appear after processing.
</p>
)}

</motion.div>
)

}